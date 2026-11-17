---
id: computing-software.ai-ml-engineering.ollama.modelfile-create-and-inspect
name: modelfile-create-and-inspect
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [create, show-modelfile, ollama-create, requires, ollamacreate]
level: intro
status: docs-checked
description: "Build a model from a Modelfile with ollama create -f and read an existing one with ollama show --modelfile."
sources:
  - https://docs.ollama.com/modelfile.md
  - https://docs.ollama.com/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: turn a Modelfile into a runnable local model and inspect it.

Create from a file:

```
ollama create mymodel -f ./Modelfile
```

Run it with `ollama run mymodel`. The CLI page lists `ollama create` among the model commands, with `-f` naming the Modelfile.

Inspect any installed model, including how a library model was built:

```
ollama show --modelfile llama3.2
```

The generated output itself says to replace its `FROM` line to build a new Modelfile from it.

Compatibility guards in the Modelfile:

- `REQUIRES 0.14.0` states the minimum Ollama version the model needs.
- `CAPABILITY decision` declares decision-trained weights (the CLI page shows `--ask` against a decision model).

Related commands from the CLI page: `ollama ls` lists installed models, `ollama rm <model>` deletes one, `ollama pull <model>` downloads one, and `ollama ps` shows what is loaded.

## Checked

2026-11-03. `ollama create -f`, `ollama show --modelfile`, `REQUIRES`, `CAPABILITY decision`, `ls`/`rm`/`pull`/`ps` against the Modelfile reference (docs.ollama.com/modelfile) and the CLI page. Removed the `ollama cp`/`push` sharing and cloud-API-creation claims (not on the fetched pages) and replaced the derived-model advice with what the generated Modelfile says.

Method: documentation only; no commands were run.
