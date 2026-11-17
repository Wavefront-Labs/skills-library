---
id: computing-software.web-development.fastapi.jwt-password-hashing
name: jwt-password-hashing
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, security, jwt, pyjwt, pwdlib, argon2, password-hashing, timing-attack]
level: advanced
status: docs-checked
description: "Secure a FastAPI login with PyJWT access tokens and pwdlib Argon2 password hashes, including the sub claim and the dummy-hash timing defence."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/security/oauth2-jwt.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWT tokens and password hashing

Goal: real token signing and hashed passwords.

## Pieces
- JWT is a JSON object codified as a dense string. It is not encrypted (anyone can read it) but it is signed, so you can verify you issued it and detect tampering with the expiry.
- Install `pyjwt` (`pyjwt[crypto]` for RSA or ECDSA signatures).
- Install `pwdlib` with Argon2 (`pwdlib[argon2]`); Argon2 is the recommended algorithm. pwdlib supports bcrypt but no legacy algorithms; for outdated hashes the docs suggest passlib.
- Make a utility to hash and one to verify.
- Timing defence: when the username does not exist, still run `verify_password` against a dummy hash so response time does not reveal valid usernames.
- Generate the signing key with `openssl rand -hex 32` and keep it as `SECRET_KEY`; never reuse the docs sample. Set `ALGORITHM` to `"HS256"` and an expiry.

## Flow
1. `/token` builds a `timedelta`, creates the JWT and returns it with a Pydantic token response model.
2. `get_current_user` decodes and verifies the token; invalid means an HTTP error at once.
3. The `sub` claim holds a unique string identifier; prefix it (e.g. `username:`) to avoid collisions between entity types.

OAuth2 scopes extend this (see the scopes material in the advanced guide).

## Verify
Log in with the docs UI and confirm the `Authorization: Bearer` header carries only the token.

## Checked

Every claim above was read in the FastAPI OAuth2 with Password and JWT tutorial page (about JWT, PyJWT, pwdlib/Argon2, dummy-hash timing note, HS256 and openssl key generation, sub claim). Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
