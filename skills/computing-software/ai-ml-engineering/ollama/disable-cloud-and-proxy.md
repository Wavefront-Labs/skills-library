---
id: computing-software.ai-ml-engineering.ollama.disable-cloud-and-proxy
name: disable-cloud-and-proxy
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [disable-cloud, ollama-no-cloud, https-proxy, server-json]
level: practitioner
status: docs-checked
description: "Run local-only by disabling Ollama cloud features with OLLAMA_NO_CLOUD or server.json and route pulls through HTTPS_PROXY."
sources:
  - https://docs.ollama.com/faq.md
  - https://docs.ollama.com/cloud.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep prompts local and work behind a proxy.

Disable cloud features either way:

- environment: `OLLAMA_NO_CLOUD=1`
- config: set `disable_ollama_cloud` to true in `~/.ollama/server.json`

Restart Ollama after changing configuration. When active the server log shows `Ollama cloud disabled: true`. The FAQ says that disabling cloud features means losing Ollama's cloud models and web search. The cloud page says that to use only local models you should disable cloud features this way, and that cloud prompts and responses are processed to answer requests and not used to train models.

Proxy: Ollama downloads models over HTTPS, so set `HTTPS_PROXY` (for example `HTTPS_PROXY=https://proxy.example.com`) for the server process, and make sure the proxy certificate is installed as a system certificate. The FAQ says to avoid setting `HTTP_PROXY`, because that can break client connections to the server. In Docker pass it with `-e HTTPS_PROXY=https://proxy.example.com`; if the proxy uses its own certificate, the FAQ shows a Dockerfile that copies it into the image and runs `update-ca-certificates`.

Use the per-OS steps in the environment-variable skill to make either setting persistent.

Related sign-in state: `ollama signin` adds your key to ollama.com, which the FAQ says is needed to push models, pull private models and run models in Ollama's cloud. In the Ollama app or CLI, cloud models use a `:cloud` name such as `gemma4:cloud` (cloud page).

## Checked

2026-11-08. `OLLAMA_NO_CLOUD`, `server.json`, the log line, lost features, `HTTPS_PROXY` and `HTTP_PROXY` advice, the Docker proxy options and `ollama signin` against the FAQ (docs.ollama.com/faq); local-only advice, data handling and the `:cloud` naming against the cloud page (docs.ollama.com/cloud). Removed the `ollama signout` claim (not on either page) and corrected the `-cloud` suffix to `:cloud`.

Method: documentation only; no commands were run.
