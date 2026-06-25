from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from youtube_transcript_api.formatters import TextFormatter, JSONFormatter
import yt_dlp
import re
import argparse
import sys
import json
from pathlib import Path
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="🎥 YouTube Clean Transcript Downloader")
    parser.add_argument("--url", "-u", help="YouTube video URL")
    parser.add_argument("--output", "-o", default="transcripts",
                        help="Output folder (default: transcripts/)")
    args = parser.parse_args()

    print("🎥 YouTube Transcript Downloader (Clean + Raw + Info)")
    print("=" * 65)

    # Get the URL
    if args.url:
        video_url = args.url.strip()
    else:
        video_url = input("\nPaste the YouTube video URL here:\n> ").strip()

    if not video_url:
        print("❌ No URL provided. Exiting.")
        sys.exit(1)

    # Fetch metadata
    print("🔍 Fetching title and metadata...")
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'transcript')
            video_id = info['id']
    except Exception as e:
        print(f"❌ Error while fetching title: {e}")
        sys.exit(1)

    # Clean title for filename
    safe_title = re.sub(r'[\\/*?:"<>|]', '', title)
    safe_title = re.sub(r'\s+', ' ', safe_title).strip()[:150]

    print(f"📹 Video: {title}")

    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # === Fetch transcript ===
    print("📝 Fetching transcript...")
    try:
        yt_api = YouTubeTranscriptApi()
        transcript = yt_api.fetch(video_id, languages=['en', 'fr', 'en-US'])

        # ==================== VIDEO INFO JSON ====================
        video_info = {
            "video_url": video_url,
            "video_id": video_id,
            "title": title,
            "safe_title": safe_title,
            "download_date": datetime.now().isoformat(),
            "language_codes": ['en', 'fr', 'en-US']
        }

        info_file = output_dir / f"{safe_title}_info.json"
        with open(info_file, "w", encoding="utf-8") as f:
            json.dump(video_info, f, ensure_ascii=False, indent=2)

        # ==================== RAW TRANSCRIPT ====================
        raw_file = output_dir / f"{safe_title}_raw.json"
        json_formatter = JSONFormatter()
        with open(raw_file, "w", encoding="utf-8") as f:
            f.write(json_formatter.format_transcript(transcript, indent=2))

        # ==================== CLEAN TRANSCRIPT ====================
        text_formatter = TextFormatter()
        clean_text = text_formatter.format_transcript(transcript)

        clean_file = output_dir / f"{safe_title}.txt"
        
        header = f"""# {title}
URL: {video_url}
Video ID: {video_id}

---

"""
        clean_file.write_text(header + clean_text, encoding="utf-8")

        # ==================== Success ====================
        print(f"\n===TRANSCRIPT_FILE:{clean_file.absolute()}===")
        print(f"\n✅ Success!")
        print(f"   📄 Clean transcript     → {clean_file.name}")
        print(f"   📊 Raw transcript       → {raw_file.name}")
        print(f"   ℹ️  Info file           → {info_file.name}")
        print(f"   ≈ {len(clean_text.split())} words")
        print(f"   📁 Folder: {output_dir.resolve()}")
        
    except (NoTranscriptFound, TranscriptsDisabled) as e:
        print(f"❌ No transcript available: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("💡 Tip: the video must have subtitles (auto or manual).")


if __name__ == "__main__":
    main()
