---
id: computing-software.ai-ml-engineering.llama-cpp.speculative-eagle3-dflash
name: speculative-eagle3-dflash
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, eagle3, dflash, dspark, mtp-draft]
level: sme
status: docs-checked
description: "Prepare and use EAGLE-3, DFlash and DSpark draft models for speculative decoding."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/speculative.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EAGLE-3, DFlash and DSpark drafts

These draft types use a small draft model trained for one specific target model, not a generic small LLM.

- `--spec-type draft-eagle3`: a one-layer transformer that reads the target's hidden states; it shares the target's tokenizer.
- `--spec-type draft-dflash`: a block-diffusion draft that emits a whole block of draft tokens in one forward pass.
- `--spec-type draft-dspark`: DFlash plus a semi-autoregressive Markov head. Currently only drafts with a Qwen3 backbone are supported.
- `--spec-type draft-mtp`: uses Multi Token Prediction heads from the main model.

Convert the draft checkpoint with `--target-model-dir` so it inherits the target's tokenizer (and, for DFlash/DSpark, token embeddings):

```bash
python convert_hf_to_gguf.py AngelSlim/Qwen3-4B_eagle3 \
    --target-model-dir Qwen/Qwen3-4B --outtype bf16 --outfile Qwen3-4B-eagle3.gguf

llama-server -m Qwen3-4B.gguf -md Qwen3-4B-eagle3.gguf --spec-type draft-eagle3
```

DFlash and DSpark runs use `-fa on --jinja` and set `--spec-draft-n-max` (the page uses 15 for DFlash and 7 for DSpark); `--spec-draft-n-max` is clamped to the draft model's trained block size. For DSpark, `--spec-draft-p-min P` truncates a drafted block at the first position whose predicted acceptance falls below P (default 0 = disabled; values above 0 need a draft with a confidence head).

In router mode, `POST /models` accepts `sidecars`, the kinds pulled with the model: `mmproj` (the default) and the draft heads `mtp`, `dflash`, `eagle3` and `dspark`.

## Checked

2026-11-04: confirmed against the llama.cpp `speculative.md` page (EAGLE-3, DFlash and DSpark sections, `--spec-type` table) and the llama-server README (`sidecars` kinds). Replaced the generic conversion command with the page's example and removed the "thin-source" note.
Method: documentation only; no commands were run.
