# Quick Start

Get up and running with FED TTS in under 5 minutes.

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- A modern web browser (Chrome, Firefox, Safari, or Edge) with SpeechSynthesis support
- (Optional) ffmpeg for additional audio format support

## Installation

### Option 1: Install from source (recommended for development)

```bash
# Clone the repository
git clone https://github.com/fed-tts/fed-tts.git
cd fed-tts

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install the package in development mode
pip install -e .

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

### Option 2: Install from PyPI

```bash
pip install fed-tts
```

### Option 3: Using Conda

```bash
conda env create -f environment.yml
conda activate fed-tts
pip install -e .
```

### Option 4: Using Docker

```bash
docker build -t fed-tts .
docker run -p 8501:8501 fed-tts
```

## Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## Basic Usage

### Step 1: Upload an Audio File

1. Click the **"Browse files"** button or drag and drop an audio file
2. Supported formats: MP3, WAV, M4A, FLAC, OGG
3. The audio player will appear below the uploader

### Step 2: Transcribe the Audio

1. Play the audio using the built-in player
2. Type your transcript in the text area labeled "Transcription"
3. Your transcript is automatically saved as you type (session state)
4. Use the word count and character count in the sidebar to track progress

### Step 3: Check Grammar and Spelling

1. Click the **"Check Grammar"** button
2. Misspelled words will be highlighted with suggestions
3. Grammar issues (like "would of" → "should have") will be listed
4. Review each issue and make corrections

### Step 4: Read Aloud

1. After correcting your transcript, click **"Read Aloud"**
2. Your browser will use the operating system's built-in voice to read the text
3. Click **"Stop"** at any time to stop the speech
4. The speech rate, pitch, and volume can be adjusted (if configured)

## Example Session

Here's a complete example of using FED TTS:

```
1. Upload: meeting_recording.mp3
2. Play audio and type transcript:
   "Today we discussed the quarterly results. I would of liked to see
   more growth but the team did a good job."

3. Click "Check Grammar":
   - Spelling: No issues found
   - Grammar: "would of" detected → suggestion: "would have"

4. Fix the error:
   "Today we discussed the quarterly results. I would have liked to see
   more growth but the team did a good job."

5. Click "Read Aloud":
   - Browser reads the corrected text using OS voice
   - Click "Stop" when done

6. Copy the transcript for use elsewhere
```

## Configuration

### Custom CSS

FED TTS uses a custom CSS file (`styles.css`) for styling. You can modify
this file to change the appearance:

```css
/* Example: Change the header color */
h1, h2, h3 {
    color: #your-color-here;
}
```

### Streamlit Configuration

Create a `.streamlit/config.toml` file for Streamlit configuration:

```toml
[server]
port = 8501
address = "0.0.0.0"

[theme]
base = "light"
primaryColor = "#4a6fa5"
```

## Troubleshooting

### No audio player appears

- Ensure the uploaded file is in a supported format (MP3, WAV, M4A, FLAC, OGG)
- Check the file size — very large files may take a moment to load
- Try a different audio file

### TTS doesn't work

- Ensure your browser supports the SpeechSynthesis API (most modern browsers do)
- Check your system's TTS voices are installed
- Try a different browser
- On Linux, you may need to install speech-dispatcher:
  ```bash
  sudo apt install speech-dispatcher espeak-ng
  ```

### Transcript disappears on refresh

- This is expected behavior — session state is lost on page refresh
- Copy your transcript before refreshing

## Next Steps

- Read the [API Reference](api.md) for detailed function documentation
- Check the [Architecture](architecture.md) document for design details
- See the [FAQ](../FAQ.md) for common questions
- Review the [Roadmap](../ROADMAP.md) for upcoming features
- Consider [contributing](../CONTRIBUTING.md) to the project!

## Support

- 💬 [GitHub Discussions](https://github.com/fed-tts/fed-tts/discussions) — Ask questions
- 🐛 [GitHub Issues](https://github.com/fed-tts/fed-tts/issues) — Report bugs
- ☕ [Ko-fi](https://ko-fi.com/fedtts) — Support the project
- 📖 [Support Guide](../SUPPORT.md) — All support channels

---

*FED TTS — No AI, just deterministic tools that work.*
