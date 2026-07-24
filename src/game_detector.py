import os
from config import ETS2_PATH, ATS_PATH


def check_game(path):

    if os.path.exists(path):
        return True

    return False



def detect_games():

    return {

        "ETS2": check_game(ETS2_PATH),

        "ATS": check_game(ATS_PATH)

    }