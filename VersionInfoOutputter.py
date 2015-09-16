_cpp_format = """
#pragma once
#ifndef __GITVERSIONBUILDER__VERSION_H__
#define __GITVERSIONBUILDER__VERSION_H__

namespace version {
  constexpr const char *versionString = "%s";
  constexpr const char *tagName = "%s";
  constexpr const unsigned int commitsSinceTag = %d;
  constexpr const char *gitCommitId = "%s";
}

#endif
"""


def to_cpp(version_info):
    return _cpp_format % (
        version_info.version_string, version_info.tag_name, version_info.commits_since_tag, version_info.commit_id)
