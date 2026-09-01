# Security Policy

## Supported Versions

We actively support the latest release of FED TTS.

| Version | Supported          |
|---------|--------------------|
| 0.1.x   | ✅ Current release |
| < 0.1   | ❌ Not supported   |

## Reporting a Vulnerability

Please **do not** report security vulnerabilities through public GitHub issues. Instead, please report them via email to [your-email@example.com].

### What to Include in Your Report

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 5 business days
- **Fix Release**: Depends on severity, typically within 30 days for high severity

## Privacy & Security Features

FED TTS is designed with privacy as a top priority:

- ✅ **No data collection** - The app does not collect any user data
- ✅ **No cloud calls** - All processing happens locally
- ✅ **No telemetry** - No usage analytics or tracking
- ✅ **No external APIs** - No calls to third-party services
- ✅ **Offline capable** - Works without internet (except browser TTS which uses OS voices)

## Security Best Practices for Users

1. **Keep your dependencies updated**: Run `pip install --upgrade -r requirements.txt` regularly
2. **Use a virtual environment**: Isolate FED TTS from your system Python
3. **Review code before running**: FED TTS is open source—review the code yourself
4. **Run locally**: Always run FED TTS on your local machine for maximum privacy
