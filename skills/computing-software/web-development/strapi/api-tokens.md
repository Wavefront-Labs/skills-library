---
id: computing-software.web-development.strapi.api-tokens
name: api-tokens
category: computing-software
field: web-development
product: strapi
tags: [strapi, api-token, content-api, salt, encryption-key, authorization]
level: practitioner
status: docs-checked
description: "Create Strapi API tokens, choose type and duration, set the salt, and the encryption key that keeps tokens viewable."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/features/api-tokens.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# API tokens

Authenticate external requests to the Content API (REST and GraphQL). Path: Settings > Global settings > API Tokens. Separate from admin tokens: each is rejected on the other's routes.

Strapi pre-generates a Full access and a Read-only token. Create more with **Create new API Token**:

| Setting | Options |
|---|---|
| Name | required |
| Description | optional |
| Token duration | 7 days, 30 days, 90 days, Unlimited |
| Token type | Read-only, Full access, Custom (pick per content-type permissions) |

Without encryption configured, a token is shown only once; regenerate it after setting an encryption key to make it permanently viewable.

## Code config
The salt is `API_TOKEN_SALT` in `.env` or `apiToken.salt` in `/config/admin`. Changing the salt invalidates all existing API tokens.

To keep tokens visible in the admin panel set an encryption key:

```js
module.exports = ({ env }) => ({
  // other config parameters
  secrets: {
    encryptionKey: env('ENCRYPTION_KEY'),
  }
});
```

Without it tokens still work but cannot be viewed after first display. New projects get this key generated.

Practice from the page: prefer read-only tokens, scope narrowly, rotate long-lived tokens, store in a secrets manager.

## Checked

2026-11-04: checked against the Strapi docs page API Tokens (features/api-tokens). Confirmed: path, pre-generated Full access and Read-only tokens, form fields and options, `API_TOKEN_SALT` and `apiToken.salt`, salt change invalidating tokens, `secrets.encryptionKey` example and viewability rules, security advice. Reworded: the 'regenerate if lost' line to match the page, which advises regenerating after an encryption key is set.

Method: documentation only; no commands were run.
