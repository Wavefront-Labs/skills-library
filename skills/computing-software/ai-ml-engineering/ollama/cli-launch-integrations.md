---
id: computing-software.ai-ml-engineering.ollama.cli-launch-integrations
name: cli-launch-integrations
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [ollama-launch, claude-code, codex, opencode, ollamalaunch]
level: practitioner
status: docs-checked
description: "Start coding agents against Ollama models with ollama launch, choosing a model and passing arguments through."
sources:
  - https://docs.ollama.com/cli.md
  - https://docs.ollama.com/quickstart.md
  - https://docs.ollama.com/integrations/claude-code.md
  - https://docs.ollama.com/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run a coding agent on local or cloud Ollama models.

From your project directory:

```
ollama launch claude
ollama launch codex
ollama launch opencode
```

The CLI page lists integrations OpenCode, Claude Code, Codex, VS Code and Droid, and `ollama launch` with no argument is the interactive way to pick one. Ollama offers to install Claude Code or OpenCode if needed; Codex CLI must be installed first, per the quickstart. Choose a model when prompted.

Options named on the CLI page: `--model` selects the model (`ollama launch claude --model qwen3.5`) and `--config` configures an integration without launching it (`ollama launch droid --config`). The Claude Code page shows a non-interactive form for scripts, Docker or CI:

```
ollama launch claude --model gemma4:cloud --yes -- -p "how does this repository work?"
```

`--yes` skips selectors, pulls the model when needed and requires `--model`; arguments after `--` are passed directly to Claude Code.

Context: the Claude Code page says to choose a local model and set a 64k+ context window, and for larger repositories to set the context length to 64k or higher. The FAQ sets the default with `OLLAMA_CONTEXT_LENGTH` (its example is `OLLAMA_CONTEXT_LENGTH=8192 ollama serve`); see the context-length skill.

Direct cloud use (no Ollama install) is also documented: set `ANTHROPIC_BASE_URL=https://ollama.com` with `ANTHROPIC_AUTH_TOKEN` set to your API key, choose a cloud model that supports tools, and note that hosted WebSearch and advanced tool controls are not fully supported.

Running bare `ollama` opens setup prompts, where you can sign in for cloud models or choose a local model.

## Checked

2026-11-08. Integration list, `--model`, `--config` and interactive launch against the CLI page (docs.ollama.com/cli); install offers, Codex prerequisite and bare `ollama` setup against the quickstart; `--yes` behaviour, the `--` pass-through, 64k context advice and direct-cloud variables and limits against the Claude Code page; `OLLAMA_CONTEXT_LENGTH` against the FAQ. Added the `--yes` semantics and cloud variables; removed the implied specific `OLLAMA_CONTEXT_LENGTH=64000` value, which no page gives.

Method: documentation only; no commands were run.
