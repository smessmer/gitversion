import VersionInfoReader
import VersionInfoOutputter


def get_version():
    return VersionInfoReader.from_git()


def create_version_file(output_file, lang):
    version_info = get_version()
    output = _output(version_info, lang=lang)
    _write_to_file(output_file, output)


def _output(version_info, lang):
    if lang == "cpp":
        return VersionInfoOutputter.to_cpp(version_info)
    elif lang == "python":
        return VersionInfoOutputter.to_python(version_info)
    else:
        raise ValueError("Unknown language")


def _write_to_file(output_file, output):
    with open(output_file, 'w') as file:
        file.write(output)
