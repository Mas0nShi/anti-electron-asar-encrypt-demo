# -*- coding:utf-8 -*-
"""
@Author: Mas0n
@File: config.py
@Time: 2022/4/4 19:50
@Desc: It's all about getting better.
"""
# Example for Electron application.

DOWNLOAD_LINK = {
    "win": {
        "x86": "https://typora.io/windows/typora-setup-ia32.exe",
        "x64": "https://typora.io/windows/typora-setup-x64.exe",
        "arm64": "https://typora.io/windows/typora-setup-arm64.exe",
    },
    "linux": {
        "x64": "https://download.typora.io/linux/Typora-linux-x64.tar.gz",
        "arm64": "https://download.typora.io/linux/Typora-linux-arm64.tar.gz",
    },
}

EXTRACT_ROOT_PATH = {
    "win": "app",
    "linux": "bin/Typora-linux-x64"
}