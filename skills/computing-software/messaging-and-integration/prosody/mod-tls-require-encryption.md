---
id: computing-software.messaging-and-integration.prosody.mod-tls-require-encryption
name: mod-tls-require-encryption
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, tls, encryption, c2s, s2s]
level: practitioner
status: docs-checked
description: "mod_tls in Prosody: TLS on XMPP streams as described in XMPP Core, and the c2s_require_encryption and s2s_require_encryption options, both true by default."
sources:
  - https://prosody.im/doc/modules/mod_tls
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_tls

Enables SSL/TLS encryption on connected streams, implementing TLS as described in XMPP Core. For obtaining and configuring certificates, see Prosody's certificates documentation.

```lua
modules_enabled = { "tls"; }
c2s_require_encryption = true
s2s_require_encryption = true
```

| Option | Default | Effect |
|---|---|---|
| `c2s_require_encryption` | true | whether to force all client-to-server connections to be encrypted |
| `s2s_require_encryption` | true | whether to force all server-to-server connections to be encrypted |

These options cause Prosody to deny connections that are not encrypted. For s2s you may also want to enforce certificate authentication; see the page's s2s security reference.

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_tls. Replaced the unstated RFC 6120/STARTTLS wording with the page's "XMPP Core", removed the `s2s_secure_auth` name and cross-references that this page does not give, and a generic verify line.
Method: documentation only; no commands were run.
