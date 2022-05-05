from utils import get_version, download_file, extract_file, log
from config import DOWNLOAD_LINK
import os

BASE_DIR = os.path.dirname(__file__)


def run_version(download_os, download_arch):
    from_url = DOWNLOAD_LINK[download_os][download_arch]
    to_dir = os.path.join(BASE_DIR, f"{download_os}/{download_arch}")

    download_path = os.path.join(to_dir, os.path.basename(from_url))
    download_file(from_url, download_path)
    extract_file(download_path, to_dir)
    version = get_version(to_dir)
    open(os.path.join(to_dir, "LATEST_VERSION"), "w").write(version)
    log.success(f"{download_os}-{download_arch} the latest version is {version}")


if __name__ == '__main__':
    run_version("win", "x64")
    # run_version("win", "x86")
    # run_version("linux", "x64")
