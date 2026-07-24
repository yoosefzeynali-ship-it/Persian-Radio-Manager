import os
import shutil

from config import ETS2_PATH, ATS_PATH


BACKUP_FOLDER = "backup"


def get_latest_backup(game_name):

    game_folder = os.path.join(
        BACKUP_FOLDER,
        game_name
    )

    if not os.path.exists(game_folder):
        return None

    files = [
        os.path.join(game_folder, f)
        for f in os.listdir(game_folder)
        if f.endswith(".sii")
    ]

    if not files:
        return None

    files.sort(
        key=os.path.getmtime,
        reverse=True
    )

    return files[0]


def restore_game(game_name, game_path):

    backup = get_latest_backup(game_name)

    if backup is None:
        print(f"No backup found for {game_name}")
        return False

    destination = os.path.join(
        game_path,
        "live_streams.sii"
    )

    shutil.copy2(
        backup,
        destination
    )

    print(f"{game_name} restored successfully")

    return True


def restore_backup(
    restore_ets2=False,
    restore_ats=False
):

    result = True

    if restore_ets2:

        result = restore_game(
            "ETS2",
            ETS2_PATH
        ) and result

    if restore_ats:

        result = restore_game(
            "ATS",
            ATS_PATH
        ) and result

    return result