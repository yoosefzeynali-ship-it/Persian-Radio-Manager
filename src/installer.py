import os
import shutil

from github_api import get_latest_release
from downloader import download_file
from extractor import extract_zip
from backup import backup_file
from version_manager import save_installed_version

from config import ETS2_PATH, ATS_PATH


def find_radio_file(folder):

    for root, dirs, files in os.walk(folder):

        if "live_streams.sii" in files:

            return os.path.join(
                root,
                "live_streams.sii"
            )

    return None


def install_to_game(source_file, game_path, game_name):

    if not os.path.exists(game_path):

        print(
            f"{game_name} path not found"
        )

        return False


    target_file = os.path.join(
        game_path,
        "live_streams.sii"
    )


    # Backup درست قبل از جایگزینی
    backup_file(
        target_file,
        game_name
    )


    shutil.copy2(
        source_file,
        target_file
    )


    print(
        f"{game_name} installation completed"
    )


    return True


def cleanup():

    folders = [

        "downloads",

        "temp"

    ]

    for folder in folders:

        if os.path.exists(folder):

            shutil.rmtree(
                folder,
                ignore_errors=True
            )


def install_radio_pack(
        install_ets2=False,
        install_ats=False
):

    if not install_ets2 and not install_ats:

        print(
            "No game selected"
        )

        return False


    print(
        "Checking latest release..."
    )


    release = get_latest_release()


    if "error" in release:

        print(
            release["error"]
        )

        return False


    download_url = release.get(
        "download_url"
    )


    if not download_url:

        print(
            "Download file not found"
        )

        return False


    zip_file = download_file(
        download_url
    )


    if not zip_file:

        return False


    extracted = extract_zip(
        zip_file
    )


    if not extracted:

        return False


    radio_file = find_radio_file(
        extracted
    )


    if not radio_file:

        print(
            "live_streams.sii not found"
        )

        return False


    result = True


    if install_ets2:

        result = install_to_game(
            radio_file,
            ETS2_PATH,
            "ETS2"
        ) and result


    if install_ats:

        result = install_to_game(
            radio_file,
            ATS_PATH,
            "ATS"
        ) and result


    if result:

        save_installed_version(
            release["version"]
        )

        cleanup()

        print(
            "Radio Pack installed successfully!"
        )


    return result