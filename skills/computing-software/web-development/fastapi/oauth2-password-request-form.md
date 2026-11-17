---
id: computing-software.web-development.fastapi.oauth2-password-request-form
name: oauth2-password-request-form
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, security, oauth2, oauth2passwordrequestform, token-endpoint, scopes, www-authenticate]
level: practitioner
status: docs-checked
description: "Build the FastAPI /token login endpoint with OAuth2PasswordRequestForm, return access_token and token_type, and add the WWW-Authenticate header on 401."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/security/simple-oauth2.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The token endpoint

Goal: a spec-compliant OAuth2 password-flow login route.

## Rules
- The spec requires form fields named exactly `username` and `password` (not JSON, and not `email`). Your own models can use other names.
- `OAuth2PasswordRequestForm` is a class dependency declaring a form body: `username`, `password`, optional `scope` (one string, scopes separated by spaces), optional `grant_type`, `client_id`, `client_secret`. Use it with `Depends` on the `/token` path operation.
- The instance has `scopes`, a list built from `scope`.
- The spec requires `grant_type` with value `password` but this class does not enforce it; use `OAuth2PasswordRequestFormStrict` if you need that.
- It is only a convenience; you could write `Form` parameters yourself, unlike `OAuth2PasswordBearer` which registers the OpenAPI security scheme.
- On wrong credentials raise `HTTPException` ("Incorrect username or password"). Never store plaintext passwords; compare hashes.
- Respond with JSON containing `access_token` and `token_type` (`bearer`). This is the one thing you must do right yourself.
- A 401 should also carry `WWW-Authenticate: Bearer`; optional but part of the spec.
- Build `get_current_active_user` on top of `get_current_user` as a second dependency.

## Verify
Use the docs Authorize button, then call `/users/me`; logged out expect 401 "Not authenticated".

## Checked

Method: docs-only read of cited pages, 2026-11-08
