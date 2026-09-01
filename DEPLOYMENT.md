# 🚀 Deployment Guide

## Local Deployment (Recommended)

### Option 1: Streamlit Run

```bash
streamlit run app.py
```

### Option 2: Production Server

```bash
pip install waitress
waitress-serve --port=8501 app:app
```

### Option 3: With Custom Configuration

Create `.streamlit/config.toml`:

```toml
[server]
port = 8501
address = "0.0.0.0"
maxUploadSize = 500
enableCORS = false
enableXsrfProtection = true
headless = true

[browser]
gatherUsageStats = false
```

```bash
streamlit run app.py
```

## Cloud Deployment

### Streamlit Community Cloud (Free)

1. Push your repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Connect your repository
5. Select the `main` branch and `app.py` as the entry point
6. Click "Deploy"

The app will be live at `https://your-username-fed-tts.streamlit.app`

### Docker Deployment

```bash
# Build the image
docker build -t fed-tts .

# Run the container
docker run -d -p 8501:8501 --name fed-tts-app fed-tts

# View logs
docker logs fed-tts-app

# Stop the container
docker stop fed-tts-app

# Remove the container
docker rm fed-tts-app
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  fed-tts:
    build: .
    ports:
      - "8501:8501"
    restart: unless-stopped
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
```

```bash
docker-compose up -d
```

### Heroku Deployment

1. Create a `Procfile` (already included):
   ```
   web: sh setup.sh && streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
   ```

2. Deploy via Heroku CLI:
   ```bash
   heroku create fed-tts-app
   git push heroku main
   heroku open
   ```

### Railway Deployment

1. Go to [railway.app](https://railway.app)
2. Create a new project from your GitHub repo
3. Railway will auto-detect the Dockerfile
4. Set the port to 8501
5. Deploy

### Render Deployment

1. Go to [render.com](https://render.com)
2. Create a new Web Service from your GitHub repo
3. Use the Dockerfile
4. Set port to 8501
5. Deploy

## Desktop Deployment (PyInstaller)

```bash
# Install PyInstaller
pip install pyinstaller

# Build for Windows
pyinstaller --onefile --windowed --name "FED TTS" --icon=icon.ico app.py

# Build for macOS
pyinstaller --onefile --windowed --name "FED TTS" app.py

# Build for Linux
pyinstaller --onefile --name "FED TTS" app.py
```

The executable will be in the `dist/` directory.

## Important Notes

- **No AI APIs**: Everything runs locally, no external dependencies for core functionality
- **Browser TTS**: Requires a modern browser with SpeechSynthesis support
- **Storage**: Files and transcripts stay on the user's machine
- **Privacy**: No data is sent to any server

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STREAMLIT_SERVER_PORT` | 8501 | Port to run the app on |
| `STREAMLIT_SERVER_ADDRESS` | 0.0.0.0 | Address to bind to |
| `STREAMLIT_SERVER_HEADLESS` | true | Run without opening browser |

## Health Check

The Docker image includes a health check endpoint:

```bash
curl http://localhost:8501/_stcore/health
# Should return: {"status": "ok"}
```

## Monitoring

For production deployments, consider monitoring:

- CPU and memory usage
- Response times
- Error rates
- Uptime

Tools like Prometheus, Grafana, or Uptime Robot can be used.
