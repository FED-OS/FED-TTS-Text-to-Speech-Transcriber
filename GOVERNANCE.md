# 🏛️ FED TTS - Governance Model

## Overview

FED TTS is an open-source project governed by its maintainers and contributors. This document outlines how decisions are made and how the community can participate.

## Roles

### Lead Maintainer
- Responsible for overall project direction and vision
- Makes final decisions on major changes
- Manages releases and versioning
- Ensures project health and sustainability
- Enforces the Code of Conduct

### Maintainers
- Review and merge pull requests
- Triage and respond to issues
- Help shape the roadmap
- Mentor new contributors
- Ensure code quality and adherence to project standards

### Contributors
- Anyone who submits a pull request
- Propose improvements via issues and discussions
- Participate in community discussions
- Help with documentation and testing

### Community Members
- Anyone who uses FED TTS
- Report bugs and request features
- Participate in discussions
- Help others in the community

## Decision-Making Process

### Minor Changes
- Can be merged by any maintainer after review
- No formal discussion required
- Examples: Bug fixes, documentation updates, minor feature additions, grammar rule additions

### Major Changes
- Requires consensus among maintainers
- Must be discussed via GitHub issue or discussion before implementation
- Examples: New major features, UI redesigns, significant architecture changes

### Breaking Changes
- Requires community consultation via GitHub Discussions
- Must be documented in CHANGELOG.md
- Must provide migration guide if needed
- Examples: API changes, dependency updates that affect behavior, removal of features

## Key Principle: NO AI

All decisions must adhere to the core principle of FED TTS being **100% AI-free**. Any proposal that introduces AI/ML, cloud-based AI APIs, or neural networks will be rejected. This is a non-negotiable aspect of the project.

## Community Participation

### GitHub Discussions
- For questions, ideas, and general conversation
- Categories: Ideas, Q&A, Announcements, Show and Tell, General

### GitHub Issues
- For bug reports and feature requests
- Use the appropriate template
- Include all requested information

### Pull Requests
- For code contributions
- Follow the PR template
- Ensure all checks pass

## Release Process

1. Update `CHANGELOG.md` with all changes
2. Bump version in `pyproject.toml`
3. Create a release PR
4. After merge, create a new tag: `git tag -a vX.X.X -m "Release vX.X.X"`
5. Push tag: `git push origin vX.X.X`
6. GitHub Actions will automatically create the release and publish to PyPI
7. Update documentation if needed

### Versioning

FED TTS follows [Semantic Versioning](https://semver.org/):
- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (0.X.0): New features, backward compatible
- **PATCH** (0.0.X): Bug fixes, backward compatible

## Code of Conduct

All participants must follow our [Code of Conduct](CODE_OF_CONDUCT.md). Violations should be reported to [your-email@example.com].

## Funding

- The project is volunteer-driven
- Donations via [Ko-fi](https://ko-fi.com/YOUR_USERNAME) support development
- All funding goes to project maintenance and development
- No funding influences project direction or decisions

## How to Become a Maintainer

Contributors who consistently provide high-quality PRs, engage in code reviews, and participate in discussions may be invited to become maintainers. The Lead Maintainer makes this decision based on:

1. Quality and consistency of contributions
2. Understanding of the project's principles (especially "No AI")
3. Community engagement and helpfulness
4. Technical competence

## Contact

- **Lead Maintainer:** [Your Name] ([your-email@example.com])
- **GitHub:** [https://github.com/your-github-username/fed-tts](https://github.com/your-github-username/fed-tts)
- **Discussions:** [GitHub Discussions](https://github.com/your-github-username/fed-tts/discussions)
