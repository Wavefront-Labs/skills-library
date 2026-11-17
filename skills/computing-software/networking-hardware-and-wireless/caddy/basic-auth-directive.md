---
id: computing-software.networking-hardware-and-wireless.caddy.basic-auth-directive
name: basic-auth-directive
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [basic-auth, authentication, caddyfile, hash-password, argon2id, bcrypt, http-401]
level: practitioner
status: docs-checked
description: "Protect paths with the Caddyfile basic_auth directive: hashed passwords only, bcrypt or argon2id, realm, matcher scoping and the user id placeholder."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/basic_auth
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: put HTTP Basic Authentication in front of a site or a path without storing plaintext passwords.

Syntax: `basic_auth [<matcher>] [<hash_algorithm> [<realm>]] { <username> <hashed_password> ... }`. The default hash algorithm is `bcrypt`; `argon2id` is the documented alternative and is named before the realm, e.g. `basic_auth /secret/* argon2id { ... }`. Caddy refuses plaintext passwords in configuration, so generate each hash with the `caddy hash-password` command and paste the result next to the username.

Behaviour: a missing or wrong `Authorization` header gets `401 Unauthorized`, which makes the browser prompt. After a successful login the placeholder `{http.auth.user.id}` holds the username, so `respond "Welcome, {http.auth.user.id}" 200` works. Usernames and hashes may use global placeholders such as `{env.*}`, replaced when the config loads, which keeps hashes out of the file. Other text in braces is left as-is.

Scoping: with no matcher the whole site is protected. A path matcher such as `/secret/*` protects only that subtree while `file_server` still serves everything else publicly; combine it with `root /srv` as in the page example.

Gotchas: basic auth is not secure over plain HTTP, so only rely on it where HTTPS is active. Before v2.8.0 the directive was spelled `basicauth`; old configs and snippets still show that name, so rename when upgrading. Bcrypt hash prefixes in the examples look like `$2a$14$...`; argon2id ones look like `$argon2id$v=19$m=47104,t=1,p=1$...`.

## Checked
2026-11-03. Confirmed against the Caddy basic_auth directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
