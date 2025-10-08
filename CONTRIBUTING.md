# Contributing Guidelines

## Welcome Contributors! 🎉

Thank you for your interest in contributing to LinguaStream! This document provides comprehensive guidelines for contributing to our real-time offline audio translation system.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Workflow](#contribution-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Standards](#documentation-standards)
- [Issue Reporting](#issue-reporting)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors. Please:

- **Be respectful** and constructive in all interactions
- **Be patient** with newcomers and questions
- **Be collaborative** and help others learn
- **Be professional** in all communications
- **Be inclusive** and welcoming to diverse perspectives

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Personal attacks or trolling
- Spam or off-topic discussions
- Sharing private information without permission
- Any conduct that creates an unwelcoming environment

## Getting Started

### Prerequisites

- Python 3.8+ development environment
- Git version control
- Basic understanding of audio processing and machine learning
- Familiarity with Persian (Farsi) and English languages

### Areas for Contribution

We welcome contributions in the following areas:

#### 🎯 High Priority
- **Performance Optimization**: Reduce latency and memory usage
- **Model Integration**: Add support for new STT/TTS models
- **Audio Quality**: Improve audio preprocessing and postprocessing
- **Error Handling**: Enhance robustness and error recovery
- **Testing**: Expand test coverage and add integration tests

#### 🔧 Medium Priority
- **Multi-language Support**: Add support for Arabic, Turkish, etc.
- **GUI Development**: Create user-friendly interface
- **Mobile Support**: Optimize for mobile platforms
- **Cloud Integration**: Add optional cloud processing
- **API Development**: Create REST API for external integration

#### 🚀 Future Features
- **Lip-sync Integration**: Real-time facial animation
- **Video Processing**: Multi-modal translation
- **Voice Cloning**: Custom voice synthesis
- **Edge Computing**: IoT and embedded deployment

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/yourusername/LinguaStream.git
cd LinguaStream

# Add upstream remote
git remote add upstream https://github.com/originalowner/LinguaStream.git
```

### 2. Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Pre-commit Hooks

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### 4. IDE Configuration

#### VS Code Settings

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"]
}
```

#### PyCharm Configuration

1. Open project in PyCharm
2. Configure Python interpreter to use virtual environment
3. Enable code inspection and formatting
4. Configure pytest as test runner

## Contribution Workflow

### 1. Issue First Approach

Before starting work on a feature or bug fix:

1. **Check existing issues** to avoid duplication
2. **Create a new issue** describing the problem or feature
3. **Wait for maintainer approval** before starting work
4. **Assign yourself** to the issue

### 2. Branch Strategy

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Or bugfix branch
git checkout -b bugfix/issue-number-description

# Or hotfix branch
git checkout -b hotfix/critical-issue
```

### 3. Development Process

```bash
# Make changes
# Test your changes
python -m pytest tests/

# Commit changes
git add .
git commit -m "feat: add new feature description"

# Push to your fork
git push origin feature/your-feature-name
```

### 4. Pull Request

1. **Create Pull Request** from your fork to main repository
2. **Fill out PR template** completely
3. **Link related issues** using keywords (fixes #123)
4. **Request review** from maintainers
5. **Address feedback** promptly

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

```python
# Use Black for formatting
black --line-length 88 src/ tests/

# Use isort for import sorting
isort src/ tests/

# Use flake8 for linting
flake8 src/ tests/
```

### Code Style Examples

#### Good Practices

```python
# Type hints
def transcribe(self, audio_data: np.ndarray) -> str:
    """Transcribe audio data to Persian text.
    
    Args:
        audio_data: Audio chunk as numpy array
        
    Returns:
        Transcribed Persian text
    """
    if audio_data is None or len(audio_data) == 0:
        return ""
    
    try:
        result = self.model.transcribe(audio_data, language="fa")
        return result["text"].strip()
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        return ""
```

#### Avoid These Patterns

```python
# Bad: No type hints, unclear variable names
def transcribe(audio):
    result = model.transcribe(audio)
    return result["text"]

# Bad: No error handling
def transcribe(self, audio_data):
    return self.model.transcribe(audio_data)["text"]

# Bad: No documentation
def transcribe(self, audio_data):
    return self.model.transcribe(audio_data)["text"]
```

### File Organization

```
src/
├── __init__.py
├── audio_handler.py      # Audio I/O operations
├── stt_engine.py         # Speech-to-text engine
├── translator.py         # Translation engine
├── tts_engine.py         # Text-to-speech engine
├── exceptions.py         # Custom exceptions
└── utils.py             # Utility functions

tests/
├── __init__.py
├── test_audio_handler.py
├── test_stt_engine.py
├── test_translator.py
├── test_tts_engine.py
└── integration/
    └── test_pipeline.py
```

## Testing Guidelines

### Test Structure

```python
# test_stt_engine.py
import pytest
import numpy as np
from src.stt_engine import STTEngine
from src.exceptions import ModelError

class TestSTTEngine:
    @pytest.fixture
    def stt_engine(self):
        return STTEngine()
    
    @pytest.fixture
    def sample_audio(self):
        # Generate test audio data
        return np.random.randint(-32768, 32767, 48000, dtype=np.int16)
    
    def test_transcribe_valid_audio(self, stt_engine, sample_audio):
        """Test transcription with valid audio data."""
        result = stt_engine.transcribe(sample_audio)
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_transcribe_empty_audio(self, stt_engine):
        """Test transcription with empty audio data."""
        empty_audio = np.array([])
        result = stt_engine.transcribe(empty_audio)
        assert result == ""
    
    def test_transcribe_none_input(self, stt_engine):
        """Test transcription with None input."""
        result = stt_engine.transcribe(None)
        assert result == ""
    
    @pytest.mark.performance
    def test_transcribe_latency(self, stt_engine, sample_audio):
        """Test transcription latency is within acceptable limits."""
        import time
        
        start_time = time.perf_counter()
        stt_engine.transcribe(sample_audio)
        end_time = time.perf_counter()
        
        latency = end_time - start_time
        assert latency < 0.5  # Should be under 500ms
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_stt_engine.py

# Run with coverage
pytest --cov=src tests/

# Run performance tests
pytest -m performance

# Run integration tests
pytest tests/integration/
```

### Test Data

```python
# tests/fixtures/audio_samples.py
import numpy as np

def create_silence_sample(duration_seconds=1, sample_rate=16000):
    """Create silence audio sample."""
    return np.zeros(int(duration_seconds * sample_rate), dtype=np.int16)

def create_tone_sample(frequency=440, duration_seconds=1, sample_rate=16000):
    """Create tone audio sample."""
    t = np.linspace(0, duration_seconds, int(duration_seconds * sample_rate))
    return (np.sin(2 * np.pi * frequency * t) * 32767).astype(np.int16)
```

## Documentation Standards

### Docstring Format

We use Google-style docstrings:

```python
def translate(self, text: str) -> str:
    """Translate Persian text to English.
    
    This method uses the Helsinki-NLP translation model to convert
    Persian text to English with high accuracy.
    
    Args:
        text: Persian text to translate
        
    Returns:
        Translated English text
        
    Raises:
        TranslationError: If translation fails
        
    Example:
        >>> translator = Translator()
        >>> result = translator.translate("سلام دنیا")
        >>> print(result)
        "Hello world"
    """
```

### README Updates

When adding new features, update relevant documentation:

1. **README.md**: Add feature description
2. **API.md**: Document new methods/classes
3. **ARCHITECTURE.md**: Update system diagrams
4. **PERFORMANCE.md**: Add performance metrics
5. **DEPLOYMENT.md**: Update installation instructions

### Code Comments

```python
# Good: Explain why, not what
# Use smaller chunk size for lower latency on slower hardware
chunk_size = 512 if cpu_cores < 4 else 1024

# Bad: Obvious comment
# Increment counter
counter += 1
```

## Issue Reporting

### Bug Reports

Use the bug report template:

```markdown
**Bug Description**
A clear description of the bug.

**Steps to Reproduce**
1. Go to '...'
2. Click on '....'
3. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g., Windows 10, Ubuntu 20.04]
- Python Version: [e.g., 3.10.0]
- LinguaStream Version: [e.g., 1.0.0]

**Additional Context**
Any other context about the problem.
```

### Feature Requests

Use the feature request template:

```markdown
**Feature Description**
A clear description of the feature.

**Use Case**
Describe the problem this feature would solve.

**Proposed Solution**
Describe your proposed solution.

**Alternatives**
Describe alternative solutions you've considered.

**Additional Context**
Any other context about the feature request.
```

## Pull Request Process

### PR Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or documented)

## Related Issues
Fixes #123
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests
2. **Code Review**: Maintainers review code quality
3. **Testing**: Manual testing on different environments
4. **Approval**: At least one maintainer approval required
5. **Merge**: Squash and merge to main branch

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number updated
- [ ] CHANGELOG.md updated
- [ ] Release notes prepared
- [ ] Tag created
- [ ] Release published

### Changelog Format

```markdown
## [1.1.0] - 2024-01-15

### Added
- Support for Arabic language translation
- GPU acceleration for Whisper model
- Real-time performance monitoring

### Changed
- Improved audio preprocessing pipeline
- Updated default model to Whisper Base

### Fixed
- Memory leak in TTS engine
- Audio synchronization issues
- Translation accuracy for short phrases
```

## Community Guidelines

### Getting Help

- **GitHub Discussions**: For questions and general discussion
- **Discord**: For real-time chat and support
- **Email**: For security issues and private matters

### Recognition

Contributors will be recognized in:
- **README.md**: Contributors section
- **Release Notes**: Feature acknowledgments
- **Documentation**: Code examples and tutorials

### Mentorship

We offer mentorship for:
- New contributors
- Complex feature development
- Code review guidance
- Technical architecture decisions

## Security

### Reporting Security Issues

For security vulnerabilities, please:

1. **DO NOT** create public issues
2. Email security@linguastream.dev
3. Include detailed reproduction steps
4. Allow 90 days for response before public disclosure

### Security Best Practices

- Never commit API keys or secrets
- Use environment variables for sensitive data
- Validate all user inputs
- Follow secure coding practices

## License

By contributing to LinguaStream, you agree that your contributions will be licensed under the MIT License.

## Contact

- **Maintainer**: [Your Name](mailto:maintainer@linguastream.dev)
- **Discord**: [Join our community](https://discord.gg/linguastream)
- **Website**: [linguastream.dev](https://linguastream.dev)

---

Thank you for contributing to LinguaStream! Together, we're building the future of real-time multilingual communication. 🌍✨
