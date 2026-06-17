from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import yt_dlp
import re

print("🎥 YouTube Transcript Downloader (propre)")
print("=" * 50)

# Demande l'URL à l'utilisateur
video_url = input("\nColle l'adresse URL de la vidéo YouTube ici :\n> ").strip()

if not video_url:
    print("❌ Aucune URL saisie. Arrêt.")
    exit()

# 1. Récupérer le titre de la vidéo
print("🔍 Récupération du titre...")
try:
    with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
        info = ydl.extract_info(video_url, download=False)
        title = info.get('title', 'transcript')
        video_id = info['id']
except Exception as e:
    print(f"❌ Erreur lors de la récupération du titre : {e}")
    exit()

# Nettoyage du titre pour un nom de fichier valide
safe_title = re.sub(r'[\\/*?:"<>|]', '', title)
safe_title = re.sub(r'\s+', ' ', safe_title).strip()[:150]  # limite à 150 caractères

print(f"📹 Vidéo : {title}")

# 2. Récupération du transcript
print("📝 Récupération du sous-titre auto-généré...")
try:
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id=video_id, languages=['en', 'fr', 'en-US'])

    formatter = TextFormatter()
    clean_text = formatter.format_transcript(transcript)

    # 3. Sauvegarde
    filename = f"{safe_title}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(clean_text)

    print(f"\n✅ Succès !")
    print(f"   Fichier créé : {filename}")
    print(f"   ≈ {len(clean_text.split())} mots")

except Exception as e:
    print(f"❌ Erreur : {e}")
    print("Astuce : essaie avec une autre vidéo ou vérifie que yt-dlp et youtube-transcript-api sont bien installés.")
