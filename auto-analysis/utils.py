# -*- coding:utf-8 -*-
"""
@Author: Mas0n
@File: utils.py
@Time: 2022/4/3 18:36
@Desc: It's all about getting better.
"""
from loguru import logger as log
from config import DOWNLOAD_LINK, EXTRACT_ROOT_PATH
import subprocess
import json
import os

BASE_DIR = os.path.dirname(__file__)


def get_version(to_path):
    package_file_path = os.path.join(to_path, "app/resources/package.json")
    package_info = open(package_file_path, "r").read()
    package_obj = json.loads(package_info)
    return package_obj["version"]


def download_file(from_link, to_path):
    subprocess.check_call(["wget", "-q", from_link, "-O", to_path])


def extract_file(from_path, to_path):
    if from_path.endswith(".exe"):
        subprocess.check_call(["innoextract", "-q", from_path, "-d", to_path])
    elif from_path.endswith(".tar.gz"):
        subprocess.check_call(["tar", "-zxvf", from_path, "-C", to_path])


def patch_file(_key, _iv, to_dir):
    exports_file_path = os.path.join(BASE_DIR, "../exports.tar.gz")
    save_dir = os.path.join(to_dir, "build")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    subprocess.check_call(["tar", "-zxvf", exports_file_path, "-C", save_dir])
    patch_file_path = os.path.join(save_dir, "decrypt.py")
    content = open(patch_file_path, "r").read()
    content = content.replace("{AES_KEY}", f"b''.fromhex('{_key}')")
    content = content.replace("{AES_IV}", f"b''.fromhex('{_iv}')")
    open(patch_file_path, "w").write(content)


def scheduler(func, basedir, link, root_path):
    download_path = os.path.join(basedir, os.path.basename(link))
    log.info(f"downloading from {link}")
    download_file(link, download_path)
    log.info("ready extract package")

    extract_file(download_path, basedir)
    log.info("preparation stage completed")

    main_node_path = os.path.join(basedir, os.path.join(root_path, "resources/app.asar.unpacked/main.node"))
    log.info("auto analysis start")
    key, iv = func.get_aes_key_and_iv(main_node_path)
    log.success("analysis done")

    patch_file(key.hex(), iv.hex(), basedir)
    log.success("patch done")


def win_x64_run():
    from win.x64 import analysis
    dirs = os.path.join(BASE_DIR, "win/x64")
    url = DOWNLOAD_LINK["win"]["x64"]
    scheduler(func=analysis, basedir=dirs, link=url, root_path=EXTRACT_ROOT_PATH["win"])


def win_x86_run():
    from win.x86 import analysis
    dirs = os.path.join(BASE_DIR, "win/x86")
    url = DOWNLOAD_LINK["win"]["x86"]
    scheduler(func=analysis, basedir=dirs, link=url, root_path=EXTRACT_ROOT_PATH["win"])


def linux_x64_run():
    from linux.x64 import analysis
    dirs = os.path.join(BASE_DIR, "linux/x64")
    url = DOWNLOAD_LINK["linux"]["x64"]
    scheduler(func=analysis, basedir=dirs, link=url, root_path=EXTRACT_ROOT_PATH["linux"])


if __name__ == '__main__':
    win_x86_run()
    win_x64_run()
    linux_x64_run()
