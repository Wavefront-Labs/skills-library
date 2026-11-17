---
id: computing-software.ai-ml-engineering.ollama.modelfile-instructions
name: modelfile-instructions
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [modelfile, instructions, from, parameter, template]
level: intro
status: docs-checked
description: "Know the Modelfile instruction set: FROM, PARAMETER, TEMPLATE, SYSTEM, LICENSE, MESSAGE, REQUIRES and CAPABILITY."
sources:
  - https://docs.ollama.com/modelfile.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write a valid Modelfile blueprint for a custom model.

A Modelfile is the blueprint for creating and sharing models with Ollama. The documented instructions are:

- `FROM` (required): the base model.
- `PARAMETER`: sets a runtime option.
- `TEMPLATE`: the full prompt template sent to the model.
- `SYSTEM`: the system message in the template.
- `LICENSE`: the legal licence.
- `MESSAGE`: a message history to seed the conversation.
- `REQUIRES`: the minimum Ollama version, for example `REQUIRES 0.14.0`.
- `CAPABILITY`: declares a capability. `CAPABILITY decision` marks weights that were trained for decision output.

The page says the Modelfile is not case sensitive; the examples use uppercase so instructions are easier to tell from arguments. Instructions can appear in any order, though the examples start with `FROM`.

A minimal example:

```
FROM llama3.2
PARAMETER temperature 1
SYSTEM """
You are Mario from super mario bros, acting as an assistant.
"""
```

Build and run it:

```
ollama create mario -f ./Modelfile
ollama run mario
```

`ollama show --modelfile <model>` prints the Modelfile of an existing model, which is the documented way to see what a base model uses before you override its template or parameters.

## Checked

2026-11-03. Instruction list, `REQUIRES`, `CAPABILITY decision`, case insensitivity, ordering and `ollama show --modelfile` confirmed against the Modelfile reference (docs.ollama.com/modelfile). Nothing removed.

Method: documentation only; no commands were run.
