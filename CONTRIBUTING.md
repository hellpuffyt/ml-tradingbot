# Contributing to ML Trading Bot

Thank you for your interest in contributing! We welcome contributions from the community. Please follow these guidelines to ensure smooth collaboration.

---

## Types of Contributions

- 🐛 **Bug Reports** - Report issues and errors
- ✨ **Features** - Add new functionality
- 📚 **Documentation** - Improve docs and examples
- 🧪 **Tests** - Add test coverage
- 🔧 **Improvements** - Code optimization and refactoring

---

## Getting Started

### 1. Fork the Repository
```bash
# Go to GitHub and click "Fork"
git clone https://github.com/YOUR_USERNAME/ml-trading-bot.git
cd ml-trading-bot
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-name
```

Branch naming convention:
- `feature/add-macd-indicator` ✅
- `fix/sentiment-analysis-bug` ✅
- `docs/improve-readme` ✅
- `test/add-unit-tests` ✅

### 3. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies with dev tools
pip install -r requirements.txt
pip install pytest black flake8 mypy
```

---

## Making Changes

### Code Style
- Follow **PEP 8** guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep lines under 100 characters

### Code Format
```bash
# Format code with black
black tradingbot.py

# Check for style issues
flake8 tradingbot.py

# Type checking
mypy tradingbot.py
```

### Commit Messages
Follow conventional commit format:

```bash
git commit -m "feat: add stop-loss optimization"
git commit -m "fix: resolve sentiment analysis timeout"
git commit -m "docs: update README with examples"
git commit -m "test: add backtesting unit tests"
```

Good commit messages:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `chore:` Maintenance

### Testing

Write tests for new features:
```python
# tests/test_sentiment.py
def test_positive_sentiment():
    probability, sentiment = estimate_sentiment(
        ["Great news about the company!"]
    )
    assert sentiment == "positive"
    assert probability > 0.9
```

Run tests:
```bash
pytest tests/ -v
```

---

## Making a Pull Request

### Before Submitting
- [ ] Code follows PEP 8 style
- [ ] All tests pass (`pytest`)
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No API keys or credentials added
- [ ] Branch is up to date with main

### PR Description Template
```markdown
## Description
Brief description of your changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update

## Related Issues
Fixes #123

## Changes Made
- Change 1
- Change 2

## Testing
How to test the changes:
1. Step 1
2. Step 2

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] My code follows PEP 8 style
- [ ] Tests pass locally
- [ ] No new warnings generated
- [ ] Documentation updated
```

### Submit Your PR
1. Push to your fork
```bash
git push origin feature/your-feature-name
```

2. Go to GitHub and create a Pull Request
3. Add descriptive title and description
4. Link related issues
5. Wait for review

---

## Code Review Process

Our team will review your PR and may:
- Request changes
- Ask clarifying questions
- Suggest improvements
- Approve and merge

Please be patient and open to feedback! 🙂

---

## Feature Requests

Have an idea? Create an issue with:

```markdown
# Feature Request

## Description
What should the feature do?

## Use Case
Why is this useful?

## Example
How would users interact with it?

## Possible Implementation
Any ideas on how to implement it?
```

---

## Bug Reports

Found a bug? Report it with:

```markdown
# Bug Report

## Description
What's the issue?

## Steps to Reproduce
1. Step 1
2. Step 2

## Expected Behavior
What should happen?

## Actual Behavior
What actually happens?

## Environment
- OS: Windows/Mac/Linux
- Python: 3.13
- GPU: Yes/No

## Error Message
[Include full error trace]

## Workaround (if any)
Any temporary solutions?
```

---

## Documentation Contributions

### Update README.md
- Add new features to the tech stack section
- Include examples for new functionality
- Update architecture diagram if needed

### Add Code Comments
```python
def estimate_sentiment(news):
    """
    Analyze sentiment of financial news using FinBERT.
    
    Args:
        news (list): List of news headlines to analyze
        
    Returns:
        tuple: (probability (float), sentiment (str))
            probability: Confidence score 0.0-1.0
            sentiment: "positive", "negative", or "neutral"
    """
```

---

## Development Roadmap

Check [Issues](https://github.com/yourusername/ml-trading-bot/issues) for planned features:
- Machine learning model improvements
- More indicators
- Portfolio optimization
- Cloud deployment

---

## Community Guidelines

- **Respectful** - Be kind and professional
- **Collaborative** - Help each other succeed
- **Transparent** - Communicate openly
- **Inclusive** - Welcome all backgrounds

---

## Questions?

- 📧 Email: contributors@example.com
- 💬 GitHub Discussions: [Ask here](https://github.com/yourusername/ml-trading-bot/discussions)
- 🐦 Twitter: [@YourHandle](https://twitter.com)

---

## Recognition

Contributors will be:
- Listed in README.md
- Credited in release notes
- Added to CONTRIBUTORS.md

---

Thank you for helping make this project better! 🙏✨
