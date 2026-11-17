---
id: computing-software.ai-ml-engineering.open-webui.forward-user-identity-headers-to-backends
name: forward-user-identity-headers-to-backends
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [env-configuration, forward-user-info, headers, jwt, audit, tool-servers]
level: advanced
status: docs-checked
description: "Send the signed-in user's identity and chat IDs from Open WebUI to model and tool backends as headers or a signed JWT, with per-connection custom headers."
sources:
  - https://docs.openwebui.com/reference/env-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let an upstream (model gateway, tool server, embedding service) know which user and chat a request belongs to, for authorization, auditing, rate limiting or tracing.

## Turn it on
`ENABLE_FORWARD_USER_INFO_HEADERS=true` (default `False`). Headers and where they go:
- `X-OpenWebUI-User-Name`, `-User-Id`, `-User-Email`, `-User-Role`: OpenAI, Ollama and Anthropic connections, OpenAPI and MCP tool servers, and external embedding, reranking, web-search, audio, image and document-loader services (including Mistral OCR).
- `X-OpenWebUI-Chat-Id`: OpenAI, Ollama and tool servers (not Anthropic).
- `X-OpenWebUI-Message-Id`: tool servers only; needed for external tool event emitting.
- `X-OpenWebUI-Auth-Type`: OpenAI and Ollama only; value `jwt` (browser session) or `api_key`. Do not build an authorization rule on its absence elsewhere.

## Rename headers
Variables: `FORWARD_USER_INFO_HEADER_USER_NAME`, `_USER_ID`, `_USER_EMAIL`, `_USER_ROLE`, `_AUTH_TYPE`, `FORWARD_SESSION_INFO_HEADER_CHAT_ID`, `FORWARD_SESSION_INFO_HEADER_MESSAGE_ID`. Example for AWS Bedrock AgentCore:
```bash
FORWARD_USER_INFO_HEADER_USER_NAME=X-Amzn-Bedrock-AgentCore-Runtime-Custom-User-Name
FORWARD_SESSION_INFO_HEADER_CHAT_ID=X-Amzn-Bedrock-AgentCore-Runtime-Custom-Chat-Id
```

## Signed identity instead of plain headers
Set `FORWARD_USER_INFO_HEADER_JWT_SECRET` to send one HS256 JWT in the header named by `FORWARD_USER_INFO_HEADER_JWT` (default `X-OpenWebUI-User-Jwt`) in place of the four `X-OpenWebUI-User-*` headers. Claims: `sub`, `email`, `name`, `role`, `iss` (`open-webui`), `iat`, `exp`. Lifetime `FORWARD_USER_INFO_HEADER_JWT_EXPIRES_SECONDS` (default 300); a fresh token is minted per request, so it only covers clock skew. The upstream verifies it with the shared secret, which plain headers cannot offer.

## Per-connection custom headers
Not an env var: in Settings > Admin > Connections, edit a connection and fill Headers with JSON, or use the `headers` object inside `OPENAI_API_CONFIGS` / `OLLAMA_API_CONFIGS`.
```json
{"X-Message-Id": "{{MESSAGE_ID}}", "X-Trace": "{{CHAT_ID}}/{{MESSAGE_ID}}"}
```
Placeholders: `{{CHAT_ID}}`, `{{MESSAGE_ID}}`, `{{USER_MESSAGE_ID}}`, `{{USER_MESSAGE_PARENT_ID}}`, `{{FILE_ID}}`, `{{FILE_NAME}}`, `{{FILE_CONTENT_TYPE}}`, `{{TASK}}`, `{{MODEL_ID}}`, `{{USER_ID}}`, `{{USER_NAME}}`, `{{USER_EMAIL}}`, `{{USER_ROLE}}`, `{{AUTH_TYPE}}`, `{{USER_GROUPS}}`, `{{USER_GROUP_IDS}}`, `{{USER_AGENT}}`. A placeholder with no value becomes an empty string. Group placeholders cost a database lookup, done only when used.

## Gotchas
- Custom headers work even when `ENABLE_FORWARD_USER_INFO_HEADERS` is false, are applied last, and override a built-in header of the same name.
- Plain headers can be spoofed by anything on the network path; prefer the JWT.
- `{{MODEL_ID}}` is empty on background tasks such as title or tag generation from a browser chat.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page reference/env-configuration (read the whole Security Variables forwarding section from ENABLE_FORWARD_USER_INFO_HEADERS through Custom Forwarded Headers): default False, the header-to-backend table, the Auth-Type values and its absence warning, every rename variable and the AgentCore example, the HS256 JWT claims, header name and 300 second default lifetime, per-connection custom headers independent of the toggle and applied last, the full placeholder list, empty-string behaviour, the group lookup cost and the MODEL_ID empty-on-background-task note. Nothing removed.
Method: documentation only; no commands were run.
