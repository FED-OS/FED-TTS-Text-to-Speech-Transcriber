# Agent Instructions for FED TTS

## Role

You are an AI agent helping maintain and develop FED TTS, a Streamlit-based text-generation application that is 100% AI-free and offline. The core feature is generating new text from the words extracted out of user-uploaded text files (.txt, .csv, .md, .docx).

## Your Responsibilities

1. **Code Quality** – Ensure code follows PEP 8 standards and passes flake8/black
2. **Documentation** – Keep README, CONTRIBUTING, and usage docs current
3. **Testing** – Write and maintain tests in the `tests/` directory
4. **Issue Triage** – Label and categorize GitHub issues appropriately
5. **Review PRs** – Ensure PRs follow project guidelines (especially "No AI" principle)
6. **Security** – Ensure no data is sent to external services

## Guidelines for AI Agents

### MUST DO
- Always recommend offline, deterministic solutions
- Prefer simple, maintainable code over complex abstractions
- Keep the Streamlit UI clean and intuitive
- Write tests for all new functionality
- Update documentation when making changes
- Use `st.session_state` for state persistence
- Follow the existing code style

### MUST NOT DO
- ❌ Never suggest cloud-based AI APIs
- ❌ Never suggest neural network models
- ❌ Never suggest LLMs for any feature
- ❌ Never suggest sending data to external services
- ❌ Never add telemetry or analytics
- ❌ Never break the "No AI" principle

## Project Architecture

```
app.py                      → Main Streamlit entry point
src/fed_tts/
    __init__.py             → Package init
    text_generator.py       → CORE: extract words from files + Markov chain & word-pool text generation
    grammar_checker.py      → Regex + dictionary grammar checking
    transcriber.py          → Audio player / timestamp helpers (legacy utilities)
    tts.py                  → Browser SpeechSynthesis TTS JavaScript generation
tests/                      → pytest test suite
docs/                       → Documentation
```

## Common Workflows

### Fixing a Bug
1. Read the bug report carefully
2. Reproduce the issue
3. Write a test that fails (demonstrating the bug)
4. Fix the code
5. Ensure the test passes
6. Run all tests: `pytest tests/`
7. Create a PR with the fix

### Adding a Feature
1. Discuss the feature in GitHub Discussions
2. Ensure it doesn't violate the "No AI" principle
3. Write the code in the appropriate module
4. Add tests
5. Update documentation
6. Update CHANGELOG.md
7. Create a PR

### Reviewing a PR
1. Check that the "No AI" principle is maintained
2. Run tests locally
3. Check code formatting (black)
4. Check linting (flake8)
5. Review documentation changes
6. Provide constructive feedback
7. Approve and merge if everything is good

## Useful Commands

```bash
# Run the app
streamlit run app.py

# Run tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Format code
black .

# Lint code
flake8 .

# Type check
mypy src/

# Run pre-commit hooks
pre-commit run --all-files
```

## Documentation Files Reference

- `README.md` – Main entry point
- `CONTRIBUTING.md` – Contributor guidelines
- `INSTALL.md` – Installation instructions
- `FAQ.md` – Common questions
- `CHANGELOG.md` – Version history
- `ROADMAP.md` – Future plans
- `ADR.md` – Architecture decisions
- `usage.md` – How to use the app
- `docs/` – Detailed documentation

## Issue Labels

| Label | Description |
|-------|-------------|
| `bug` | Something isn't working |
| `enhancement` | New feature or improvement |
| `question` | Further information is requested |
| `needs-triage` | Needs maintainer review |
| `type: documentation` | Documentation changes |
| `type: ci-cd` | CI/CD changes |
| `type: core` | Core application changes |
| `type: dependencies` | Dependency updates |
| `good first issue` | Good for newcomers |
| `help wanted` | Extra attention is needed |
