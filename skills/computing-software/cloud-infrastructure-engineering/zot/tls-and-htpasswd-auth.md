---
id: computing-software.cloud-infrastructure-engineering.zot.tls-and-htpasswd-auth
name: tls-and-htpasswd-auth
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, htpasswd, basic-auth, bcrypt, tls-config, local-accounts]
level: practitioner
status: docs-checked
description: "Set up Zot TLS and htpasswd basic authentication with bcrypt, hot reload of the password file, and ordering when LDAP is also configured."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/authn-authz.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
TLS is required because basic credentials travel over HTTP:

```json
"http": { "tls": { "cert": "/etc/zot/certs/server.cert", "key": "/etc/zot/certs/server.key" } }
```

Basic auth sends `username:password`, base64-encoded, in the `Authorization` header. Usernames cannot contain a colon; the first colon splits username from password.

htpasswd:
1. Create the file. `-B` is required because bcrypt is the only supported algorithm:
   ```
   htpasswd -bBn <username> <password> >> /etc/zot/htpasswd
   ```
2. Point Zot at it:
   ```json
   "http": { "auth": { "htpasswd": { "path": "/etc/zot/htpasswd" } } }
   ```

Zot watches the file and reloads on change; Kubernetes Secret volume updates are detected without a pod restart.

If both htpasswd and LDAP are configured, htpasswd is checked first, so a local htpasswd account still works when LDAP is unreachable.

Without any `accessControl` rules, authenticated users get no admin routes; see the access control skill.

## Checked

2026-11-04. Read against the zot authn-authz article (TLS, basic auth, htpasswd sections); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
