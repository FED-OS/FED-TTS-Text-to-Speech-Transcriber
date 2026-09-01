# Contributing to FED TTS

We love your input! We want to make contributing to this project as easy and transparent as possible.

## 🛠️ Development Process

1. Fork the repo and create your branch from `main`
2. If you've added code, add comments explaining the logic
3. Ensure the code passes linting (`flake8 .`) and formatting (`black .`)
4. Ensure tests pass (`pytest tests/`)
5. Issue a pull request!

## 🐛 Report Bugs Using GitHub's Issue Tracker

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/your-github-username/fed-tts/issues/new/choose).

### Write Bug Reports with Detail

Great Bug Reports tend to have:

- A quick summary
- Steps to reproduce
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening)
- Environment details (OS, Python version, Streamlit version, browser)

## 💡 Suggest Enhancements

Open a [feature request issue](https://github.com/your-github-username/fed-tts/issues/new/choose) with:

- A clear description of the problem you're trying to solve
- The solution you'd like to see
- Any alternatives you've considered

## 🔒 Key Principle: NO AI

FED TTS is built on the principle of being **100% AI-free**. All contributions must adhere to this:

- ❌ No neural networks or deep learning models
- ❌ No cloud-based AI APIs (OpenAI, Google Cloud AI, etc.)
- ❌ No LLMs for grammar correction
- ✅ Dictionary-based spell checking (pyspellchecker)
- ✅ Regex-based grammar rules
- ✅ Browser's native SpeechSynthesis API for TTS
- ✅ Manual transcription (human-in-the-loop)
- ✅ Everything runs locally, 100% offline

## 📋 Coding Standards

- Use 4 spaces for indentation
- Use descriptive variable names
- Keep functions small and focused
- Write docstrings for all functions and classes
- Follow PEP 8 (enforced by flake8)
- Format with black (line length 88)
- Add tests for new functionality

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_grammar_checker.py
```

## 📝 Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Build process, dependencies, etc.

Example: `feat: add repeated word detection to grammar checker`

## 🔄 Pull Request Process

1. Update the [CHANGELOG.md](CHANGELOG.md) with details of changes
2. Update documentation if needed
3. Ensure all tests pass and code is formatted
4. The PR will be reviewed by maintainers
5. Once approved, your PR will be merged

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to FED TTS! 🎙️
