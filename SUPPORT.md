# 🆘 FED TTS - Support

## Where to Get Help

### 📚 Documentation

Start here:
- [README.md](README.md) – Main overview and quick start
- [INSTALL.md](INSTALL.md) – Detailed installation guide
- [usage.md](usage.md) – How to use the app
- [FAQ.md](FAQ.md) – Frequently asked questions
- [docs/](docs/) – Full documentation

### 💬 GitHub Discussions

[Join the community!](https://github.com/your-github-username/fed-tts/discussions)

- **💡 Ideas** – Share feature requests and improvement suggestions
- **❓ Q&A** – Ask for help with installation, configuration, or usage
- **📢 Announcements** – Stay updated on project news and releases
- **🎯 Show and Tell** – Share what you've built with FED TTS
- **🤝 General** – For everything else

### 🐛 GitHub Issues

[Report bugs or request features](https://github.com/your-github-username/fed-tts/issues)

- Bug reports (use the bug report template)
- Feature requests (use the feature request template)
- General questions (use the custom issue template)

### 💰 Priority Support

If you need personalized or priority support:

1. [Buy me a coffee](https://ko-fi.com/YOUR_USERNAME) and mention your issue
2. For enterprise support, contact [your-email@example.com]

## Self-Help Resources

### Common Issues

**Issue:** Audio player doesn't work
- **Solution:** Ensure you're using a supported browser (Chrome, Firefox, Edge, Safari). Check that your audio file format is supported (MP3, WAV, M4A, FLAC, OGG).

**Issue:** TTS doesn't speak
- **Solution:**
  1. Check your system volume
  2. Check browser permissions for audio
  3. Make sure your OS has TTS voices installed
  4. Try clicking "Stop" first, then "Speak Now" again

**Issue:** Spelling checker not working
- **Solution:** Make sure pyspellchecker is installed:
  ```bash
  pip install pyspellchecker
  ```

**Issue:** App crashes on large files
- **Solution:** Try compressing the audio file or using a smaller sample. You can also increase the upload limit in `.streamlit/config.toml`:
  ```toml
  [server]
  maxUploadSize = 500
  ```

**Issue:** "ModuleNotFoundError" on startup
- **Solution:** Install all dependencies:
  ```bash
  pip install -r requirements.txt
  ```

**Issue:** Port 8501 already in use
- **Solution:** Use a different port:
  ```bash
  streamlit run app.py --server.port 8502
  ```

### Error Messages

If you see an error, please:
1. Copy the full error message
2. Note your environment (OS, Python version, browser)
3. Include steps to reproduce
4. Open a [GitHub issue](https://github.com/your-github-username/fed-tts/issues/new/choose)

## Response Times

| Method | Response Time |
|--------|---------------|
| GitHub Discussions | 24-48 hours |
| GitHub Issues | 24-72 hours |
| Email (Enterprise) | 12-24 hours |
| Ko-fi Priority | 6-12 hours |

## Community Guidelines

When seeking support:
- ✅ Be respectful and inclusive
- ✅ Search before asking (your question may already be answered)
- ✅ Provide as much detail as possible
- ✅ Include screenshots and error logs
- ✅ Use the appropriate template
- ✅ Mark your issue as resolved when fixed

- ❌ Don't spam or cross-post
- ❌ Don't demand immediate responses
- ❌ Don't share sensitive information publicly

## Contributing

Want to help others? You can:
- Answer questions in GitHub Discussions
- Help triage issues
- Improve documentation
- Write tutorials
- Share your use cases

See [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

## 💖 Support the Project

<a href='https://ko-fi.com/YOUR_USERNAME' target='_blank'>
    <img height='36' style='border:0px;height:36px;' src='https://ko-fi.com/img/githubbutton_sm.svg' border='0' alt='Buy Me a Coffee at ko-fi.com' />
</a>
