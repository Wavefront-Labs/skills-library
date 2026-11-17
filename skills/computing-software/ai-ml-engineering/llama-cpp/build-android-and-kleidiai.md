---
id: computing-software.ai-ml-engineering.llama-cpp.build-android-and-kleidiai
name: build-android-and-kleidiai
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, android, termux, kleidiai, arm64]
level: advanced
status: docs-checked
description: "Run llama.cpp on Android through Termux or the NDK and enable KleidiAI on Arm CPUs."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/android.md", "https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Android and KleidiAI

**Termux** (on device, no root): in the Termux shell run `apt update && apt upgrade -y` and `apt install git cmake libandroid-spawn`, then follow the normal CMake build. Put the downloaded GGUF in `~/` for best performance and run:

```bash
./build/bin/llama-cli -m ~/{model}.gguf -c {context-size} -p "{your-prompt}"
```

Set the context size to something reasonable (the guide suggests 4096 to start), otherwise memory can spike and kill the terminal.

**Cross-compile with the NDK:** set `ANDROID_NDK` to the NDK root, then:

```bash
cmake \
  -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake \
  -DANDROID_ABI=arm64-v8a \
  -DANDROID_PLATFORM=android-28 \
  -DGGML_NATIVE=OFF \
  -DGGML_OPENMP=OFF \
  -DGGML_LLAMAFILE=OFF \
  -DLLAMA_OPENSSL=OFF \
  -B build-android
cmake --build build-android --config Release -j{n}
cmake --install build-android --prefix {install-dir} --config Release
```

Why these options (from the guide): `GGML_NATIVE=OFF` is required because the host CPU is not the target CPU; OpenMP would have to be installed by CMake as a dependency, which is not supported; llamafile does not appear to support Android; `LLAMA_OPENSSL=OFF` avoids OpenSSL, which is not in the NDK stable native API set. Do not add a global `-march` flag unless you intend to raise the baseline for every source.

Run on the device: `adb shell "mkdir /data/local/tmp/llama.cpp"`, `adb push` the install dir and the model there, then in `adb shell` run `LD_LIBRARY_PATH=lib ./bin/llama-simple -m {model}.gguf -c {context-size} -p "{your-prompt}"`. Android does not find the `lib` path on its own, hence `LD_LIBRARY_PATH`.

**Android Studio:** import `examples/llama.android`, Gradle sync and build. The binding supports acceleration up to SME2 on Arm and AMX on x86-64 and detects the hardware automatically.

**KleidiAI** (build.md, "Arm KleidiAI"): provides Arm CPU microkernels for the ggml CPU backend. Build with `-DGGML_CPU_KLEIDIAI=ON`, valid only for AArch64/arm64 (not x86, 32-bit Arm or other Android ABIs). On Android arm64-v8a, add it to the NDK command above; the Android Studio project enables it automatically for arm64-v8a. Building it in makes the kernels available; at run time llama.cpp picks a compatible kernel from CPU features, tensor type, operation shape and backend priority.

Verify with `llama-cli`: a line such as `load_tensors: CPU_KLEIDIAI model buffer size = ...` shows tensors were allocated through the KleidiAI buffer, not that every operation used a KleidiAI kernel.

`GGML_KLEIDIAI_SME` is a diagnostics/debug override, to be left unset in normal use: unset means automatic detection, `0` disables SME-family kernels, and `<n> > 0` enables them with up to n threads for quantized SME kernels.

**Qualcomm GPUs:** see the OpenCL backend skill; build.md also lists a Hexagon backend with its own README.

## Checked

Date: 2026-11-08. Confirmed against docs/android.md and the Arm KleidiAI and OpenCL sections of docs/build.md. Removed: the apt/Termux "clone and build" snippet detail beyond what the guide shows, and the unsourced advice on choosing quantizations.

Method: docs-only read of cited pages, 2026-11-08
