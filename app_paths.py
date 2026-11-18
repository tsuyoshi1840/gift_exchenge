import sys
from pathlib import Path


# ==================================
# 素材ファイルの場所
# ==================================
# EXE（PyInstaller）で動いているときは展開先フォルダ（sys._MEIPASS）、
# Pythonで直接動かしているときはこのファイルがあるフォルダを基準にする。

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent


def resource_path(*parts):
    """素材ファイルのパスを返す。例: resource_path("assets", "images", "icon_image.ico")"""
    return BASE_DIR.joinpath(*parts)
