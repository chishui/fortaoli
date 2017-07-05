cmake_minimum_required (VERSION 2.8)
set(CMAKE_MACOSX_RPATH 1)
project (main)
set(CMAKE_BUILD_TYPE Release)
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Wall")

add_definitions(-DBUILDING_DLL)

add_library (main SHARED main.cpp)
