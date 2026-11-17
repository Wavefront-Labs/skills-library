---
id: computing-software.devops-ci-cd.verdaccio.basic-login-and-bearer-tokens
name: basic-login-and-bearer-tokens
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [basic-login, bearer-token, http-basic, basiclogin, authorization-header, e401]
level: advanced
status: docs-checked
description: "Verdaccio 7 accepts only Bearer tokens on the API; the security.api.basicLogin option controls the Basic exception on login routes. Fixes E401 with _auth."
sources:
  - https://verdaccio.org/docs/configuration/
  - https://verdaccio.org/docs/setup-pnpm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Available from 7.x. Verdaccio 7 rejects `Authorization: Basic` on every API route except the login routes `GET` and `PUT /-/user/org.couchdb.user:<name>`. When the account exists, the client gets `409` from the PUT and retries with Basic (npm login on the second PUT, yarn on the GET too; pnpm login sends it on a single PUT).

```yaml
security:
  api:
    basicLogin: false   # default is true
```
With `false`, `npm login` for an existing user fails with 401 and `need: Bearer`. Users then get a token via the web login flow or the web UI and put it in `.npmrc` as `_authToken`. Passwords are still checked behind the same rate limit and two-factor challenge.

Gotcha: an `.npmrc` using `_auth` (base64 user:password) works on 6.x but fails on 7.x with `E401 Unable to authenticate`. Use host-scoped `_authToken`:
```
//localhost:4873/:_authToken=${VERDACCIO_TOKEN}
```
npm itself rejects a bare `_auth` in a project `.npmrc` (ERR_INVALID_AUTH).

6.x accepts Basic on every route and has no such option.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Configuration (Basic login section) and pnpm setup (_auth stops working on Verdaccio 7). Confirmed: the Basic exception on the login routes, the 409 retry, basicLogin default and its effect, E401 Unable to authenticate for _auth, ERR_INVALID_AUTH for a bare _auth, 6.x behaviour. Removed or corrected: nothing.

Method: documentation only; no commands were run.
