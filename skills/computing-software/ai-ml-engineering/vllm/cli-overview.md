---
id: computing-software.ai-ml-engineering.vllm.cli-overview
name: cli-overview
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [cli, vllm-serve, help, bench]
level: intro
status: docs-checked
description: "Know the vllm sub-commands, how to inspect flags with --help, and the human-readable integer suffixes."
sources:
  - https://docs.vllm.ai/en/latest/cli/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: find and use the right `vllm` sub-command and discover its flags.

Commands: `vllm {chat,complete,serve,launch,bench,collect-env,download-kernels,run-batch,preload}`.

`vllm serve MODEL` starts the OpenAI-compatible server. Examples from the guide: `--port 8100`, and `--uds /tmp/vllm.sock` to serve over a Unix domain socket.

Discover flags:

```bash
vllm serve --help=all            # every flag
vllm serve --help=ModelConfig    # one argument group
vllm serve --help=max-num-seqs   # one argument
vllm serve --help=max            # keyword search
```

Human-readable integers: `1k` = 1,000 (decimal), `1K` = 1,024 (binary), `1m` / `1M` = 1,000,000 / 1,048,576, `g/G` and `t/T` likewise. Decimal suffixes accept floats (`25.6k` = 25,600); binary suffixes need integers (`32K` = 32,768). Supported for `--max-model-len`, `--max-num-batched-tokens`, `--max-num-scheduled-tokens`, `--kv-cache-memory-bytes`, `--safetensors-prefetch-block-size`.

Client commands talk to a running server: `vllm chat` and `vllm complete` default to localhost; use `--url http://HOST:PORT/v1`, `--quick "prompt"` for one shot, and `--stats` to print TTFT and throughput after each response.

`vllm launch render MODEL` starts the rendering server component. `vllm bench` needs `pip install vllm[bench]` and offers `forward`, `latency`, `serve`, `throughput`.

## Checked

2026-11-03. Confirmed against the vLLM CLI Guide (docs.vllm.ai/en/latest/): command list, help forms, human-readable integer suffixes, chat/complete flags, launch render and bench. Reworded vllm launch render to the page's wording.

Method: documentation only; no commands were run.
