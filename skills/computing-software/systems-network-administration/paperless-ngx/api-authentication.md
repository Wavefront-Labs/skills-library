---
id: computing-software.systems-network-administration.paperless-ngx.api-authentication
name: api-authentication
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, rest-api, api-token, basic-auth, authorization, schema]
level: practitioner
status: docs-checked
description: "Authenticate to the Paperless-ngx REST API with basic auth, session, token, remote user or headless OIDC, and find the browsable schema."
sources:
  - "https://docs.paperless-ngx.com/api/"
  - "https://docs.paperless-ngx.com/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# REST API authentication

The browsable API and schema are at `/api/schema/view/`. Five methods exist.

1. Basic: `Authorization: Basic <credentials>` with base64 of `username:password`.
2. Session: logged-in browsers need no header.
3. Token: obtain one by POSTing `username` and `password` as a form or JSON to `/api/token/`, or create or regenerate it with the circular arrow in My Profile. Tokens can be managed in the Django admin. Send:
```
Authorization: Token <token>
```
4. Remote user: if `PAPERLESS_ENABLE_HTTP_REMOTE_USER_API` is on (default false). Make sure your reverse proxy does not pass a `Remote-User` header straight from the internet.
5. Headless OIDC through django-allauth endpoints under `api/auth/`.

```bash
curl -H "Authorization: Token <TOKEN>" https://paperless.example.com/api/documents/?page=1
```

## Notes
- Exports do not include API tokens; regenerate them after an import.
- Responses to authenticated requests carry `X-Api-Version` and `X-Version` headers.
- Global permissions define which API endpoints a user can access; object-level permissions are separate. Without view rights on a related object, the UI shows "Private" in place of its name.
- Object-level permissions accept `owner` and `set_permissions`; add `full_perms=true` to see the full structure instead of `user_can_change`.

## Checked
2026-11-04. Read the Authorization, Permissions and API Versioning parts of the API page and the remote user API setting in configuration (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts), plus the permissions section of usage and the exporter note in administration. Confirmed: five methods, schema path, token endpoint and profile button, Django admin token management, allauth `api/auth/`, exporter excludes tokens, version headers, `owner`/`set_permissions`/`full_perms=true`/`user_can_change`. Removed: the generic "use HTTPS" line. Reworded the permission note to what usage states ("Private" shown in place of object names).

Method: documentation only; no commands were run.
