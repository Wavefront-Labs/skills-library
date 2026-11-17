---
id: computing-software.ai-ml-engineering.ollama.modelfile-from-sources
name: modelfile-from-sources
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [from, gguf, safetensors, split-gguf]
level: practitioner
status: docs-checked
description: "Point FROM at a model name, a Safetensors directory or a GGUF file, including split GGUF shards with a wildcard."
sources:
  - https://docs.ollama.com/modelfile.md
  - https://docs.ollama.com/import.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose the right base for a new model.

`FROM <model name>:<tag>` builds on an existing model, for example `FROM llama3.2`. `FROM` is the only required instruction.

Importing weights is also done with `FROM`:

- A Safetensors directory: `FROM <model directory>`, which should contain Safetensors weights for a supported architecture. The import page also allows `FROM .` when the Modelfile sits in the weights directory, then `ollama create my-model`.
- A GGUF file: `FROM ./ollama-model.gguf`. The path can be absolute or relative to the Modelfile.
- A split GGUF: keep the original split filenames and use a wildcard such as `FROM ./model-*.gguf`; shards can also be listed with separate `FROM` instructions.

Then build and run:

```
ollama create example -f Modelfile
ollama run example
```

Quantization gotcha: Ollama does not quantize GGUF models on import. Prepare and quantize them first with a GGUF tool such as llama.cpp's `llama-quantize`.

For a model that is already in the library, skip all of this and name it directly in `FROM`.

## Checked

2026-11-08. `FROM` forms, absolute-or-relative GGUF path, split GGUF wildcard and separate-`FROM` option against the Modelfile page (docs.ollama.com/modelfile); `FROM .`, `ollama create`, no import quantization and `llama-quantize` against the import page. Removed the `vicuna-33b` example (not on either page) and the vague statement about converting models "not already in the files the page expects"; the pages only say the directory must hold Safetensors weights for a supported architecture.

Method: documentation only; no commands were run.
