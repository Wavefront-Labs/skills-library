---
id: computing-software.ai-ml-engineering.llama-cpp.cvector-generator-control-vectors
name: cvector-generator-control-vectors
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, control-vector, cvector-generator, pca, steering]
level: advanced
status: docs-checked
description: "Create control vectors with cvector-generator and apply them with scaling and layer ranges."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/cvector-generator/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Control vectors

The `cvector-generator` example generates a control vector from a GGUF model. Examples from the README:

```bash
# CPU only
./cvector-generator -m ./llama-3.Q4_K_M.gguf

# With GPU
./cvector-generator -m ./llama-3.Q4_K_M.gguf -ngl 99

# With advanced options
./cvector-generator -m ./llama-3.Q4_K_M.gguf -ngl 99 --pca-iter 2000 --pca-batch 100

# Using mean value instead of PCA
./cvector-generator -m ./llama-3.Q4_K_M.gguf --method mean

# See the "cvector" section of the help
./cvector-generator -h
```

The README does not list the prompt-file options; read them from `-h`. If a prompt spans several lines, escape each newline as `\n` so it stays on one line, for example `<|im_start|>system\nAct like a person who is extremely happy.<|im_end|>`.

Apply the output file with `llama-cli`, scaled and limited to a layer range (the README notes the vector works better on layers higher than 10):

```bash
./llama-cli -m ./llama-3.Q4_K_M.gguf -p "<prompt>" --special \
  --control-vector-scaled ./control_vector.gguf 0.8 --control-vector-layer-range 10 31
```

## Checked

2026-11-04: confirmed against the llama.cpp `tools/cvector-generator/README.md` page: binary name, `-ngl`, `--pca-iter`, `--pca-batch`, `--method mean`, newline escaping, `--control-vector-scaled`, `--control-vector-layer-range`, the layer-10 tip. Removed `--positive-file`/`--negative-file`, `-o`, the `llama-` binary prefix, the stated PCA defaults, `--control-vector` and the closing paragraph (none on the page).
Method: documentation only; no commands were run.
