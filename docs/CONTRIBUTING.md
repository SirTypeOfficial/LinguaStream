# راهنمای مشارکت

## خوش آمدید مشارکت‌کنندگان! 🎉

از علاقه شما به مشارکت در VoiceBridge متشکریم! این سند راهنمای جامعی برای مشارکت در سیستم ترجمه صوتی آفلاین همزمان ما ارائه می‌دهد.

## فهرست مطالب

- [کد رفتار](#کد-رفتار)
- [شروع کار](#شروع-کار)
- [راه‌اندازی توسعه](#راه‌اندازی-توسعه)
- [گردش کار مشارکت](#گردش-کار-مشارکت)
- [استانداردهای کدنویسی](#استانداردهای-کدنویسی)
- [راهنمای تست](#راهنمای-تست)
- [استانداردهای مستندسازی](#استانداردهای-مستندسازی)
- [گزارش مسائل](#گزارش-مسائل)
- [فرآیند Pull Request](#فرآیند-pull-request)
- [فرآیند انتشار](#فرآیند-انتشار)

## کد رفتار

### تعهد ما

ما متعهد به ارائه محیطی خوشامد و فراگیر برای تمام مشارکت‌کنندگان هستیم. لطفاً:

- **محترم باشید** و سازنده در تمام تعاملات
- **صبور باشید** با تازه‌کاران و سوالات
- **مشارکتی باشید** و به دیگران کمک کنید یاد بگیرند
- **حرفه‌ای باشید** در تمام ارتباطات
- **فراگیر باشید** و خوشامد به دیدگاه‌های متنوع

### رفتار غیرقابل قبول

- آزار و اذیت، تبعیض یا نظرات توهین‌آمیز
- حملات شخصی یا ترویل
- اسپم یا بحث‌های خارج از موضوع
- اشتراک اطلاعات خصوصی بدون اجازه
- هر رفتاری که محیطی ناخوشامد ایجاد کند

## شروع کار

### پیش‌نیازها

- محیط توسعه Python 3.8+
- کنترل نسخه Git
- درک پایه از پردازش صوتی و یادگیری ماشین
- آشنایی با زبان‌های فارسی و انگلیسی

### زمینه‌های مشارکت

ما از مشارکت در زمینه‌های زیر استقبال می‌کنیم:

#### 🎯 اولویت بالا
- **بهینه‌سازی عملکرد**: کاهش تأخیر و استفاده از حافظه
- **ادغام مدل**: افزودن پشتیبانی از مدل‌های STT/TTS جدید
- **کیفیت صوتی**: بهبود پیش‌پردازش و پس‌پردازش صوتی
- **مدیریت خطا**: افزایش استحکام و بازیابی خطا
- **تست**: گسترش پوشش تست و افزودن تست‌های یکپارچگی

#### 🔧 اولویت متوسط
- **پشتیبانی چندزبانه**: افزودن پشتیبانی از عربی، ترکی و غیره
- **توسعه GUI**: ایجاد رابط کاربری دوستانه
- **پشتیبانی موبایل**: بهینه‌سازی برای پلتفرم‌های موبایل
- **ادغام ابری**: افزودن پردازش ابری اختیاری
- **توسعه API**: ایجاد REST API برای ادغام خارجی

#### 🚀 ویژگی‌های آینده
- **ادغام همگام‌سازی لب**: انیمیشن صورت همزمان
- **پردازش ویدیو**: ترجمه چندوجهی
- **کلونینگ صدا**: سنتز صدا سفارشی
- **محاسبات Edge**: استقرار IoT و embedded

## راه‌اندازی توسعه

### 1. Fork و Clone

```bash
# Fork کردن مخزن روی GitHub
# سپس clone کردن fork شما
git clone https://github.com/yourusername/VoiceBridge.git
cd VoiceBridge

# افزودن remote upstream
git remote add upstream https://github.com/originalowner/VoiceBridge.git
```

### 2. راه‌اندازی محیط

```bash
# ایجاد محیط مجازی
python -m venv venv
source venv/bin/activate  # Linux/macOS
# یا
venv\Scripts\activate     # Windows

# نصب وابستگی‌های توسعه
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Pre-commit Hooks

```bash
# نصب pre-commit hooks
pip install pre-commit
pre-commit install

# اجرای دستی hooks
pre-commit run --all-files
```

### 4. پیکربندی IDE

#### تنظیمات VS Code

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

#### پیکربندی PyCharm

1. باز کردن پروژه در PyCharm
2. پیکربندی مفسر Python برای استفاده از محیط مجازی
3. فعال کردن بررسی کد و فرمت‌بندی
4. پیکربندی pytest به عنوان اجراکننده تست

## گردش کار مشارکت

### 1. رویکرد Issue First

قبل از شروع کار روی یک ویژگی یا رفع باگ:

1. **بررسی مسائل موجود** برای جلوگیری از تکرار
2. **ایجاد issue جدید** توصیف مشکل یا ویژگی
3. **انتظار برای تأیید نگهدارنده** قبل از شروع کار
4. **اختصاص خود** به issue

### 2. استراتژی Branch

```bash
# ایجاد branch ویژگی
git checkout -b feature/your-feature-name

# یا branch رفع باگ
git checkout -b bugfix/issue-number-description

# یا branch hotfix
git checkout -b hotfix/critical-issue
```

### 3. فرآیند توسعه

```bash
# ایجاد تغییرات
# تست تغییرات شما
python -m pytest tests/

# commit تغییرات
git add .
git commit -m "feat: add new feature description"

# push به fork شما
git push origin feature/your-feature-name
```

### 4. Pull Request

1. **ایجاد Pull Request** از fork شما به مخزن اصلی
2. **پر کردن قالب PR** به طور کامل
3. **پیوند دادن مسائل مرتبط** با استفاده از کلمات کلیدی (fixes #123)
4. **درخواست بررسی** از نگهدارندگان
5. **رسیدگی به بازخورد** به موقع

## استانداردهای کدنویسی

### راهنمای سبک Python

ما از [PEP 8](https://pep8.org/) با برخی تغییرات پیروی می‌کنیم:

```python
# استفاده از Black برای فرمت‌بندی
black --line-length 88 src/ tests/

# استفاده از isort برای مرتب‌سازی import
isort src/ tests/

# استفاده از flake8 برای linting
flake8 src/ tests/
```

### نمونه‌های سبک کد

#### بهترین روش‌ها

```python
# Type hints
def transcribe(self, audio_data: np.ndarray) -> str:
    """تبدیل داده‌های صوتی به متن فارسی.
    
    Args:
        audio_data: chunk صوتی به عنوان آرایه numpy
        
    Returns:
        متن فارسی تبدیل شده
    """
    if audio_data is None or len(audio_data) == 0:
        return ""
    
    try:
        result = self.model.transcribe(audio_data, language="fa")
        return result["text"].strip()
    except Exception as e:
        logger.error(f"تبدیل شکست خورد: {e}")
        return ""
```

#### از این الگوها اجتناب کنید

```python
# بد: بدون type hints، نام‌های متغیر نامشخص
def transcribe(audio):
    result = model.transcribe(audio)
    return result["text"]

# بد: بدون مدیریت خطا
def transcribe(self, audio_data):
    return self.model.transcribe(audio_data)["text"]

# بد: بدون مستندسازی
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
