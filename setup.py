from cx_Freeze import setup
import certifi
import charset_normalizer
import idna
import mido
import packaging
import pynput
import requests
import six
import urllib3
import yt_dlp

include_files = {"src/"}

# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "include_files": include_files,
    "packages": ["certifi", "charset_normalizer", "idna", "mido", "packaging", "pynput", "requests", "six", "urllib3", "yt_dlp"],
}

setup(
    name="guifoo",
    version="0.1",
    description="My GUI application!",
    options={"build_exe": build_exe_options},
    executables=[{"script": "app.py", "base": "gui"}],
)