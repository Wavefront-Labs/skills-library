---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-digestauth
name: middleware-digestauth
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, digestauth, authentication, realm, usersfile, middleware]
level: practitioner
status: docs-checked
description: "Configure the digestAuth middleware in Traefik, including the name:realm:encoded-password user format, usersFile and Kubernetes secrets."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/digestauth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware digestauth
The `digestAuth` middleware restricts access with HTTP digest authentication. Options: `users` (each entry `name:realm:encoded-password`), `usersFile` (same format in a file), `realm` (default `traefik`), `headerField` (header that stores the authenticated user) and `removeHeader` (remove the authorization header before forwarding; default false).

```yaml
http:
  middlewares:
    test-auth:
      digestAuth:
        users:
          - "test:traefik:a2688e031edb4be6a3797f3882655c05"
          - "test2:traefik:518845800f9e2bfb1f1f740ec24f074e"
```
Generate the passwords with `htdigest`. If both `users` and `usersFile` are set they are merged, and `users` wins.

On Kubernetes use the `secret` field instead of `users`/`usersFile`. The secret is either a `kubernetes.io/basic-auth` secret (keys `username` and `password`, not hashed or encrypted, so less secure) or an Opaque secret with a `users` field holding one user per line.

## Checked
2026-11-03. Confirmed against the Traefik digestAuth reference page (docs/content/reference/routing-configuration/http/middlewares/digestauth.md): options, defaults, user format, htdigest, merge rule, Kubernetes secret types. Removed: claims that changing the realm invalidates hashes or causes repeated 401s, the dollar-doubling hedge, and the curl Verify step with the WWW-Authenticate header.
Method: documentation only; no commands were run.
