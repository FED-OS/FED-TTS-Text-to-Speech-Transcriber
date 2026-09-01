# 🎙️ FED TTS - Complete File Tree for Supa Ninja AI

**Project:** FED TTS (Fluid Enhanced Dynamic Text-to-Speech)
**Description:** Transcriber + Read Aloud + Grammarly-clone. 100% Offline. Zero AI.
**Tech Stack:** Python + Streamlit
**License:** MIT

---

## 📁 Complete File Tree

```
fed-tts/
│
├── .github/
│   ├── DISCUSSION_WELCOME_README.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── FUNDING.yml
│   ├── CODEOWNERS
│   ├── dependabot.yml
│   ├── labeler.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   ├── custom.md
│   │   └── config.yml
│   └── workflows/
│       ├── build.yml
│       ├── test.yml
│       ├── ci.yml
│       ├── cd.yml
│       ├── deploy.yml
│       ├── release.yml
│       ├── publish.yml
│       ├── pr.yml
│       ├── stale.yml
│       ├── labeler.yml
│       ├── greetings.yml
│       ├── codeql.yml
│       ├── main.yml
│       ├── pages.yml
│       ├── dependency-review.yml
│       └── scorecards.yml
│
├── src/
│   └── fed_tts/
│       ├── __init__.py
│       ├── app.py
│       ├── transcriber.py
│       ├── grammar_checker.py
│       └── tts.py
│
├── tests/
│   ├── __init__.py
│   ├── test_app.py
│   ├── test_grammar_checker.py
│   └── test_transcriber.py
│
├── docs/
│   ├── index.md
│   ├── api.md
│   ├── architecture.md
│   └── quickstart.md
│
├── examples/
│   └── example_usage.md
│
├── prompts/
│   └── .gitkeep
│
├── wiki/
│   └── .gitkeep
│
├── discussion/
│   └── .gitkeep
│
├── CLAUDE.md
├── AGENTS.md
├── AUTHORS.md
├── MAINTAINERS.md
├── ADR.md
├── ROADMAP.md
├── DEPLOYMENT.md
├── BUILD.md
├── INSTALL.md
├── SUMMARY.md
├── todo.md
├── PRICING.md
├── COPYING.md
├── CITATIONS.md
├── GOVERNANCE.md
├── SUPPORT.md
├── CODE_OF_CONDUCT.md
├── README.md
├── CONTRIBUTING.md
├── usage.md
├── CHANGELOG.md
├── FAQ.md
├── NOTICE.md
├── SECURITY.md
├── LICENSE
├── .gitignore
├── .pre-commit-config.yaml
├── styles.css
├── social-image.png
├── app.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── environment.yml
├── Dockerfile
├── setup.sh
├── Procfile
└── MANIFEST.in
```

---

## 📋 Build Instructions for Supa Ninja AI

### Core Application Files

#### `app.py` (Main Streamlit App)
- Privacy-first Streamlit app with 100% offline functionality
- File upload (MP3, WAV, M4A, FLAC, OGG) via `st.file_uploader`
- Audio playback via `st.audio` with native player
- Manual transcription text area with `st.session_state` persistence
- Grammarly clone: `pyspellchecker` (dictionary) + regex rules (grammar)
- Read aloud: Browser's native `SpeechSynthesis` API via `st.components.v1.html`
- Custom CSS loading from `styles.css`
- **NO AI/ML, NO cloud APIs, NO external TTS services**

#### `src/fed_tts/transcriber.py`
- Manual transcription workspace logic
- Audio playback control helpers
- Session state management for transcripts

#### `src/fed_tts/grammar_checker.py`
- Dictionary-based spell checking (`pyspellchecker`)
- Regex-based grammar rules:
  - "would of" → "would have"
  - "could of" → "could have"
  - Double space detection
  - Passive voice detection (`was ... by`)
  - Long sentence detection (>25 words)

#### `src/fed_tts/tts.py`
- Browser SpeechSynthesis API integration
- Voice selection, rate, and pitch controls
- Pure JavaScript injection (no cloud TTS)

### Configuration Files

#### `pyproject.toml`
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "fed-tts"
version = "0.1.0"
description = "Transcriber + Read Aloud + Grammarly-clone. 100% Offline. Zero AI."
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "streamlit>=1.29.0",
    "pyspellchecker>=0.7.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "ruff>=0.1.0",
    "black>=23.0",
    "mypy>=1.0",
    "flake8>=6.0",
]

[tool.ruff]
line-length = 88
target-version = "py38"

[tool.black]
line-length = 88
target-version = ['py38']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true
```

#### `requirements.txt`
```
streamlit>=1.29.0
pyspellchecker>=0.7.0
```

#### `requirements-dev.txt`
```
pytest>=7.0
pytest-cov>=4.0
ruff>=0.1.0
black>=23.0
mypy>=1.0
flake8>=6.0
pre-commit>=3.0
```

#### `.pre-commit-config.yaml`
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.0.0
    hooks:
      - id: black
        language_version: python3
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
```

#### `.gitignore`
```
# Python
__pycache__/
*.py[cod]
*.so
.Python
env/
venv/
.venv/
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/
*.egg-info/
dist/
build/

# Streamlit
.streamlit/secrets.toml
.streamlit/cache/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
uploads/
temp/
data/
*.log
```

### GitHub Configuration Files

#### `.github/FUNDING.yml`
```yaml
github: [your-github-username]
ko_fi: YOUR_USERNAME
custom: ["https://ko-fi.com/YOUR_USERNAME"]
```

#### `.github/CODEOWNERS`
```
* @your-github-username
```

#### `.github/dependabot.yml`
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

#### `.github/labeler.yml`
```yaml
'type: documentation':
  - '**/*.md'
  - 'docs/**/*'
'type: ci-cd':
  - '.github/**/*'
  - '.github/workflows/**/*'
'type: core':
  - 'app.py'
  - 'src/**/*'
'type: dependencies':
  - 'requirements.txt'
  - 'pyproject.toml'
  - 'setup.py'
```

### Key Documentation Files

#### `README.md` (Include Ko-fi button)
```markdown
# 🎙️ FED TTS - Fluid Enhanced Dynamic Text-to-Speech

**Transcriber + Read Aloud + Grammarly-clone. 100% Offline. Zero AI.**

[Include: Features, Quick Start, Requirements, Contributing, License, Ko-fi button]

## 💖 Support the Project
<a href='https://ko-fi.com/YOUR_USERNAME' target='_blank'>
    <img height='36' style='border:0px;height:36px;' src='https://ko-fi.com/img/githubbutton_sm.svg' border='0' alt='Buy Me a Coffee at ko-fi.com' />
</a>
```

### GitHub Actions Workflows (16 total)

1. **build.yml** - Build smoke test across Python versions
2. **test.yml** - Run pytest with coverage, upload to Codecov
3. **ci.yml** - Lint (flake8) + format check (black) + tests
4. **cd.yml** - Continuous deployment on tags (PyPI)
5. **deploy.yml** - Deploy to Streamlit Cloud
6. **release.yml** - Auto-create GitHub releases on tags
7. **publish.yml** - Publish to PyPI on release
8. **pr.yml** - PR validation + Conventional Commits check
9. **stale.yml** - Auto-close stale issues (60d) and PRs (30d)
10. **labeler.yml** - Auto-label PRs based on changed files
11. **greetings.yml** - Welcome new contributors
12. **codeql.yml** - Security analysis with CodeQL
13. **main.yml** - Main CI/CD pipeline (lint, test, build, artifact)
14. **pages.yml** - Deploy docs to GitHub Pages
15. **dependency-review.yml** - Review dependency changes for vulnerabilities
16. **scorecards.yml** - OpenSSF Scorecards security analysis

### Issue Templates (3)
- **bug_report.md** - Bug report with environment details
- **feature_request.md** - Feature request template
- **custom.md** - General questions/discussions
- **config.yml** - Disable blank issues, link to discussions

### Documentation Files (20+)
- CLAUDE.md - AI agent instructions for the project
- AGENTS.md - Agent responsibilities and guidelines
- AUTHORS.md - Project authors
- MAINTAINERS.md - Maintainer list and responsibilities
- ADR.md - Architecture Decision Records
- ROADMAP.md - Project roadmap (v0.1.0 → v1.0.0)
- DEPLOYMENT.md - Deployment guide (local, Streamlit Cloud, Docker, Heroku)
- BUILD.md - Build instructions (PyInstaller, PyPI)
- INSTALL.md - Installation guide with ffmpeg instructions
- SUMMARY.md - Executive summary
- todo.md - Project todo list
- PRICING.md - Free and open source, Ko-fi support
- COPYING.md - MIT License copying details
- CITATIONS.md - How to cite the project (APA, BibTeX)
- GOVERNANCE.md - Project governance model
- SUPPORT.md - Support channels and response times
- CODE_OF_CONDUCT.md - Contributor Covenant
- CONTRIBUTING.md - Contribution guidelines
- usage.md - Usage guide
- CHANGELOG.md - Version history
- FAQ.md - Frequently asked questions
- NOTICE.md - Copyright and third-party notices
- SECURITY.md - Security policy and vulnerability reporting

### Styles
#### `styles.css`
- Custom Streamlit theme
- Color scheme: #f8f9fa background, #2c3e50 headers, #4a6fa5 buttons
- Custom text area styling with monospace font
- Button hover effects with box shadows
- Alert styling with left border

### Other Assets
- **social-image.png** - 1280x640 social preview image
- **Dockerfile** - Container build for deployment
- **environment.yml** - Conda environment alternative
- **Procfile** - Heroku deployment config
- **setup.sh** - Streamlit Cloud setup script
- **MANIFEST.in** - Package data files

---

## 🎯 Key Design Principles

1. **No AI/ML** - Use only deterministic algorithms (regex, dictionary lookups, native browser TTS)
2. **Privacy First** - No data leaves the user's machine, no cloud calls
3. **Simplicity** - Clean, well-documented codebase
4. **Open Source** - MIT licensed
5. **Offline** - Works without internet (except browser TTS which uses OS voices)

## 📝 Placeholders to Replace

- `YOUR_USERNAME` → Your Ko-fi username
- `your-github-username` → Your GitHub username
- `your-email@example.com` → Your contact email
- `[Your Name]` → Your actual name

---

**Ready for Supa Ninja AI to build! 🚀**
