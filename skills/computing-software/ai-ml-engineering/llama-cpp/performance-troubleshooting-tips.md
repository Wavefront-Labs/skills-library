---
id: computing-software.ai-ml-engineering.llama-cpp.performance-troubleshooting-tips
name: performance-troubleshooting-tips
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, performance, threads, gpu-offload-check, slow-generation]
level: intro
status: docs-checked
description: "Checklist for diagnosing slow token generation: verify GPU offload and tune thread count."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/development/token_generation_performance_tips.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Token generation performance tips

**Verify GPU offload.** Build with the GPU backend so the binary accepts `-ngl N` (`--n-gpu-layers N`). Setting N very large offloads the maximum possible number of layers, even if that is fewer than N:

```bash
./llama-cli -m "path/to/model.gguf" -ngl 200000 -p "Please sir, may I have some "
```

Before inference starts, the program prints diagnostic information showing whether work is offloaded to the GPU, including the number of layers offloaded and the VRAM used. If those lines are absent, the GPU is not being used.

**Verify the CPU is not oversaturated.** `-t N` (`--threads N`) must not be too large. If generation is extremely slow, try `-t 1`. If that is significantly faster, the CPU is oversaturated: set `-t` explicitly to the number of physical CPU cores, even when using a GPU. If in doubt, start at 1, double until performance stops improving, then scale back down.

## Checked

2026-11-04: confirmed against the llama.cpp `token_generation_performance_tips.md` page: `-ngl`, `-t` semantics and the 1-and-double procedure. Removed unconfirmed advice (`--numa`, `--fit`, memory-bandwidth and swapping remarks, `llama-bench` baseline, system-info feature line).
Method: documentation only; no commands were run.
