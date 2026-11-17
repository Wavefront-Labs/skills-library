---
id: computing-software.ai-ml-engineering.llama-cpp.build-zendnn-amd
name: build-zendnn-amd
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, zendnn, amd-epyc, bf16, matmul]
level: advanced
status: docs-checked
description: "Speed up CPU inference on AMD Zen processors with the ZenDNN backend, data types and tuning variable."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/backend/ZenDNN.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ZenDNN (AMD CPU)

ZenDNN is AMD's deep learning library for AMD EPYC CPUs (and Ryzen on Zen architectures). It is not the same as IBM's zDNN. The documented platform is Linux (Ubuntu 20.04, 22.04, 24.04 verified). Build llama.cpp with it; CMake downloads and builds ZenDNN automatically:

```bash
cmake -B build -DGGML_ZENDNN=ON -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j $(nproc)
```

To use your own ZenDNN build (requires CMake >= 3.25 to build ZenDNN), set `ZENDNN_ROOT` as an environment variable or pass `-DZENDNN_ROOT=/path/to/ZenDNN/build/install`.

Run-time notes:

- The backend accelerates `MUL_MAT` and `MUL_MAT_ID` (MoE) only; other operations run on the standard CPU backend.
- Data types: FP32, BF16 and Q8_0. BF16 gives the best performance on Zen 4 and Zen 5 (EPYC 9004/9005); BF16 needs those architectures, otherwise FP32 is used. Other quantization formats fall back to the standard CPU backend.
- `ZENDNNL_MATMUL_ALGO=1` selects the Blocked AOCL DLP algorithm, recommended for best performance.
- Q8_0 mainly helps prompt processing (prefill); token generation may stay close to the standard CPU backend.
- On multi-socket systems manual NUMA binding may be needed, e.g. `numactl --cpunodebind=0 --membind=0 ./build/bin/llama-server ...`.

Example (from the page):

```bash
export ZENDNNL_MATMUL_ALGO=1
./build/bin/llama-server -m models/Llama-3.1-8B-Instruct.BF16.gguf --host 0.0.0.0 --port 9931 -t 64
```

## Checked

2026-11-04: confirmed against the llama.cpp `ZenDNN.md` backend page: build flags, `ZENDNN_ROOT`, supported operations, data types, `ZENDNNL_MATMUL_ALGO`, Q8_0 note, NUMA note. Removed: "use physical-core thread counts", the `llama-bench` comparison advice, and the "Ryzen and EPYC matmul library" wording that the page does not state that way.
Method: documentation only; no commands were run.
