from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from youtube_transcript_api.formatters import TextFormatter
import yt_dlp
import re
import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="🎥 YouTube Clean Transcript Downloader")
    parser.add_argument("--url", "-u", help="URL de la vidéo YouTube")
    parser.add_argument("--output", "-o", default="transcripts",
                        help="Dossier de sortie (par défaut: transcripts/)")
    args = parser.parse_args()

    print("🎥 YouTube Transcript Downloader (propre)")
    print("=" * 50)

    # Récupération de l'URL
    if args.url:
        video_url = args.url.strip()
    else:
        video_url = input("\nColle l'adresse URL de la vidéo YouTube ici :\n> ").strip()

    if not video_url:
        print("❌ Aucune URL saisie. Arrêt.")
        sys.exit(1)

    # Récupération du titre
    print("🔍 Récupération du titre...")
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'transcript')
            video_id = info['id']
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du titre : {e}")
        sys.exit(1)

    # Nettoyage du titre pour le nom de fichier
    safe_title = re.sub(r'[\\/*?:"<>|]', '', title)
    safe_title = re.sub(r'\s+', ' ', safe_title).strip()[:150]

    print(f"📹 Vidéo : {title}")

    # === Création du dossier de sortie ===
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = output_dir / f"{safe_title}.txt"

    # Récupération du transcript
    print("📝 Récupération du transcript...")
    try:
        yt_api = YouTubeTranscriptApi()
        transcript = yt_api.fetch(video_id, languages=['en', 'fr', 'en-US'])

        formatter = TextFormatter()
        clean_text = formatter.format_transcript(transcript)

        filename.write_text(clean_text, encoding="utf-8")

        print(f"\n✅ Succès !")
        print(f"   Fichier créé : {filename}")
        print(f"   ≈ {len(clean_text.split())} mots")
        print(f"   📁 Dossier : {output_dir.resolve()}")
        
    except (NoTranscriptFound, TranscriptsDisabled) as e:
        print(f"❌ Pas de transcript disponible : {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        print("💡 Astuce : la vidéo doit avoir des sous-titres (auto ou manuels).")


if __name__ == "__main__":
    main()