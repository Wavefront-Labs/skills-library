---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-basicauth
name: middleware-basicauth
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, basicauth, authentication, htpasswd, usersfile, middleware]
level: practitioner
status: docs-checked
description: "Protect a Traefik router with the basicAuth middleware using hashed users or a usersFile, with realm and header options."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/basicauth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware basicauth
The `basicAuth` middleware grants access to authorized users only. Options: `users` (list of `name:hashed-password`), `usersFile` (path to a file with the same format), `realm` (default `traefik`), `headerField` (header that stores the authenticated user) and `removeHeader` (remove the authorization header before forwarding; default false).

```yaml
http:
  middlewares:
    test-auth:
      basicAuth:
        users:
          - "test:$apr1$H6uskkkW$IgXLP6ewTrSuBkTrqE8wj/"
        realm: "internal"
        removeHeader: true
```
Passwords must be hashed with MD5, SHA1 or BCrypt; use `htpasswd` to generate them. If both `users` and `usersFile` are set they are merged, and `users` wins over the file contents.

Gotchas: in docker-compose labels every dollar sign in the hash must be doubled (`$$`), for example `echo $(htpasswd -nB user) | sed -e s/\\$/\\$\\$/g`; do not double them where the value is not interpolated (for example the Ansible docker_container module). On Kubernetes use the `secret` field instead of `users`/`usersFile`; a `kubernetes.io/basic-auth` secret (keys `username`, `password`) is not hashed or encrypted and is less secure.

## Checked
2026-11-03. Confirmed against the Traefik basicAuth reference page (docs/content/reference/routing-configuration/http/middlewares/basicauth.md): options, defaults, hash algorithms, users/usersFile merge rule, dollar-sign doubling, Kubernetes secret. Removed: the "confirm how they combine" hedge (the docs state the rule) and the curl Verify step including the WWW-Authenticate header claim.
Method: documentation only; no commands were run.
