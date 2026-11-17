---
id: computing-software.ai-ml-engineering.llama-cpp.rpc-server-distributed
name: rpc-server-distributed
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, rpc, distributed-inference, ggml-rpc-server, remote-backend]
level: advanced
status: docs-checked
description: "Offload layers to remote machines with ggml-rpc-server and the --rpc client flag, with the security warning."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/rpc/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RPC backend

Warning from the docs: the RPC backend is at a proof-of-concept stage, fragile and insecure. Never run the RPC server on an open network or in a sensitive environment.

On each remote host and on the main host, add `-DGGML_RPC=ON` to the build options (plus the backends for the local accelerators, e.g. `-DGGML_CUDA=ON`):

```bash
cmake .. -DGGML_CUDA=ON -DGGML_RPC=ON
cmake --build . --config Release
```

On each worker, `ggml-rpc-server` exposes all available accelerator devices (a single CPU device if there are none):

```bash
bin/ggml-rpc-server -p 50052
```

The default endpoint is `127.0.0.1:50052`. Limit the exposed devices with `CUDA_VISIBLE_DEVICES` or `--device CUDA0`. Add `-c` to enable a local cache for large tensors, which speeds up model loading; it lives in `$HOME/.cache/llama.cpp/rpc` unless `LLAMA_CACHE` is set.

On the main host, point `llama-cli` or `llama-server` at each worker with `--rpc`:

```bash
llama-cli -hf ggml-org/gemma-3-1b-it-GGUF -ngl 99 --rpc 192.168.88.10:50052,192.168.88.11:50052
```

By default weights and KV cache are spread across all local and remote devices in proportion to each device's available memory; override with `--tensor-split`.

RDMA (RoCEv2 on Linux, Thunderbolt 5 on macOS) is negotiated at handshake and falls back to TCP; set `GGML_RPC_NO_RDMA=1` on either peer to force TCP. `GGML_RPC_DEBUG` sets log verbosity: unset/0 only warnings and errors, 1 high-level events, 2 per-command trace, 3 fine detail. On the client also pass `-lv 5`, or the debug records are dropped.

## Checked

2026-11-04: confirmed against the llama.cpp `tools/rpc/README.md` page: warning, build flag, `-p`, default endpoint, `--device`, `-c` cache path, `--rpc`, `--tensor-split` behaviour, RDMA and `GGML_RPC_DEBUG`. Removed the `-H` host flag and the `llama-bench --rpc` claim (neither is on the page) and the repeated closing paragraph.
Method: documentation only; no commands were run.
