---
id: computing-software.ai-ml-engineering.llama-cpp.build-vulkan-backend
name: build-vulkan-backend
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, vulkan, glslc, moltenvk, spirv]
level: practitioner
status: docs-checked
description: "Build with the Vulkan backend, required SDK tools, vulkaninfo checks and macOS options."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vulkan build

```bash
cmake -B build -DGGML_VULKAN=ON
cmake --build build --config Release
```

(The guide also writes `-DGGML_VULKAN=1` in its Linux and macOS sections.)

**Linux:** either install the LunarG Vulkan SDK from the tarball (after setup, `source` its `setup_env.sh` in every terminal session you build from, or the build will not work), or use system packages. On Debian/Ubuntu: `sudo apt-get install libvulkan-dev glslc spirv-headers`. SPIRV-Headers (`spirv/unified1/spirv.hpp`) are required and not always pulled in by the loader dev package; other distros call the package `spirv-headers` (Ubuntu/Debian/Arch) or `spirv-headers-devel` (Fedora/openSUSE). Run `vulkaninfo` first to confirm the SDK works. Test with `./build/bin/llama-cli -m "PATH_TO_MODEL" -p "Hi you how are you" -ngl 99`; the output should include a `ggml_vulkan: Using ...` line naming your GPU.

**Windows:** three routes in the guide: w64devkit (copy `glslc.exe`, `vulkan-1.lib` and the headers from the Vulkan SDK into w64devkit and create a `vulkan.pc`), Git Bash MINGW64 with Visual Studio (C++), CMake and the Vulkan SDK, or MSYS2 (UCRT terminal; install `mingw-w64-ucrt-x86_64-gcc`, `-cmake`, `-vulkan-devel`, `-shaderc`, `-spirv-headers` with pacman). All then run the two CMake commands above. The LunarG SDK Include directory already contains the SPIR-V headers.

**macOS:** follow LunarG's macOS Vulkan SDK guide. Two drivers map Vulkan to Metal: MoltenVK (the default with the SDK) and KosmicKrisp (tick it in the SDK installer). Switch by pointing `VK_ICD_FILENAMES` and `VK_DRIVER_FILES` at `$VULKAN_SDK/share/vulkan/icd.d/libkosmickrisp_icd.json`. Source the SDK's `setup-env.sh`, then build with `cmake -B build -DGGML_VULKAN=1 -DGGML_METAL=OFF`.

**Docker:** the Vulkan SDK is installed inside the container. `docker build -t llama-cpp-vulkan --target light -f .devops/vulkan.Dockerfile .`, then run with the GPU devices mapped, for example `--device /dev/dri/renderD128:/dev/dri/renderD128 --device /dev/dri/card1:/dev/dri/card1`.

Several backends can be built together; select with `--device` and list with `--list-devices`.

## Checked

Date: 2026-11-08. Confirmed against the Vulkan section of docs/build.md. Removed: `vulkaninfo --summary`, `--device Vulkan0`, the `VULKAN_SDK` Windows advice, the `-vulkan` image-tag claim, and the closing portability remark, none of which are on the page.

Method: docs-only read of cited pages, 2026-11-08
