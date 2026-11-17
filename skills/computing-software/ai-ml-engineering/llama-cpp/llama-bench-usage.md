---
id: computing-software.ai-ml-engineering.llama-cpp.llama-bench-usage
name: llama-bench-usage
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, llama-bench, benchmark, prompt-processing, token-generation]
level: practitioner
status: docs-checked
description: "Benchmark prompt and generation speed with llama-bench: tests, defaults, list syntax and output formats."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/llama-bench/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# llama-bench

```bash
./build/bin/llama-bench -m /path/to/model.gguf -ngl 99
```

Defaults from the usage text: `-p` 512 prompt tokens, `-n` 128 generated tokens, `-r` 5 repetitions, `-b` 2048, `-ub` 512, `-ngl` -1, `-fa` auto, `-o md` (stdout). The default `-m` is a placeholder path under `models/7B/`, so always pass `-m` (or `-hf user/model[:quant]` to pull from Hugging Face).

Three test types:

- Prompt processing (pp): `-p N`.
- Text generation (tg): `-n N`.
- Prompt then generation (pg): `-pg pp,tg`.
- `-d N` (`--n-depth`) prefills the KV cache with N tokens before each test; rows then show `@ dN`.

Apart from `-r`, `-o` and `-v`, options can take several values, separated by commas (`-n 16,32`) or by repeating the option, and each pp/tg test runs over all combinations. Ranges are written `first-last`, `first-last+step` or `first-last*mult`:

```bash
llama-bench -m model.gguf -p 128,512 -n 64 -ngl 0,16,32 -t 4-16+4
```

Output formats via `-o`: `csv`, `json`, `jsonl`, `md`, `sql` (`-oe` sets the stderr format). SQL output is meant for importing into SQLite by piping it to the `sqlite3` tool. Other options: `--delay` seconds between tests, `--progress` indicators, `--no-warmup`, `--list-devices`, `-rpc` to register RPC devices, `-fitt` (fit the model to device memory with a per-device MiB margin, default off) and `-fitc`, `-dev`, `-sm`, `-mg`, `-ts`, `-ncmoe`, `-lm`.

Each test is repeated `-r` times and averaged; results are average tokens per second plus standard deviation, and json also contains each repetition's samples. The page notes that measurements do not include tokenization and sampling time. For options not described on the page it points to the completion example.

## Checked

Date: 2026-11-08. Confirmed against the llama-bench README (usage text, test types, range syntax, output formats). Removed: the claim that results are therefore "higher than end-to-end server throughput" and the advice on comparing runs, which are inferences not on the page.

Method: docs-only read of cited pages, 2026-11-08
