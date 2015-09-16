import subprocess
import VersionInfo


def from_git():
    return VersionInfo.parse(_read_git_version_string())


def _read_git_version_string():
    try:
        return subprocess.check_output(["git", "describe", "--tags", "--long", "--abbrev=4"])
    except subprocess.CalledProcessError:
        return subprocess.check_output(["git", "describe", "--all", "--long", "--abbrev=7"])
