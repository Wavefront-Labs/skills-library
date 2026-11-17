---
id: computing-software.ai-ml-engineering.llama-cpp.llama-completion-interactive
name: llama-completion-interactive
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, llama-completion, interactive-mode, prompt-cache, infinite-generation]
level: practitioner
status: docs-checked
description: "Raw text completion and interactive mode with llama-completion, including reverse prompts and context handling."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/completion/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# llama-completion

Text generation tool. The README's quick start disables conversation mode explicitly:

```bash
./llama-completion -m models/gemma-1.1-7b-it.Q4_K_M.gguf -no-cnv --prompt "Once upon a time"
```

Options (from the README):

- `-cnv, --conversation` / `-no-cnv, --no-conversation`: conversation mode does not print special tokens or suffix/prefix, uses the default or provided chat template and enables interactive mode; default is on if a chat template is available.
- `-i, --interactive`: interactive mode (default false). Press Ctrl+C to interject, type input and press Return; end a line with `\` to continue on another line.
- `-if, --interactive-first`: interactive mode that waits for input right away.
- `-r, --reverse-prompt PROMPT`: halt generation at the prompt and return control in interactive mode. It does not work when the string ends with a space; use `--in-prefix " "` to add one. `--in-suffix` adds text after the input (after the automatic newline), for example `-r "User:" --in-prefix " " --in-suffix "Assistant:"`. With `--in-prefix` or `--in-suffix` the chat template is disabled.
- `-n N`: tokens to predict, default -1 (infinite), -2 until the context is filled. With -1, when the context fills, half of the tokens after `--keep` are discarded and the context is re-evaluated, which can cause a long pause; `-2` stops immediately when full; `--no-context-shift` also stops generation when the window is full (the table lists `--context-shift` as default disabled).
- `-c N`: context size; the options table default is 0, meaning loaded from the model (some prose on the page still says 4096). For a fine-tune extended by RoPE scaling, set `--ctx-size` and `--rope-scale` (the page's example: a 4k model fine-tuned to 32k has factor 8, so `--ctx-size 32768 --rope-scale 8`).
- `--keep N`: tokens kept from the initial prompt when the context resets; default 0, -1 keeps all.
- `--prompt-cache FNAME`: cache prompt state for faster startup; `--prompt-cache-all` also saves user input and generations; `--prompt-cache-ro` uses the cache without updating it.
- `-f, --file FNAME`: read the prompt from a file.
- `--ignore-eos` keeps generating past an end-of-sequence token.

LoRA: `--lora FNAME` (scale 1.0, repeatable or comma-separated) and `--lora-scaled FNAME:SCALE`. Adapters must be GGUF (convert with `convert-lora-to-gguf.py`), are loaded separately and applied during inference rather than merged, so mmap loading still works.

## Checked

Date: 2026-11-08. Confirmed against the llama-completion README (options table, interactive mode, context management, generation flags, LoRA). Corrected: context default (table says 0, not 4096), `-n -2` meaning, and the claim that older tokens are always discarded keeping the first `--keep`.

Method: docs-only read of cited pages, 2026-11-08
