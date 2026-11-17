---
id: computing-software.ai-ml-engineering.llama-cpp.llama-cli-options
name: llama-cli-options
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, llama-cli, conversation-mode, single-turn, server-base]
level: intro
status: docs-checked
description: "Use llama-cli for chat from the terminal, including system prompts, single-turn mode and attaching media."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/cli/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# llama-cli

`llama-cli` is the interactive chat tool. Basic use:

```bash
llama-cli -m /path/to/model.gguf
llama-cli -hf ggml-org/GLM-4.7-Flash-GGUF:Q4_K_M
```

`-hf` takes `<user>/<model>[:quant]`; the quant is optional and case-insensitive, defaults to Q4_K_M, or falls back to the first file in the repo. An mmproj file is also downloaded automatically if available (add `--no-mmproj` to disable).

Options from the README:

- `-sys, --system-prompt PROMPT` and `-sysf, --system-prompt-file FNAME`: system prompt (applies depending on the chat template).
- `-st, --single-turn`: run the conversation for a single turn, then exit; not interactive if the first turn is predefined with `--prompt`.
- `-mli, --multiline-input`: write or paste multiple lines without ending each in `\`.
- `--image`, `--audio`, `--video FILE`: path to an image, audio or video file for multimodal models; comma-separated values for several files. Related: `--image-min-tokens`, `--image-max-tokens`, `--video-fps` (default 4.0), `--video-timestamp-interval` (default 5000 ms), `--video-ffmpeg-dir`.
- `--simple-io`: basic IO for better compatibility in subprocesses and limited consoles.
- `--show-timings` / `--no-show-timings`: timing information after each response (default true).
- `--server-base URL`: connect to this server instead of starting a new one, for example `http://localhost:9931`.
- `--jinja` / `--no-jinja`: the Jinja chat template engine (default enabled). `--chat-template` and `--chat-template-file` set a custom template; the default comes from the model metadata.
- Reasoning: `-rea, --reasoning [on|off|auto]` (default auto, detected from the template), `--reasoning-budget N` (-1 unrestricted, 0 immediate end, N>0 token budget; default -1), `--reasoning-format` (`none`, `deepseek`, `deepseek-legacy`), `--reasoning-effort`.
- Common parameters: `-c` (default 0, meaning loaded from the model), `-n` (default -1, infinite), `-b` 2048, `-ub` 512, `-fa` auto.

For raw text completion without a chat template use `llama-completion`. Run `llama-cli --help` for the full list.

## Checked

Date: 2026-11-08. Confirmed against the llama-cli README option tables. Removed: `cmake --build build -t llama-cli` (not on the page) and the statement that sampling flags match llama-server.

Method: docs-only read of cited pages, 2026-11-08
