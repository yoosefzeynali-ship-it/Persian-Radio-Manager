import requests
import urllib3


urllib3.disable_warnings()


OWNER = "yoosefzeynali-ship-it"

REPO = "Persian-Radio-Pack"


API_URL = (
    f"https://api.github.com/repos/"
    f"{OWNER}/{REPO}/releases/latest"
)



def get_latest_release():

    try:

        response = requests.get(
            API_URL,
            timeout=10,
            verify=False
        )

        response.raise_for_status()


        data = response.json()


        release = {

            "version": data.get("tag_name"),

            "name": data.get("name"),

            "download_url": None

        }


        assets = data.get(
            "assets",
            []
        )


        for asset in assets:

            name = asset.get(
                "name",
                ""
            )


            if (
                name.startswith("PersianRadioPack")
                and name.endswith(".zip")
            ):

                release["download_url"] = (
                    asset.get(
                        "browser_download_url"
                    )
                )

                break


        return release


    except Exception as e:

        return {

            "error": str(e)

        }