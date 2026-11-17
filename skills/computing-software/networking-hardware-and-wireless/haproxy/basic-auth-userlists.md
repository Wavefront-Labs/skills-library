---
id: computing-software.networking-hardware-and-wireless.haproxy.basic-auth-userlists
name: basic-auth-userlists
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, userlist, http-auth, basic-auth, password-hash, http-request-auth]
level: practitioner
status: docs-checked
description: "Protect paths with HTTP basic authentication in HAProxy using userlist, hashed passwords and http-request auth, and keep credentials out of config."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# basic auth userlists
A `userlist` holds users, passwords and groups.

```
userlist admins
    user alice password $6$<salt>$<hash>
    user bob   insecure-password 'changeme'                 # avoid
    group ops users alice,bob
frontend fe_web
    acl auth_ok http_auth(admins)
    acl auth_ops http_auth_group(admins) ops
    http-request auth realm "Restricted" if { path_beg /admin } !auth_ok
    http-request del-header Authorization if auth_ok
```
`password` takes an encrypted hash evaluated with `crypt(3)`, so the algorithms depend on the system (glibc supports MD5, SHA-256, SHA-512 and DES); `insecure-password` stores plaintext. Passwords are ordinary arguments, so single-quote them. Generate hashes with your system's tooling and keep them out of version control.

Hashes cost CPU: each request's password is run through the algorithm, and the docs warn this can become a major share of HAProxy CPU use; reduce the SHA rounds or the algorithm cost, and note musl (Alpine) is slower than glibc. Keep basic auth for admin paths only.

`http-request auth [realm <realm>]` stops rule evaluation and answers 401 (or 407) with a `WWW-Authenticate` basic challenge for the realm. Basic auth sends credentials in a reversible encoding, so require TLS. Delete the `Authorization` header before forwarding if the backend should not see it. Combine with rate limiting against brute force (see per-ip-rate-limiting).

Verify: `curl -i https://host/admin` returns 401; `curl -u alice:<password> https://host/admin` returns 200.

## Checked
2026-11-03. Confirmed against configuration.html: section 3.4 Userlists (`user`, `group`, `password`, `insecure-password`, crypt(3), CPU warning, quoting), `http-request auth`, `http_auth`, `http_auth_group`. Removed: the `mkpasswd -m` and `openssl passwd -6` commands (not in the docs), the `$5$rounds` sample hash, the "cache with a cookie" tip and the unlabelled-prompt claim.
Method: documentation only; no commands were run.
