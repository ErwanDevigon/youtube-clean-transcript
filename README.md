# YouTube Clean Transcript

A clean and simple Python tool to download **well-formatted transcripts** (auto-generated or manual subtitles) from any YouTube video.

---

## Features

- Automatically fetches the video title
- Downloads the transcript with priority: English → French → others
- Cleans and formats the text nicely
- Saves both a clean `.txt` version and a raw JSON version
- Creates a lightweight `_info.json` with video metadata (URL, ID, title, date…)
- Friendly command-line interface with alias support

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/ErwanDevigon/youtube-clean-transcript.git

# 2. Create virtual environment and install
cd youtube-clean-transcript
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

---

## Usage

```bash
# Interactive mode
getyt

# Direct URL
getyt https://youtu.be/v4F1gFy-hqg

# Specify output folder
getyt https://youtu.be/v4F1gFy-hqg --output ~/MyTranscripts
```

## Recommended Alias

Add this to your `~/.zshrc` or `~/.bash_aliases`:

```bash
getyt() {
    local project_dir="$HOME/Projets/youtube-clean-transcript"
    
    # Check if venv exists
    if [[ ! -d "$project_dir/venv" ]]; then
        echo "❌ Virtual environment not found for youtube-clean-transcript."
        echo "   Please create it with:"
        echo "   cd $project_dir && python3 -m venv venv && source venv/bin/activate && pip install -e ."
        return 1
    fi

    # Run in a clean subshell
    (
        cd "$project_dir"
        source venv/bin/activate
        youtube-transcript "$@"
    )
}
```

> After adding the alias, run `source ~/.zshrc` (or `source ~/.bash_aliases`) or restart your terminal.

---

## Output Files

For each video, the tool creates:

- `{title}.txt` — Clean, readable transcript with header
- `{title}_raw.json` — Complete raw transcript (with timestamps)
- `{title}_info.json` — Video metadata (URL, ID, title, download date…)

---

## Author

**Erwan Devigon**

---
