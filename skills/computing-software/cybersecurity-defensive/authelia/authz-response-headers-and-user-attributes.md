---
id: computing-software.cybersecurity-defensive.authelia.authz-response-headers-and-user-attributes
name: authz-response-headers-and-user-attributes
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, remote-user, remote-groups, trusted-header-sso, authz-headers, user-attributes]
level: practitioner
status: docs-checked
description: "Customise the identity headers Authelia returns from authz endpoints, such as Remote-User and Remote-Groups, and their name restrictions."
sources:
  - https://www.authelia.com/configuration/miscellaneous/server-endpoints-authz/
  - https://www.authelia.com/overview/authorization/trusted-headers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Protected applications that support trusted-header single sign-on learn who the user is from response headers copied from Authelia. Each authz endpoint can define them under `headers`.

```yaml
server:
  endpoints:
    authz:
      forward-auth:
        implementation: 'ForwardAuth'
        headers:
          Remote-User:
            user_attribute: 'username'
          Remote-Groups:
            user_attribute: 'groups'
          Remote-Name:
            user_attribute: 'display_name'
          Remote-Email:
            user_attribute: 'email'
```

Rules to respect:

- Configuring `headers` replaces the default set entirely. If you add one header, restate `Remote-User`, `Remote-Groups`, `Remote-Name` and `Remote-Email` when applications still need them.
- Names must be valid header characters and must not be standard or reserved headers such as `Content-Type`, `Location`, `Set-Cookie`, `WWW-Authenticate`, `Access-Control-*`, `X-Forwarded-*` or `X-Original-*`. Names are case-insensitive, so the same name cannot appear twice in different cases.
- `user_attribute` can be any attribute from the authentication backend or one created under user attribute definitions. An unknown or unmapped attribute causes a startup error.
- A list-valued attribute, such as `groups`, is joined with commas.

Check: point a header-echo test app at the proxy and confirm the four headers carry your values after login.

## Checked

2026-11-08. Confirmed against the Server Authz Endpoints configuration page (headers dictionary, replacement of defaults, reserved header names, user_attribute, startup error, comma-joined lists) and the Trusted Headers SSO overview. Removed: an unsourced advice about proxy-only reachability.

Method: documentation only; no commands were run.
