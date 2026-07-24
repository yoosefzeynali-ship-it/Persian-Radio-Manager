from github_api import get_latest_release
from version_manager import get_installed_version


def check_update():

    latest = get_latest_release()

    if "error" in latest:

        return latest

    installed = get_installed_version()

    return {

        "installed": installed,

        "latest": latest["version"],

        "update_available":
            installed != latest["version"]

    }