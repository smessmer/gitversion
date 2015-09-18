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
  FILE(MAKE_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/git_version_builder")
  EXECUTE_PROCESS(COMMAND /usr/bin/env python "${DIR_OF_GITVERSION_TOOL}/git-version-builder" --lang cpp --dir "${CMAKE_CURRENT_SOURCE_DIR}" "${CMAKE_CURRENT_BINARY_DIR}/git_version_builder/git_version.h"
		  RESULT_VARIABLE result)
  IF(NOT ${result} EQUAL 0)
    MESSAGE(FATAL_ERROR "Error running messmer/git-version tool. Return code is: ${result}")
  ENDIF()
  TARGET_INCLUDE_DIRECTORIES(${BII_BLOCK_TARGET} INTERFACE "${CMAKE_CURRENT_BINARY_DIR}/git_version_builder")
endfunction(ADD_GIT_VERSION)
