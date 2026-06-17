# YouTube Clean Transcript

Outil Python simple et propre pour récupérer un **transcript bien formaté** (sous-titres auto ou manuels) d’une vidéo YouTube.

## Installation

```bash
git clone https://github.com/ErwanDevigon/youtube-clean-transcript.git
cd youtube-clean-transcript
pip install -r requirements.txt
```

## Utilisation

**Méthode recommandée** (depuis la racine du projet) :

```bash
python -m youtube_transcript.main --url "https://www.youtube.com/watch?v=..."
```

Ou directement :

```bash
cd src/youtube_transcript
python main.py
```

## Fonctionnalités
- Récupère automatiquement le titre de la vidéo
- Télécharge le transcript (priorité : anglais → français)
- Nettoie le texte et le sauvegarde dans un fichier `.txt` avec un nom propre
- Gestion des erreurs claire

## Auteur
**ErwanDevigon**
