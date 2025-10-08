#!/usr/bin/env python3
"""
اسکریپت نصب خودکار LinguaStream
این اسکریپت مشکلات سازگاری Python 3.13 را حل می‌کند
"""

import sys
import subprocess
import platform
import os

def check_python_version():
    """بررسی ورژن Python"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 13:
        print("⚠️  Warning: Python 3.13+ detected. Some packages may not be compatible.")
        print("💡 Recommendation: Use Python 3.11 for best compatibility.")
        return False
    elif version.major == 3 and version.minor >= 11:
        print("✅ Python version is compatible!")
        return True
    else:
        print("❌ Python version is too old. Please use Python 3.11+")
        return False

def install_package(package):
    """نصب پکیج با مدیریت خطا"""
    try:
        print(f"📦 Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def install_pyaudio():
    """نصب PyAudio با روش‌های مختلف"""
    print("🎤 Installing PyAudio...")
    
    # روش 1: نصب مستقیم
    if install_package("pyaudio"):
        return True
    
    # روش 2: استفاده از pipwin (Windows)
    if platform.system() == "Windows":
        print("🪟 Trying pipwin method for Windows...")
        if install_package("pipwin"):
            try:
                subprocess.check_call([sys.executable, "-m", "pipwin", "install", "pyaudio"])
                print("✅ PyAudio installed via pipwin!")
                return True
            except:
                pass
    
    # روش 3: نصب از wheel
    print("🔧 Trying wheel installation...")
    if install_package("pyaudio --only-binary=all"):
        return True
    
    print("❌ PyAudio installation failed. Please install manually:")
    print("   Windows: pip install pipwin && pipwin install pyaudio")
    print("   Linux: sudo apt-get install portaudio19-dev && pip install pyaudio")
    print("   macOS: brew install portaudio && pip install pyaudio")
    return False

def main():
    """تابع اصلی"""
    print("🚀 LinguaStream Installation Script")
    print("=" * 50)
    
    # بررسی ورژن Python
    if not check_python_version():
        print("\n⚠️  Continuing with current Python version...")
    
    # لیست پکیج‌های ضروری
    essential_packages = [
        "torch",
        "torchaudio", 
        "transformers",
        "openai-whisper",
        "streamlit",
        "numpy",
        "scipy",
        "librosa",
        "soundfile"
    ]
    
    # نصب پکیج‌های ضروری
    print("\n📦 Installing essential packages...")
    failed_packages = []
    
    for package in essential_packages:
        if not install_package(package):
            failed_packages.append(package)
    
    # نصب PyAudio
    print("\n🎤 Installing PyAudio...")
    if not install_pyaudio():
        failed_packages.append("pyaudio")
    
    # نتیجه
    print("\n" + "=" * 50)
    if not failed_packages:
        print("🎉 All packages installed successfully!")
        print("\n🚀 Next steps:")
        print("1. Run: python setup.py")
        print("2. Run: streamlit run app.py")
    else:
        print(f"⚠️  Some packages failed to install: {', '.join(failed_packages)}")
        print("\n🔧 Manual installation:")
        for package in failed_packages:
            print(f"   pip install {package}")
    
    print("\n📚 For more help, see INSTALL_FIX.md")

if __name__ == "__main__":
    main()
