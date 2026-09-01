# 🏗️ Building FED TTS

## Build for Development

### Prerequisites

- Python 3.8+
- Git
- Virtual environment (recommended)

### Setup

```bash
# Clone the repository
git clone https://github.com/your-github-username/fed-tts.git
cd fed-tts

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run the app
streamlit run app.py
```

## Build for Distribution

### PyInstaller (Standalone Executable)

```bash
# Install PyInstaller
pip install pyinstaller

# Build the executable
pyinstaller --onefile --windowed --name "FED TTS" app.py

# Output: dist/FED TTS.exe (Windows) or dist/FED TTS (Linux/macOS)
```

### PyInstaller with Custom Icon

```bash
pyinstaller --onefile --windowed --icon=icon.ico --name "FED TTS" app.py
```

### PyInstaller with All Data Files

```bash
pyinstaller --onefile --windowed \
    --add-data "styles.css:." \
    --add-data "src:src" \
    --name "FED TTS" \
    app.py
```

## Build for PyPI (Python Package)

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Check the package
twine check dist/*

# Upload to Test PyPI (for testing)
twine upload --repository testpypi dist/*

# Upload to PyPI (production)
twine upload dist/*
```

## Continuous Integration (GitHub Actions)

The `.github/workflows/` directory contains all CI/CD configurations:

- **build.yml**: Build smoke test across Python versions
- **test.yml**: Run pytest with coverage
- **ci.yml**: Lint + format check + tests
- **cd.yml**: Continuous deployment on tags
- **release.yml**: Auto-create GitHub releases on tags
- **publish.yml**: Publish to PyPI on release
- **codeql.yml**: Security analysis
- **scorecards.yml**: OpenSSF Scorecards analysis

Builds are automatically triggered on:
- Push to `main` branch
- Pull requests to `main`
- Tag pushes (for releases)

## Docker Build

```bash
# Build image
docker build -t fed-tts .

# Run container
docker run -p 8501:8501 fed-tts

# Run with volume mount for file access
docker run -p 8501:8501 -v $(pwd)/data:/app/data fed-tts
```

## Troubleshooting

### Issue: ffmpeg not found
**Solution:**
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org) and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

### Issue: Streamlit not found
**Solution:**
```bash
pip install streamlit==1.29.0
```

### Issue: PyInstaller build fails
**Solution:** Make sure all data files are included with `--add-data`:
```bash
pyinstaller --onefile --windowed \
    --add-data "styles.css:." \
    --add-data "src/fed_tts:src/fed_tts" \
    --name "FED TTS" \
    app.py
```

### Issue: Tests fail
**Solution:** Make sure dev dependencies are installed:
```bash
pip install -r requirements-dev.txt
pytest tests/
```

### Issue: Pre-commit hooks fail
**Solution:** Run the formatters:
```bash
black .
isort .
flake8 .
```
