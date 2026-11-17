---
id: computing-software.ai-ml-engineering.llama-cpp.build-cpu-and-general
name: build-cpu-and-general
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, cmake-build, cpu-build, ccache, windows-build]
level: intro
status: docs-checked
description: "Build llama.cpp for CPU with CMake, static builds, debug builds, ccache and the Windows presets."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Building llama.cpp (CPU)

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
cmake -B build
cmake --build build --config Release
```

Notes from the build guide:

- Faster compiles: add `-j` (for example `-j 8` runs 8 jobs) or use a generator that parallelises, such as Ninja. Install ccache for faster repeated compilation.
- Static build: `-DBUILD_SHARED_LIBS=OFF`.
- Debug build, single-config generators (the default Unix Makefiles ignores `--config`): `cmake -B build -DCMAKE_BUILD_TYPE=Debug` then `cmake --build build`.
- Debug build, multi-config generators (`-G` Visual Studio, Xcode): `cmake -B build -G "Xcode"` then `cmake --build build --config Debug`.
- HTTPS/TLS needs the OpenSSL development libraries (for example `libssl-dev` on Debian/Ubuntu). Without them the project builds and runs without SSL support. `-DLLAMA_OPENSSL=OFF` appears in the Android cross-compile command.

Windows (x86, x64, arm64) with MSVC or clang: install Visual Studio 2022 with the "Desktop development with C++" workload plus C++ CMake Tools, Git for Windows, the C++ Clang compiler and MS-Build support for the LLVM toolset, and always build from a Developer Command Prompt or PowerShell for VS2022. Presets named in the guide:

```
cmake --preset arm64-windows-llvm-release -D GGML_OPENMP_FETCH=ON
cmake --build build-arm64-windows-llvm-release

cmake --preset x64-windows-llvm-release
cmake --build build-x64-windows-llvm-release
```

The x64 Ninja/clang preset needs the `LIB` environment variable set to the Windows Kits and MSVC library paths. `GGML_OPENMP_FETCH` downloads the LLVM OpenMP runtime and needs Clang, 7-Zip and network access at configure time; omit it to use CMake's normal OpenMP detection or pass `-D GGML_OPENMP=OFF` to disable OpenMP.

Several backends can be built together (for example `-DGGML_CUDA=ON -DGGML_VULKAN=ON`). At run time `--device` picks the devices, `--list-devices` shows them, and `--device none` fully disables GPU acceleration (`-ngl 0` alone may still use the GPU for some work). `-DGGML_BACKEND_DL=ON` builds backends as dynamic libraries loaded at run time, so one binary can serve machines with different GPUs.

Metal is enabled by default on macOS; pass `-DGGML_METAL=OFF` to disable it.

## Checked

Date: 2026-11-08. Confirmed against docs/build.md (CPU Build, Metal Build, Notes about GPU-accelerated backends) and the repository README (backend list). Removed: the `-t llama-server` single-target build and the claim that `-DLLAMA_OPENSSL=ON` enables HTTPS, since neither is stated on the page; "ccache is used automatically" was reworded to the page's "install ccache".

Method: docs-only read of cited pages, 2026-11-08
