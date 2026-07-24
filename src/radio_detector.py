import os

from config import ETS2_PATH, ATS_PATH


PACK_SIGNATURE = "Persian Radio Pack"


def read_radio_file(game_path):

    radio_file = os.path.join(
        game_path,
        "live_streams.sii"
    )

    if not os.path.exists(radio_file):
        return False


    try:
        with open(
            radio_file,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            content = file.read()

            if PACK_SIGNATURE in content:
                return True


    except Exception:
        pass


    return False



def detect_radio_pack():

    return {

        "ETS2 Pack":
            read_radio_file(ETS2_PATH),

        "ATS Pack":
            read_radio_file(ATS_PATH)

    }