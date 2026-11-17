---
id: computing-software.ai-ml-engineering.vllm.serve-config-file
name: serve-config-file
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [config-file, yaml, vllm-serve, precedence]
level: practitioner
status: docs-checked
description: "Load vllm serve arguments from a YAML config file and understand command-line precedence."
sources:
  - https://docs.vllm.ai/en/latest/configuration/serve_args/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep `vllm serve` arguments in a YAML file instead of a long command line.

Argument names in the file must be the long form of the CLI flags, written without the leading dashes:

```yaml
# config.yaml
model: meta-llama/Llama-3.1-8B-Instruct
host: "127.0.0.1"
port: 6379
uvicorn-log-level: "info"
```

Start the server with:

```bash
vllm serve --config config.yaml
```

Precedence is `command line > config file values > defaults`. If an argument is given both ways the command-line value wins; for example in `vllm serve SOME_MODEL --config config.yaml`, SOME_MODEL overrides `model` from the file.

vLLM Recipes (recipes.vllm.ai) can be converted into a `config.yaml` plus an `env.sh` using the recipes conversion tool in the repository (see its README under tools/recipes). Source the generated environment first, then start the server:

```bash
source env.sh
vllm serve --config config.yaml
```

The CLI Reference page lists the available options.

## Checked

Method: 2026-11-08 read the vLLM Server Arguments page (docs source markdown) in full.
Changes: dropped the Docker mount/entrypoint recipe and the `--help=all` tip because the page does not state them; pointed to the CLI Reference instead. The YAML format, precedence and recipes claims were unchanged and match the page.
