---
id: computing-software.ai-ml-engineering.ollama.import-and-share-models
name: import-and-share-models
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [import, safetensors, gguf, ollama-push, share, ollamapush]
level: practitioner
status: docs-checked
description: "Import Safetensors or GGUF weights with ollama create, then share with ollama cp and ollama push under your username."
sources:
  - https://docs.ollama.com/import.md
  - https://docs.ollama.com/api/create.md
  - https://docs.ollama.com/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: bring your own weights into Ollama and publish them.

Import:

- Safetensors: put `FROM /path/to/safetensors/directory` (or `FROM .` when the Modelfile is in the weights directory) in a Modelfile, run `ollama create my-model`, then `ollama run my-model`.
- GGUF: `FROM /path/to/file.gguf` in a Modelfile, then `ollama create my-model`.
- Split GGUF: keep the original split filenames and use a wildcard such as `FROM /path/to/model-*.gguf`.

Ollama does not quantize GGUF on import; quantize beforehand with llama.cpp's `llama-quantize`. The `/api/create` request has a `quantize` field (for example `nvfp4`) for quantization during import.

Template and system prompt can be set in the same Modelfile (see the Modelfile skills).

Sharing on ollama.com:

1. Create an account at ollama.com; the username becomes part of the model name (for example `jmorganca/mymodel`).
2. Add your Ollama public key on the Ollama Keys settings page. It is `~/.ollama/id_ed25519.pub` on macOS and `/usr/share/ollama/.ollama/id_ed25519.pub` on Linux (in the `.ollama` folder of your user profile on Windows).
3. Copy the model to your namespace:

```
ollama cp mymodel myuser/mymodel
```

4. Push it:

```
ollama push myuser/mymodel
```

Others can then `ollama run myuser/mymodel`. Per the FAQ, `ollama signin` is one way to add the key to your account.

## Checked

2026-11-08. Safetensors and GGUF import, split wildcard, no import-time quantization, account/key/cp/push steps and run command against the import page (docs.ollama.com/import); `quantize` against the create reference; key paths and `ollama signin` against the FAQ. Replaced the draft's relative GGUF path and `-f Modelfile` form with the import page's own form, and added the username-in-model-name note and the Windows key path. Nothing else removed.

Method: documentation only; no commands were run.
