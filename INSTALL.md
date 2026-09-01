# 📦 Installation Guide

## Quick Install

### Using pip

```bash
pip install streamlit pyspellchecker
```

### Cloning from GitHub

```bash
git clone https://github.com/your-github-username/fed-tts.git
cd fed-tts
pip install -r requirements.txt
```

## Detailed Installation Steps

### Step 1: Install Python

Download Python 3.8 or later from [python.org](https://python.org).

Verify installation:

```bash
python --version
# Should show: Python 3.8.x or higher
```

### Step 2: Install ffmpeg (Recommended for broader audio support)

**Windows:**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to a folder (e.g., `C:\ffmpeg`)
3. Add `C:\ffmpeg\bin` to your system PATH

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Linux (Fedora):**
```bash
sudo dnf install ffmpeg
```

**Linux (Arch):**
```bash
sudo pacman -S ffmpeg
```

Verify installation:
```bash
ffmpeg -version
```

### Step 3: Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv fed-tts-env

# Activate it
# Windows:
fed-tts-env\Scripts\activate
# macOS/Linux:
source fed-tts-env/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

For development:
```bash
pip install -r requirements-dev.txt
pre-commit install
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## Docker Installation (Optional)

### Build the image
```bash
docker build -t fed-tts .
```

### Run the container
```bash
docker run -p 8501:8501 fed-tts
```

Access at `http://localhost:8501`.

## Conda Installation (Optional)

```bash
# Create conda environment
conda env create -f environment.yml

# Activate
conda activate fed-tts

# Run
streamlit run app.py
```

## Post-Installation

1. Open your browser to `http://localhost:8501`
2. Upload an audio file (or type text directly)
3. Start transcribing!

## Common Issues

### Error: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Error: "No such file or directory: ffmpeg"
**Solution:** Install ffmpeg (see Step 2 above).

### Error: "Port 8501 is already in use"
**Solution:** Use a different port:
```bash
streamlit run app.py --server.port 8502
```

### Error: "SpeechSynthesis not working"
**Solution:** Make sure you're using a modern browser (Chrome, Firefox, Edge, Safari) and your OS has TTS voices installed.

### Error: "File too large"
**Solution:** Streamlit has a default upload limit. For large files, increase it in `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 500
```

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.8 | 3.10+ |
| RAM | 512 MB | 2 GB+ |
| Disk Space | 100 MB | 500 MB |
| Browser | Chrome 90+ | Latest Chrome/Firefox |
| OS | Windows 10 / macOS 10.14 / Ubuntu 18.04 | Latest OS version |
