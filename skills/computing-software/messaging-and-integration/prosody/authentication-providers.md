---
id: computing-software.messaging-and-integration.prosody.authentication-providers
name: authentication-providers
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, authentication, ldap, anonymous, sasl]
level: practitioner
status: docs-checked
description: "Prosody authentication providers: internal_hashed default, internal_plain, cyrus, ldap and anonymous, and setting authentication globally or per host."
sources:
  - https://prosody.im/doc/authentication
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authentication providers

Select with the `authentication` option, globally or per host:

```lua
authentication = "internal_hashed"
```

- `internal_hashed`: hashed passwords in built-in storage (default).
- `internal_plain`: plaintext passwords in built-in storage.
- `cyrus`: Cyrus SASL, which can front LDAP, PAM and others.
- `ldap`: LDAP directory via lua-ldap.
- `anonymous`: SASL ANONYMOUS, random username, no credentials.

Built-in providers suit most deployments. Community providers vary in maturity; read their docs first. The page does not describe what happens to existing accounts when switching providers, so test on a copy.

Because the option is per host, `authentication = "anonymous"` can be set under one VirtualHost only.

Verify: a login against the configured host succeeds with the expected credentials (or without any for anonymous).

## Checked

2026-11-04. Read the Prosody authentication page: the authentication option set globally or per host, the internal_hashed default, the five providers and their descriptions, and community providers of varying maturity all match. Nothing removed.

Method: documentation only; no commands were run.
