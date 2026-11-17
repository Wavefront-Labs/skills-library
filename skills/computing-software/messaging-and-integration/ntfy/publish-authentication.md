---
id: computing-software.messaging-and-integration.ntfy.publish-authentication
name: publish-authentication
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, authentication, basic-auth, bearer, access-token]
level: practitioner
status: docs-checked
description: "Authenticate ntfy publish and subscribe requests with basic auth, bearer access tokens, or the auth query parameter."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authentication

Use HTTPS: base64 is encoding, not encryption.

## Username and password

```
curl -u phil:mypass -d "Look ma, with auth" https://ntfy.example.com/mysecrets
```

Header `Authorization: Basic base64(<username>:<password>)`, standard base64.

## Access tokens

Create with `ntfy token` or in the web app Account section.

```
curl -H "Authorization: Bearer tk_..." -d "hi" https://ntfy.example.com/mytopic
curl -u :tk_... -d "hi" https://ntfy.example.com/mytopic
```

Basic auth with an empty username also works: the server treats the password as the token.

## Query parameter (`?auth=`)

Works with either username/password or a token. The value is the raw base64 of the whole `Authorization` header value (including `Basic ` or `Bearer `), with the trailing `=` padding removed.

```
echo -n "Basic $(echo -n 'phil:mypass' | base64 -w0)" | base64 -w0 | tr -d '='

# for a token
echo -n "Bearer tk_..." | base64 -w0 | tr -d '='
```

## Gotchas

- Tokens must start with `tk_` and be 32 characters long including the prefix.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Authentication: Basic header form, tokens via ntfy token or web app, empty-username Basic, raw base64 auth parameter and its commands) and config page (tk_ prefix, 32 characters). Removed: the claim about which clients need the query parameter, the log/history gotcha and the Verify 401/403 line, none stated on the page. Corrected: the one-liner uses base64 -w0.
Method: documentation only; no commands were run.
