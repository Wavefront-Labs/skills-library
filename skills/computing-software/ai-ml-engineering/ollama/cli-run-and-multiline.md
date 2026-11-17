---
id: computing-software.ai-ml-engineering.ollama.cli-run-and-multiline
name: cli-run-and-multiline
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [ollama-run, multiline, prompt, embeddings-cli, ollamarun]
level: intro
status: docs-checked
description: "Run models interactively with ollama run: one-shot prompts, triple-quote multiline input, files and embeddings from the CLI."
sources:
  - https://docs.ollama.com/cli.md
  - https://docs.ollama.com/quickstart.md
  - https://docs.ollama.com/faq.md
  - https://docs.ollama.com/capabilities/vision.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: chat with a model from the terminal.

```
ollama run gemma4
```

starts a chat (the quickstart's example is `ollama run gemma4:e2b`, which downloads the model first). Type `/bye` to leave. A prompt can follow the model name for a one-shot answer, as the CLI page shows for images:

```
ollama run gemma4 "What's in this image? <path-to-image>"
```

For multiline input, wrap text in triple quotes:

```
>>> """Hello,
... world!
... """
```

Multimodal models take image paths in the prompt; the vision page shows `ollama run gemma4 ./image.png what is in this image?`.

Embeddings: `ollama run embeddinggemma "Hello world"` prints the output as a JSON array, and the CLI page also shows piping text: `echo "Hello world" | ollama run nomic-embed-text`.

Session parameter: `/set parameter num_ctx 4096` changes the context window for the session (FAQ).

The CLI page also shows decision-model flags `--ask`, `--choice` and `--level`, and `--voice` for a speech model.

To only download a model, use `ollama pull`.

## Checked

2026-11-08. `ollama run`, multiline `"""`, image prompt, embeddings, piping, `--ask`/`--choice`/`--level` and `--voice` against the CLI page (docs.ollama.com/cli); `/bye` against the quickstart; `/set parameter num_ctx` against the FAQ; the `./image.png` form against the vision page. Removed the `$(cat README.md)` example, `/clear`, Ctrl+D and `--hidethinking`, none of which appear on the cited pages. Updated model names to those the pages use.

Method: documentation only; no commands were run.
