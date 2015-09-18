#pragma once
#ifndef MESSMER_GITVERSION_SRC_VERSION_H
#define MESSMER_GITVERSION_SRC_VERSION_H

#include <stdexcept>
#include <messmer/cpp-utils/constexpr/const_string.h>

namespace gitversion {
    enum class VersionTag : unsigned char {
        ALPHA, BETA, RC1, FINAL
    };

    constexpr cpputils::const_string VersionTagToString(VersionTag tag) {
        return (tag == VersionTag::ALPHA) ? "alpha" :
               (tag == VersionTag::BETA) ? "beta" :
               (tag == VersionTag::RC1) ? "rc1" :
               (tag == VersionTag::FINAL) ? "" :
               throw std::logic_error("Unknown version tag");
    }

    class Version {
    public:
        constexpr Version(unsigned int major, unsigned int minor, VersionTag tag, unsigned int commitsSinceVersion,
                          const cpputils::const_string &gitCommitId)
                : _major(major), _minor(minor), _tag(tag), _commitsSinceVersion(commitsSinceVersion),
                  _gitCommitId(gitCommitId) { }

        constexpr unsigned int major() const {
            return _major;
        }

        constexpr unsigned int minor() const {
            return _minor;
        }

        constexpr VersionTag tag() const {
            return _tag;
        }

	constexpr cpputils::const_string gitCommitId() const {
	    return _gitCommitId;
	}

        constexpr bool isDev() const {
            return _commitsSinceVersion != 0;
        }

        constexpr bool isStable() const {
            return (!isDev()) && _tag == VersionTag::FINAL;
        }

        constexpr bool operator==(const Version &rhs) const {
            return _major == rhs._major && _minor == rhs._minor && _tag == rhs._tag;
        }

        constexpr bool operator!=(const Version &rhs) const {
            return !operator==(rhs);
        }

        std::string toString() const {
            if (isDev()) {
                return _versionTagString() + "-dev" + std::to_string(_commitsSinceVersion) + "-" + _gitCommitId.toStdString();
            } else {
                return _versionTagString();
            }
        }

    private:

        std::string _versionTagString() const {
            return std::to_string(_major) + "." + std::to_string(_minor) + VersionTagToString(_tag).toStdString();
        }

        const unsigned int _major;
        const unsigned int _minor;
        const VersionTag _tag;
        const unsigned int _commitsSinceVersion;
        const cpputils::const_string _gitCommitId;
    };
}


#endif
