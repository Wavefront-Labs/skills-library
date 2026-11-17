---
id: computing-software.rpa-and-low-code.n8n.credential-overwrites
name: credential-overwrites
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, credentials, oauth, credentials-overwrite-endpoint, persistence, queue-mode]
level: advanced
status: docs-checked
description: "Set global n8n credential overwrites via the REST endpoint or env var, secure it with a bearer token, show OAuth scopes and persist overwrites to workers."
sources:
  - https://docs.n8n.io/administer/manage-credentials/credential-overwrites
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: hide OAuth client secrets from users while letting them connect with the "Connect" button. n8n hides overwritten fields in the editor.

## Env var (not recommended)
`CREDENTIALS_OVERWRITE_DATA` = `{ CREDENTIAL_NAME: { PARAMETER: VALUE }}`. Environment variables are not protected in n8n, so the data can leak to users.

## REST endpoint (recommended)
1. Set the path: `export CREDENTIALS_OVERWRITE_ENDPOINT=send-credentials`. Optionally set `CREDENTIALS_OVERWRITE_ENDPOINT_AUTH_TOKEN` to require a bearer token. Without a token the endpoint can only be called once.
2. Prepare JSON keyed by credential type:
```json
{ "asanaOAuth2Api": { "clientId": "<id>", "clientSecret": "<secret>" },
  "githubOAuth2Api": { "clientId": "<id>", "clientSecret": "<secret>" } }
```
3. Send it:
```sh
curl -H "Content-Type: application/json" --data @oauth-credentials.json http://localhost:5678/send-credentials
curl -H "Content-Type: application/json" -H "Authorization: Bearer secure-token" --data @oauth-credentials.json http://localhost:5678/send-credentials
```
Credentials can extend others: set parameters on `googleOAuth2Api` and child credentials such as `googleSheetsOAuth2Api` use them.

## Scope fields
n8n hides scope fields when managed OAuth is available. `N8N_MANAGED_OAUTH_SHOW_SCOPES=googleOAuth2Api` (comma-separated list) shows them for listed types only, not types extending them. Risk: a scope you did not declare in provider app verification can get the app suspended or banned.

## Persistence
`CREDENTIALS_OVERWRITE_PERSISTENCE=true` stores encrypted overwrites in the `settings` table and broadcasts `reload-overwrite-credentials` so workers reload them. When off, overwrites live in memory of the loading process only: not propagated to workers and lost on restart.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/administer/manage-credentials/credential-overwrites

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
