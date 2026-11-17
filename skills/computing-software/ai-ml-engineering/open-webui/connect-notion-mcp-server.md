---
id: computing-software.ai-ml-engineering.open-webui.connect-notion-mcp-server
name: connect-notion-mcp-server
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, integrations, notion, mcp, oauth]
level: practitioner
status: docs-checked
description: "Connect Open WebUI to Notion hosted MCP over Streamable HTTP with OAuth 2.1, including the WEBUI_SECRET_KEY prerequisite and the common errors."
sources:
  - https://docs.openwebui.com/tutorials/integrations/mcp-notion
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Connect Notion through MCP

Goal: let chats search, read, create and manage Notion pages and databases via Notion's hosted MCP server (community guide).

## Prerequisite
Set `WEBUI_SECRET_KEY` to a persistent value. Without it the OAuth session breaks on every container restart.

## Add the connection
Settings > Admin > Integrations > **+**:
| Field | Value |
|---|---|
| Type | MCP Streamable HTTP |
| URL | `https://mcp.notion.com/mcp` |
| Auth | OAuth 2.1 (use `OAuth 2.1 (Static)` if you have pre-created client credentials) |
| Name | `Notion` |
| Connection ID | `ntn` (auto-filled from the name; overwrite if you want to match the import) |
Click **Register Client**, then **Save**. Alternatively use **Import** with a JSON array containing one object: `type: "mcp"`, `url`, `spec_type: "url"`, `spec: ""`, `path: "openapi.json"`, `auth_type: "oauth_2.1"`, `key: ""`, and `info` with `id: "ntn"`, `name: "Notion"`.

## Authorize
In a chat open **+ > Integrations > Tools** and toggle **Notion** on; you are redirected to Notion to pick the workspace and pages to grant.

## Gotchas
- Do NOT set it as a default tool on a model: OAuth 2.1 needs an interactive redirect; enable it per chat.
- `Failed to connect to MCP server 'ntn'`: session expired; re-toggle the tool to re-authorize.
- `OAuth callback failed: OAuth callback state is invalid or expired`: you opened Open WebUI on `localhost` while `WEBUI_URL` is a public domain. Use the exact `WEBUI_URL` address. Signing out mid-flow or finishing in a different browser causes it too.
- `Object not found`: the page was not shared with the integration; adjust access at Notion's integrations settings.
- `missing_property` on create: Notion needs a parent page or database; tell the model to find the parent page first.
- Rate limits: 180 requests per minute general, 30 per minute for search.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page tutorials/integrations/mcp-notion (read in full): endpoint URL, WEBUI_SECRET_KEY prerequisite, the connection field table, Register Client, the import JSON fields, authorization steps, the no-default-tool warning, all four error strings with causes and the 180 and 30 per-minute limits. Nothing removed.
Method: documentation only; no commands were run.
