---
id: computing-software.ai-ml-engineering.open-webui.enable-direct-connections
name: enable-direct-connections
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, direct-connections, cors, api-keys, connections]
level: practitioner
status: docs-checked
description: "Enable the experimental Open WebUI Direct Connections feature so users call OpenAI-compatible APIs straight from the browser, including CORS and key-scope cautions."
sources:
  - https://docs.openwebui.com/features/chat-conversations/direct-connections
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Enable Direct Connections

Goal: let users add their own OpenAI-compatible endpoint whose inference requests go from the browser straight to the provider, bypassing the Open WebUI backend (experimental, may change or be removed).

## How it differs
Normally browser -> Open WebUI backend -> provider. With Direct Connections the browser talks to the provider. The server still runs the rest of the turn (title, tags and other background steps) and those read the instance model list.

## Admin steps
1. Settings > Admin > Connections > **Direct Connections** toggle On, or set `ENABLE_DIRECT_CONNECTIONS=true`.
2. Make sure the provider allows your Open WebUI origin via CORS. Browser requests are blocked by strict providers (the docs name official OpenAI as likely to block); it suits flexible providers or internal API gateways.

## User steps
User Settings > Connections > **+** Add Connection, enter Base URL (for example `https://api.groq.com/openai/v1`) and API Key, Save. The models then show in the model list, usually indistinguishable from backend models, but traffic flows from the user machine to the provider.

## Benefits
- Personal API keys are kept in the browser local storage, not on the server.
- Fewer hops (potentially lower latency) and less server load.

## Gotchas
- Use least-privilege provider keys (inference-only if the provider supports scoped keys), never management or master keys, because keys live in browsers.
- Because the browser makes the request, the provider or gateway must allow your Open WebUI domain via CORS; strict providers may block direct browser requests.
- On a Redis-backed multi-replica deployment, background steps read one consistent copy of the model list, so a model-list refresh mid-request no longer fails the message.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page features/chat-conversations/direct-connections (read in full): experimental status, what bypasses the backend, background steps still read the model list (consistent copy on Redis-backed multi-replica), admin toggle and ENABLE_DIRECT_CONNECTIONS, the CORS prerequisite and the strict-provider caution, the least-privilege key warning, user setup steps and the example Base URL, and local storage of keys. Reworded: latency benefit to 'potentially lower' and the CORS gotcha to what the page states.
Method: documentation only; no commands were run.
