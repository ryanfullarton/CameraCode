

cmake_minimum_required(VERSION 2.6 FATAL_ERROR)

############ Make your changes here ############

set(name   camera_Calibration)
set(WITH_VIS false)
############ What's below should not need to be changed ############

# http://www.cmake.org/cmake/help/cmake_tutorial.html
# http://www.cmake.org/cmake/help/cmake2.6docs.html
# http://www.cmake.org/Wiki/CMake_FAQ

set(mymain ${name}.cc )
set(myexe  ${name}    )
set(myproj ${name}_   )  # any name as long as it is different from myexe

project(${myproj})
find_package( OpenCV REQUIRED )

include_directories( ${OpenCV_INCLUDE_DIRS} )


file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cc)
file(GLOB headers ${PROJECT_SOURCE_DIR}/include/*.hh)

include_directories(/usr/include/opencv4/)
include_directories(/usr/include/opencv4/opencv2/)
add_executable(${myexe} ${mymain})
target_link_libraries( ${myexe} ${OpenCV_LIBS} )


install(TARGETS ${myexe} DESTINATION bin)
