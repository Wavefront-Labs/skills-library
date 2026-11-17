---
id: computing-software.database-administration.dragonfly.jwt-authentication
name: jwt-authentication
category: computing-software
field: database-administration
product: dragonfly
tags: [jwt, jwt-validate, jwt-validate-url, authentication, dragonfly]
level: advanced
status: docs-checked
description: "Validate AUTH credentials against an HTTP endpoint with Dragonfly JWT mode, including required response fields and the plaintext warning."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/flags.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/acl.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
JWT mode sends every `AUTH` credential to an HTTP validation endpoint instead of checking the local ACL password store.

Flags:

| Flag | Meaning | Default |
| --- | --- | --- |
| `jwt_validate` | master switch; changeable at runtime with `CONFIG SET` | false |
| `jwt_validate_url` | endpoint that validates credentials; must be set at startup | empty |
| `jwt_validate_timeout_ms` | deadline for the whole validation call; a slow validator makes `AUTH` fail | 300 |

Endpoint contract: it must return JSON containing `valid`, `username` and optionally `exp`. The ACL user named in the response must already exist (be provisioned with `ACL SETUSER`).

Warnings from the docs:

- The ACL page warns that with JWT validation enabled the password or token of every `AUTH` command is sent to the validation endpoint **in cleartext**. Run the endpoint on the same host or a trusted private network only.
- The flag reference says the endpoint uses plain HTTP without TLS.
- Dragonfly does not cache validation results, so each `AUTH` calls the endpoint.

Plan the endpoint's availability: if it does not answer within the timeout, authentication is rejected.

## Checked

2026-11-04. Confirmed in the flags page (`jwt_validate`, `jwt_validate_url`, `jwt_validate_timeout_ms` descriptions, defaults, response fields, no caching, plain HTTP) and the ACL guide (cleartext warning). Nothing removed.

Method: documentation only; no commands were run.
