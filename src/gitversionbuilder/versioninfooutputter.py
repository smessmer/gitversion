

def to_cpp(version_info):
    return _CppFormatter().format(version_info)


def to_python(version_info):
    return _PythonFormatter().format(version_info)


class _Formatter(object):
    def __init__(self):
        pass

    def format(self, version_info):
        return self.main_formatter(version_info,
                                   self._format_is_stable(version_info) + self._format_tag_interpretation(version_info))

    def _format_is_stable(self, version_info):
        if not version_info.git_tag_exists:
            return self.is_stable_formatter(False)
        else:
            tag_interpretation = version_info.interpret_tag_name()
            if tag_interpretation is not None:
                return self.is_stable_formatter(tag_interpretation.is_stable)
            else:
                return ""

    def _format_tag_interpretation(self, version_info):
        tag_interpretation = version_info.interpret_tag_name()
        if tag_interpretation is None:
            return ""
        else:
            formatted_version_components = self.version_components_formatter(tag_interpretation.version_components)
            return self.tag_interpretation_formatter(tag_interpretation, formatted_version_components, version_info.buildnum)


# ----------------------------------------
# C++ Formatter
# ----------------------------------------

class _CppFormatter(_Formatter):
    def main_formatter(self, version_info, other_variables):
        return """
// ---------------------------------------------------
// This file is autogenerated by git-version.
// DO NOT MODIFY!
// ---------------------------------------------------

#ifndef MESSMER_GITVERSION_VERSION_H
#define MESSMER_GITVERSION_VERSION_H

#define VERSION_STRING "%s"
#define GIT_TAG_NAME "%s"
#define GIT_BRANCH_NAME "%s"
#define GIT_COMMITS_SINCE_TAG "%d"
#define GIT_COMMIT_ID "%s"
#define GIT_LAST_COMMIT_DATE "%s"
#define MODIFIED_SINCE_COMMIT %s
#define IS_DEV_VERSION %s
%s

#endif
""" % (version_info.version_string,
       version_info.git_tag_name,
       version_info.branch_name,
       version_info.git_commits_since_tag,
       version_info.git_commit_id,
       version_info.last_commit_data,
       str(version_info.modified_since_commit).lower(),
       str(version_info.is_dev).lower(),
       other_variables)

    def is_stable_formatter(self, is_stable):
        return """
  constexpr bool IS_STABLE_VERSION = %s;
""" % str(is_stable).lower()

    def tag_interpretation_formatter(self, tag_interpretation, version_components, buildnum):
        return """
  constexpr const char *VERSION_COMPONENTS[] = %s;
  constexpr const char *VERSION_TAG = "%s";
  #define VER_MAJOR %s
  #define VER_MINOR %s
  #define VER_BUG_FIX %s
  #define VER_BUILD_NUM %s
""" % (version_components,
       tag_interpretation.version_tag,
       tag_interpretation.version_components[0],
       tag_interpretation.version_components[1],
       tag_interpretation.version_components[2],
       buildnum)

    def version_components_formatter(self, version_components):
        return "{\"" + "\", \"".join(version_components) + "\"}"


# ----------------------------------------
# Python Formatter
# ----------------------------------------

class _PythonFormatter(_Formatter):
    def main_formatter(self, version_info, other_variables):
        return """
# ---------------------------------------------------
# This file is autogenerated by git-version.
# DO NOT MODIFY!
# ---------------------------------------------------

VERSION_STRING = "%s"
GIT_TAG_NAME = "%s"
GIT_COMMITS_SINCE_TAG = %d
GIT_COMMIT_ID = "%s"
MODIFIED_SINCE_COMMIT = %s
IS_DEV_VERSION = %s
%s
""" % (version_info.version_string, version_info.git_tag_name, version_info.git_commits_since_tag,
       version_info.git_commit_id, version_info.modified_since_commit, version_info.is_dev, other_variables)

    def is_stable_formatter(self, is_stable):
        return """
IS_STABLE_VERSION = %s
""" % is_stable

    def tag_interpretation_formatter(self, tag_interpretation, version_components, buildnum=1):
        return """
VERSION_COMPONENTS = %s
VERSION_TAG = "%s"
""" % (version_components, tag_interpretation.version_tag)

    def version_components_formatter(self, version_components):
        return "[\"" + "\", \"".join(version_components) + "\"]"
