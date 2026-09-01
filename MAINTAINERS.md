# 🔧 FED TTS Maintainers

## Current Maintainers

| Name | Role | GitHub | Focus Area |
|------|------|--------|------------|
| [Your Name] | Lead Maintainer | [@your-github-username](https://github.com/your-github-username) | Overall project, core features, releases |

## Responsibilities of Maintainers

### 1. Review and Merge Pull Requests
- Ensure code quality and adherence to project guidelines
- Verify the "No AI" principle is maintained
- Check that tests pass and code is formatted
- Provide constructive feedback

### 2. Triage Issues
- Label issues appropriately (bug, enhancement, question, etc.)
- Assign priorities (high, medium, low)
- Respond to questions within 24-72 hours
- Close resolved issues

### 3. Manage Releases
- Update CHANGELOG.md
- Bump version in pyproject.toml
- Create and publish versioned releases
- Write release notes

### 4. Maintain Documentation
- Keep README, docs, and wiki up to date
- Ensure INSTALL.md and BUILD.md are accurate
- Update FAQ.md with new questions

### 5. Community Management
- Foster a welcoming and inclusive community
- Enforce the Code of Conduct
- Welcome new contributors
- Respond to discussions

## How to Become a Maintainer

Contributors who consistently provide high-quality PRs, engage in code reviews, and participate in discussions may be invited to become maintainers.

### Criteria
1. Made at least 5 merged pull requests
2. Demonstrated understanding of the "No AI" principle
3. Active in community discussions for at least 3 months
4. Helpful and respectful to community members
5. Technical competence in Python and Streamlit

## Maintainer Communication

- **GitHub Discussions**: For project-related discussions
- **GitHub Issues**: For bug reports and feature requests
- **Email**: For private matters (security, conduct violations)

## Release Process

1. Update `CHANGELOG.md` with all changes since the last release
2. Bump version in `pyproject.toml`
3. Create a release PR with the changes
4. After the PR is reviewed and merged:
   ```bash
   git tag -a vX.X.X -m "Release vX.X.X"
   git push origin vX.X.X
   ```
5. GitHub Actions will automatically:
   - Create a GitHub Release with auto-generated notes
   - Build and publish the package to PyPI
6. Update documentation if needed
7. Announce the release in GitHub Discussions

## Maintainer Guidelines

### When Reviewing PRs
- ✅ Check that the "No AI" principle is maintained
- ✅ Verify tests pass
- ✅ Check code formatting (black, flake8)
- ✅ Ensure documentation is updated
- ✅ Provide constructive, kind feedback
- ✅ Approve and merge when ready

### When Triageing Issues
- ✅ Use appropriate labels
- ✅ Assign to the right person
- ✅ Respond promptly
- ✅ Close stale issues
- ✅ Convert discussions to issues when appropriate

### Code Standards
- Follow PEP 8
- Use black for formatting
- Use flake8 for linting
- Write docstrings for all functions
- Add tests for new features
