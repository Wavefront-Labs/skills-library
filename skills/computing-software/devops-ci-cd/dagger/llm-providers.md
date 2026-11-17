---
id: computing-software.devops-ci-cd.dagger.llm-providers
name: llm-providers
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, llm, ai, anthropic, openai, gemini, ollama, environment-variables]
level: practitioner
status: docs-checked
description: "Configure Dagger LLM access through environment variables or .env for Anthropic, OpenAI, Gemini, Azure, Bedrock via LiteLLM, Docker Model Runner and Ollama."
sources: [https://docs.dagger.io/0.21/reference/configuration/llm]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configuring LLM providers for Dagger

Goal: give Dagger's LLM type a provider. Dagger reads standard environment variables from the environment or a `.env` file in the current directory (parent-directory `.env` files are not supported yet). `.env` values can use Dagger secret syntax, e.g. `OPENAI_API_KEY="op://Private/OpenAI API Key/password"`. Dagger 0.21 docs.

## Per provider

- Anthropic: `ANTHROPIC_API_KEY` (required), `ANTHROPIC_MODEL` (default `claude-sonnet-4-5`).
- OpenAI: `OPENAI_API_KEY` (required), `OPENAI_MODEL` (default `gpt-4o`), optional `OPENAI_BASE_URL` (compatible endpoints) and `OPENAI_AZURE_VERSION`.
- Gemini: `GEMINI_API_KEY` (required), `GEMINI_MODEL` (default `gemini-2.0-flash`).
- Azure OpenAI: `OPENAI_BASE_URL` (e.g. `https://your-azure-openai-resource.cognitiveservices.azure.com`), `OPENAI_API_KEY` (deployment key), optional `OPENAI_MODEL` and `OPENAI_AZURE_VERSION` (e.g. `2024-12-01-preview`).
- Amazon Bedrock: via an OpenAI-compatible proxy such as LiteLLM. In its `config.yml` define `model_name` and, under `litellm_params`, `model: bedrock/...`, `aws_region_name` and `drop_params: true` (required, because the OpenAI API's `seed` and `parallel_tool_calls` parameters are generally unsupported by Bedrock models). Set `OPENAI_MODEL` to the `model_name` and `OPENAI_BASE_URL` to the host IPv4 address and LiteLLM port, e.g. `http://172.20.2.97:4000`.
- Docker Model Runner: enable it in Docker Desktop, `docker model pull ai/qwen2.5`, then:

```shell
OPENAI_BASE_URL=http://model-runner.docker.internal/engines/v1/
OPENAI_MODEL=index.docker.io/ai/qwen2.5:7B-F16
OPENAI_DISABLE_STREAMING=true
```

  This assumes the engine runs on the same machine as Docker Desktop; otherwise replace the host name.
- Ollama: run `OLLAMA_HOST="0.0.0.0:11434" ollama serve` (default context length is 2048; raise via `OLLAMA_CONTEXT_LENGTH`), `ollama pull <model>` (the page suggests tool-capable models such as `qwen2.5-coder:14b`), find the host IP (`ifconfig | grep "inet " | grep -v 127.0.0.1`, or `ip addr ...` on older Linux), then set `OPENAI_BASE_URL=http://<ip>:11434/v1/` and `OPENAI_MODEL=<model>`.

## Gotchas

- Ollama: use the host's real IP, not `localhost`, because the LLM type runs inside the engine; the trailing `/` in the URL is mandatory.
- CLI flags `--model` and `--allow-llm` are in computing-software.devops-ci-cd.dagger.cli-running-functions.

## Checked

2026-11-07

Read reference/configuration/llm.mdx in full (live slug /reference/configuration/llm, returns 200). Confirmed the .env lookup rule and the parent-directory limitation, the 1Password secret example, every provider variable with its required or optional status and the stated defaults (claude-sonnet-4-5, gpt-4o, gemini-2.0-flash), the Azure variables and example version, the LiteLLM Bedrock config and warning, the Docker Model Runner variables, and the Ollama steps (OLLAMA_HOST, 2048 context default, OLLAMA_CONTEXT_LENGTH, qwen2.5-coder:14b, host IP commands, trailing slash). Corrected the Bedrock sentence: drop_params sits under litellm_params in the page's sample, and the reason refers to the OpenAI API parameters. Model defaults are values stated by the page at the time of reading and may change.

Method: documentation only; no commands were run.
