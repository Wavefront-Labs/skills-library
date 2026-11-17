---
id: computing-software.messaging-and-integration.prosody.mod-dialback
name: mod-dialback
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, dialback, xep-0220, s2s, authentication]
level: advanced
status: docs-checked
description: "mod_dialback in Prosody: XEP-0220 s2s identity verification for untrusted certificates or no TLS, dialback_secret, and the removed dialback_without_dialback."
sources:
  - https://prosody.im/doc/modules/mod_dialback
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_dialback

Enables server-to-server identity verification using the Dialback method (XEP-0220). It may be required for server-to-server communication if your certificate is untrusted by some remote servers, or if no TLS is used.

```lua
modules_enabled = { "dialback"; }
```

- `dialback_secret`: default is a random string; rarely needed.
- Between 0.10.0 and 0.11.9 a feature to enable Dialback using certificates could be enabled with `dialback_without_dialback`. It had a security issue and was removed in 0.11.9. Do not enable this feature.

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_dialback. Removed the claim that `s2s_secure_auth` disables dialback (with a cross-reference to a skill), the wrong version range wording, and a generic verify line.
Method: documentation only; no commands were run.
