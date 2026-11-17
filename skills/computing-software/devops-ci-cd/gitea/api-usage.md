---
id: computing-software.devops-ci-cd.gitea.api-usage
name: api-usage
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-api-token, gitea, api-token-scopes, authorization-token-header, x-gitea-otp, api-pagination, api-sudo, swagger-json]
level: practitioner
status: docs-checked
description: "Call the Gitea REST API: authentication methods, creating scoped tokens, the Authorization token header, 2FA header, pagination, sudo and swagger endpoints."
sources: ["https://docs.gitea.com/development/api-usage/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea API usage

Defaults: `ENABLE_SWAGGER` true, `MAX_RESPONSE_ITEMS` 50. Docs at `/api/swagger`, OpenAPI at `/swagger.v1.json`.

## Authentication
HTTP basic auth, `token=` or `access_token=` query parameters, the `Authorization: token ...` header, or HTTP signatures with a registered SSH key or certificate (draft-cavage-http-signatures, not RFC 9421; `Signature` header, plus `x-ssh-certificate` for certificates; go-sdk implements it). The header needs the word `token` first, for historical reasons:
```sh
curl "http://localhost:4000/api/v1/repos/test1/test1/issues" \
    -H "accept: application/json" \
    -H "Authorization: token 65eaa9c8..." \
    -H "Content-Type: application/json" -d '{"body":"testing","title":"test 20"}' -i
```
Tokens from the OAuth2 provider also work as `Authorization bearer ...`, `token=` or `access_token=`.

## Creating tokens
UI: User Settings, Applications, Manage Access Tokens, **Select permissions**; the token appears once in a toast. Default tokens are very limited, so pick scopes.
API: `POST /api/v1/users/{username}/tokens` requires **BasicAuth with the password**:
```sh
curl -H "Content-Type: application/json" \
 -d '{"name":"test","scopes":["write:package","read:notification"]}' \
 -u username:password https://gitea.your.host/api/v1/users/<username>/tokens
```
Scopes are `read:` or `write:` plus `activitypub`, `admin`, `issue`, `misc`, `notification`, `organization`, `package`, `repository`, `user`; `write` implies read; `["all"]` grants every scope read and write. The `sha1` token is returned once and listings show it empty with only `token_last_eight`.

## Two-factor
With 2FA on, send the current code: `-H "X-Gitea-OTP: 123456"`.

## Pagination and sudo
`page` and `limit` parameters; the response has a `Link` header (next, prev, last) and `x-total-count`, e.g. `/api/v1/repos/search?limit=1`. Admins can act as another user with `sudo=<user>` or a `Sudo:` header.

## Checked

2026-11-03: read https://docs.gitea.com/development/api-usage/ line by line; the commands, options, defaults and values stated above match those pages.
Changed: Removed the unconfirmed `commitstatus` scope.
Method: documentation only; no commands were run.
