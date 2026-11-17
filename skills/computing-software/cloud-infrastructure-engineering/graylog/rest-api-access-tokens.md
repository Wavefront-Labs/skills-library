---
id: computing-software.cloud-infrastructure-engineering.graylog.rest-api-access-tokens
name: rest-api-access-tokens
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [rest-api, access-tokens, api-browser, token-ttl, basic-auth]
level: practitioner
status: docs-checked
description: "Call the Graylog REST API with access tokens: create tokens with a TTL, authenticate with token:token via curl."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/rest_api.html
  - https://go2docs.graylog.org/current/setting_up_graylog/rest_api_access_tokens.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# rest api access tokens

API access follows the user's permissions: what you can do in the UI you can do in the API. Use the API browser (auto-authenticated) or command line. Scripts must always send credentials; tokens avoid sending real passwords.

Create a token: **System > Users and Teams**, user's More menu, **Edit tokens**, enter a unique name and a TTL (ISO 8601 duration; default 30 days; built-in system users such as the Forwarder default to 100 years), Create Token. Copy it immediately; it cannot be retrieved later. Administrators can create tokens for others. Tokens also appear on the Token Management tab.

Use it as HTTP Basic auth with the token as username and the literal word `token` as password:

```
curl -u <token>:token -H 'Accept: application/json' -X GET 'http://localhost:9000/api/cluster?pretty=true'
```

Expired tokens stop authenticating, so update scripts with a new token.

## Checked

2026-11-04. Confirmed against the REST API and REST API Access Tokens pages (permissions model, menu path, ISO 8601 TTL, 30 day and 100 year defaults, Basic auth token:token curl form, expiry). Nothing removed.

Method: documentation only; no commands were run.
