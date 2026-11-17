---
id: computing-software.ai-ml-engineering.ollama.modelfile-template-system-message
name: modelfile-template-system-message
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [template, system, message, go-template]
level: advanced
status: docs-checked
description: "Control the prompt with TEMPLATE (Go template with .System, .Prompt, .Response), SYSTEM and seeded MESSAGE history."
sources:
  - https://docs.ollama.com/modelfile.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change exactly what text the model receives.

`TEMPLATE` is the full prompt template passed to the model, written in Go template syntax; it may include a system message, the user's message and the model's response, and its syntax may be model specific. Variables:

- `{{ .System }}`: the system message.
- `{{ .Prompt }}`: the user prompt.
- `{{ .Response }}`: the model response. When generating a response, text after this variable is omitted.

Example shape from the page:

```
TEMPLATE """{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
"""
```

`SYSTEM """<system message>"""` specifies the system message used in the template, if applicable; the page writes it with triple quotes.

`MESSAGE <role> <message>` seeds history; valid roles are `system` (alternative to `SYSTEM`), `user` (an example user message) and `assistant` (an example model reply). Several `MESSAGE` lines build a conversation that guides the model to answer in a similar way:

```
MESSAGE user Is Toronto in Canada?
MESSAGE assistant yes
MESSAGE user Is Sacramento in Canada?
MESSAGE assistant no
```

Check what a library model already uses with `ollama show --modelfile <model>` before overriding `TEMPLATE`; the page's example output shows the model's own template and stop parameters, so you can match its special tokens.

## Checked

2026-11-08. Template variables, the ChatML-style example, `SYSTEM`, `MESSAGE` roles and example, and `ollama show --modelfile` against the Modelfile page (docs.ollama.com/modelfile). Reworded the `.Response` behaviour to the page's wording (the draft's "generation starts where .Response appears" was an inference), and the draft's "triple quotes allow multi-line text" to what the page shows. The advice to match special tokens is the skill's own guidance, supported only by the example output on the page.

Method: documentation only; no commands were run.
