import os


CONFIG_FOLDER = "config"

VERSION_FILE = os.path.join(
    CONFIG_FOLDER,
    "installed_version.txt"
)


def ensure_folder():

    os.makedirs(
        CONFIG_FOLDER,
        exist_ok=True
    )


def save_installed_version(version):

    ensure_folder()

    with open(
        VERSION_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(version)


def get_installed_version():

    if not os.path.exists(VERSION_FILE):

        return None

    with open(
        VERSION_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read().strip()