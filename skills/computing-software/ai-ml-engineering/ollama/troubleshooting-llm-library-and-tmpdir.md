---
id: computing-software.ai-ml-engineering.ollama.troubleshooting-llm-library-and-tmpdir
name: troubleshooting-llm-library-and-tmpdir
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [llm-library, ollama-llm-library, ollama-tmpdir, cpu-avx2]
level: advanced
status: docs-checked
description: "Force a specific compute library with OLLAMA_LLM_LIBRARY and move temp files with OLLAMA_TMPDIR on noexec systems."
sources:
  - https://docs.ollama.com/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: work around library autodetection and unusable temp directories.

Ollama bundles several LLM libraries compiled for different GPUs and CPU vector features and picks the best for your system. If autodetection fails or crashes, override it with `OLLAMA_LLM_LIBRARY`. The server log lists the available ones, in a line like:

```
Dynamic LLM libraries [rocm_v6 cpu cpu_avx cpu_avx2 cuda_v11 rocm_v5]
```

Force a CPU library with AVX2 support, for example on a CUDA machine:

```
OLLAMA_LLM_LIBRARY="cpu_avx2" ollama serve
```

Check CPU features on Linux with `cat /proc/cpuinfo | grep flags | head -1`.

Temporary files: Ollama stores temporary executable files in a temp location. If that is mounted `noexec`, set `OLLAMA_TMPDIR` to a location writable by the user Ollama runs as.

Installing an older release when a new one regresses: `OLLAMA_VERSION=0.5.7` with the Linux install script.

The page calls this override experimental.

Related: `OLLAMA_VULKAN=0` or `GGML_VK_VISIBLE_DEVICES=-1` disables Vulkan GPUs (GPU page).

## Checked

2026-11-03. `OLLAMA_LLM_LIBRARY`, library names, `/proc/cpuinfo` check, `OLLAMA_TMPDIR`, noexec and `OLLAMA_VERSION` install against the troubleshooting page (docs.ollama.com/troubleshooting); Vulkan disable against the GPU page (docs.ollama.com/gpu). Removed the unsupported `CUDA_VISIBLE_DEVICES=-1` claim and an invented motivation for the CPU override.

Method: documentation only; no commands were run.
