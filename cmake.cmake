set(DIR_OF_GITVERSION_TOOL ${CMAKE_CURRENT_LIST_DIR}) 

#################################################
# Add git version information 
# Uses:      
#   GIT_VERSION_INIT()
# Then, you can write in your source file:
#   #include <messmer/gitversion/version.h>
#   cout << gitversion::VERSION.toString() << endl;
#################################################
function(GIT_VERSION_INIT)
  FILE(MAKE_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/messmer_gitversion")
  FILE(MAKE_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/messmer_gitversion/gitversion")
  SET(ENV{PYTHONPATH} "${DIR_OF_GITVERSION_TOOL}/src")
  EXECUTE_PROCESS(COMMAND /usr/bin/env python -m gitversionbuilder --lang cpp --dir "${CMAKE_CURRENT_SOURCE_DIR}" "${CMAKE_CURRENT_BINARY_DIR}/messmer_gitversion/gitversion/version.h"
		  RESULT_VARIABLE result)
  IF(NOT ${result} EQUAL 0)
    MESSAGE(FATAL_ERROR "Error running messmer/git-version tool. Return code is: ${result}")
  ENDIF()
  TARGET_INCLUDE_DIRECTORIES(${BII_BLOCK_TARGET} INTERFACE "${CMAKE_CURRENT_BINARY_DIR}/messmer_gitversion")

  # Load version string and write it to a cmake variable so it can be accessed from cmake.
  FILE(READ "${CMAKE_CURRENT_BINARY_DIR}/messmer_gitversion/gitversion/version.h" VERSION_H_FILE_CONTENT)
  STRING(REGEX REPLACE ".*VERSION_STRING = \"([^\"]*)\".*" "\\1" VERSION_STRING "${VERSION_H_FILE_CONTENT}")
  MESSAGE(STATUS "Version from git: ${VERSION_STRING}")
  SET(GITVERSION_VERSION_STRING "${VERSION_STRING}" PARENT_SCOPE)
endfunction(GIT_VERSION_INIT)
