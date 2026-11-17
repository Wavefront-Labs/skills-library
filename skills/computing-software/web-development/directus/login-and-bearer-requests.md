---
id: computing-software.web-development.directus.login-and-bearer-requests
name: login-and-bearer-requests
category: computing-software
field: web-development
product: directus
tags: [auth-login, bearer-token, access-token, sdk-login]
level: intro
status: docs-checked
description: "Log a Directus user in via REST, GraphQL or SDK and use the returned access token as a Bearer header on item requests."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/getting-started/5.authenticate-user.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
REST login:

```bash
curl --request POST \
  --header 'Content-Type: application/json' \
  --data '{ "email": "hello@example.com", "password": "d1r3ctu5" }' \
  --url 'https://directus.example.com/auth/login'
```

GraphQL: `mutation { auth_login(email: "...", password: "...") { access_token refresh_token } }`.

SDK:

```js
import { createDirectus, authentication } from '@directus/sdk';
const client = createDirectus('https://directus.example.com').with(authentication());
const token = await client.login({ email, password });
```

Use the access token on requests:

```bash
curl --header 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  --url 'https://directus.example.com/items/posts'
```

Gotchas:
- Access tokens expire; refresh the token when that happens (see the email login guide).
- Tokens carry the permissions of the user they belong to; the quickstart gives the user a policy with Read on the collection.

## Checked

2026-11-04: REST, GraphQL and SDK login examples, the Bearer header request and token expiry/refresh note confirmed against the Directus Authenticate a User page. Removed a Verify line the page does not state.

Method: documentation only; no commands were run.
