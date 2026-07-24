import os
import shutil
from datetime import datetime

from config import ETS2_PATH, ATS_PATH


BACKUP_FOLDER = "backup"



def create_backup_folder():

    if not os.path.exists(BACKUP_FOLDER):

        os.makedirs(
            BACKUP_FOLDER
        )



def backup_file(source_file, game_name):

    try:

        if not os.path.exists(source_file):

            print(
                f"{game_name}: No file found"
            )

            return None


        create_backup_folder()


        game_folder = os.path.join(
            BACKUP_FOLDER,
            game_name
        )


        os.makedirs(
            game_folder,
            exist_ok=True
        )


        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )


        backup_name = (
            f"live_streams_{timestamp}.sii"
        )


        destination = os.path.join(
            game_folder,
            backup_name
        )


        shutil.copy2(
            source_file,
            destination
        )


        print(
            f"{game_name} backup created:"
        )

        print(
            destination
        )


        return destination



    except Exception as e:

        print(
            f"{game_name} Backup Error:",
            e
        )

        return None



def backup_all_games():

    results = {}


    ets2_file = os.path.join(
        ETS2_PATH,
        "live_streams.sii"
    )


    ats_file = os.path.join(
        ATS_PATH,
        "live_streams.sii"
    )


    results["ETS2"] = backup_file(
        ets2_file,
        "ETS2"
    )


    results["ATS"] = backup_file(
        ats_file,
        "ATS"
    )


    return results