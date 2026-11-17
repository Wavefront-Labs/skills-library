---
id: computing-software.ai-ml-engineering.open-webui.trace-chats-with-langfuse-filter
name: trace-chats-with-langfuse-filter
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, integrations, langfuse, observability, filter-function]
level: practitioner
status: docs-checked
description: "Send every Open WebUI chat reply to Langfuse by installing the Langfuse filter function, setting its valves, scoping it globally or per model, and reading the traces."
sources:
  - https://docs.openwebui.com/tutorials/integrations/monitoring/langfuse
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trace chats with the Langfuse filter

Goal: token usage, latency, cost per user/model and sessions for every reply, in Langfuse.

## How it works
A Filter Function: `inlet` starts a Langfuse generation (name `chat-reply`, input = messages, model = base model ID behind a workspace model, metadata `model_name`, user = user email, session = chat ID, trace name `Open WebUI chat`, tag `open-webui`); `outlet` ends it with the reply and `usage` (`input_tokens`, `output_tokens`, `total_tokens`).

## Steps
1. Create a Langfuse project (cloud.langfuse.com or self-hosted) and an API key pair: public `pk-lf-...`, secret `sk-lf-...`, plus the Langfuse URL for your region/server.
2. Admin Panel > Functions > **+** > New Function; paste the Filter code from the docs page, whose header declares `requirements: langfuse~=3.11`, with a `Valves` class holding `public_key`, `secret_key`, `host` (default `https://cloud.langfuse.com`). Save. The package installs on save; if `ENABLE_PIP_INSTALL_FRONTMATTER_REQUIREMENTS` is off or `OFFLINE_MODE` is on, install `langfuse~=3.11` yourself.
3. Click the gear (Valves) on the function, enter keys and host, save, then switch the filter on.
4. Scope it: function menu > **Global** for all models, or Workspace > Models > edit a model > Filters.

## Verify
Chat with an enabled model; in Langfuse each chat is one trace and each reply a `chat-reply` generation.

## Gotchas
- Stay on Langfuse Python SDK v3: v4 needs newer OpenTelemetry packages and breaks Open WebUI's own OpenTelemetry support. v3 works with Langfuse server version 4.
- Changing Host or Secret Key while keeping the same Public Key needs an Open WebUI restart.
- Token counts need providers to report usage on streams: enable the model's **Usage** capability (Workspace models, capabilities and bindings).
- Direct API calls are traced too while `ENABLE_API_OUTLET_FILTERS` is on (default).

## Checked
2026-11-07. Confirmed against the Open WebUI docs: tutorials/integrations/monitoring/langfuse (read in full). Nothing removed.
Method: documentation only; no commands were run.
