---
id: computing-software.ai-ml-engineering.vllm.troubleshooting-debug-logging
name: troubleshooting-debug-logging
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [troubleshooting, vllm-logging-level, cuda-launch-blocking, enforce-eager, load-format-dummy, forked-pdb]
level: practitioner
status: docs-checked
description: "Isolate hangs, slow loads and CUDA crashes with debug environment variables, dummy load and eager mode."
sources:
  - https://docs.vllm.ai/en/latest/usage/troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: find where a stuck or crashing vLLM instance is failing.

Isolate model problems first:
- Hang while downloading: fetch the model with the `hf` CLI first and pass vLLM the local path.
- Hang loading from disk: large models are slow on shared or network filesystems, so prefer a local disk and watch CPU memory for swapping.
- `--load-format dummy` skips loading real weights, showing whether download or load is the bottleneck.
- Out of memory: apply the conserving-memory options.

Debug environment variables:
- `VLLM_LOGGING_LEVEL=DEBUG`: more logging.
- `VLLM_LOG_STATS_INTERVAL=1.`: frequent stats on running queue, waiting queue and cache hits.
- `CUDA_LAUNCH_BLOCKING=1`: identify the CUDA kernel at fault.
- `NCCL_DEBUG=TRACE`: more NCCL logging.
- `VLLM_TRACE_FUNCTION=1`: records every function call, but slows token generation by over 100x.

Unset these after debugging; lingering settings slow the system.

A crash near `self.graph.replay()` is a CUDA error inside CUDAGraph. Add `--enforce-eager` (or `enforce_eager=True`) to disable CUDA graphs and expose the failing operation.

Breakpoints: plain `pdb` fails in subprocesses (`bdb.BdbQuit`). Use `pip install fpdb` and `__import__('fpdb').ForkedPdb().set_trace()`, or set `VLLM_ENABLE_V1_MULTIPROCESSING=0` so the scheduler shares your process.

If quality changed after v0.8.0, defaults now come from the model's `generation_config.json`; try `--generation-config vllm` for the old defaults.

## Checked

2026-11-03. Confirmed against the Troubleshooting page (docs.vllm.ai/en/latest/): download/load hangs, debug environment variables, graph.replay crash, breakpoints and generation_config note.

Method: documentation only; no commands were run.
