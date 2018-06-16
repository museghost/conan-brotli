from conans import ConanFile, CMake, tools
import os.path


class BrotliConan(ConanFile):
    name = "brotli"
    version = "1.0.4"
    license = "MIT License"
    url = "https://github.com/google/brotli"
    description = "Brotli is a generic-purpose lossless compression algorithm that compresses data using a combination of a modern variant of the LZ77 algorithm, Huffman coding and 2nd order context modeling, with a compression ratio comparable to the best currently available general-purpose compression methods. It is similar in speed with deflate but offers more dense compression."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    scm = {
        "type": "git",
        # "url": "https://github.com/google/brotli.git",
        "url": "file:///Users/yuweishan/brotli.git",
        "revision": "v"+version
    }

    def source(self):
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("CMakeLists.txt", "project(brotli C)", '''project(brotli C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

        # log2 is not available for some platform, see FastLog2
        tools.replace_in_file("CMakeLists.txt", 'message(FATAL_ERROR "log2() not found")', 'message(WARNING "log2() not found")')

    # def build_id(self):
    #     self.info_build.options.shared = "any"

    def build(self):
        cmake = CMake(self)
        cmake.configure(defs={"BROTLI_BUNDLED_MODE":"ON"})
        pattern = "brotli%s"
        if not self.options.shared: pattern += "-static"
        for libname in ["dec", "enc"]:
            cmake.build(target=pattern % libname)

    def package(self):
        if not self.options.shared:
            folder = os.path.join(self.build_folder, "lib")
            for filename in os.listdir(folder):
                if "-static." not in filename: continue
                old_name = os.path.join(folder, filename)
                new_name = os.path.join(folder, filename.replace("-static.", "."))
                os.rename(old_name, new_name)
        self.copy("*.h", dst="include", src="c/include")
        self.copy("*.lib", dst="lib", src="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", src="lib", keep_path=False, symlinks=True)
        self.copy("*.dylib", dst="lib", src="lib", keep_path=False, symlinks=True)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["brotlicommon", "brotlidec", "brotlienc"]

    def configure(self):
        del self.settings.compiler.libcxx
