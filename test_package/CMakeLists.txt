project(PackageTest C)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(version_check version_check.c)
target_link_libraries(version_check ${CONAN_LIBS})
