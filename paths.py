import os
import sys


def base_dir():
    """Directory where bundled resources (vendor/, ui/) live, whether
    running from source or from a frozen PyInstaller build."""
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def vendor_ffmpeg_dir():
    path = os.path.join(base_dir(), "vendor", "ffmpeg")
    return path if os.path.isdir(path) else None


def vendor_models_dir():
    path = os.path.join(base_dir(), "vendor", "models")
    return path if os.path.isdir(path) else None
