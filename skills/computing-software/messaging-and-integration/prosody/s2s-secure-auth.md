---
id: computing-software.messaging-and-integration.prosody.s2s-secure-auth
name: s2s-secure-auth
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, s2s, tls, dialback, certificates, security]
level: practitioner
status: docs-checked
description: "Prosody server-to-server security: s2s_secure_auth, s2s_secure_domains, s2s_insecure_domains and how dialback acts as the fallback authentication."
sources:
  - https://prosody.im/doc/s2s
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# s2s authentication

By default Prosody tries to use TLS if the other side supports it, and falls back to dialback (a DNS-based authentication mechanism) if it does not or if the certificate is incorrect or not trusted.

- `s2s_secure_auth = true`: require encryption and certificate authentication; this disables dialback and requires all remote servers to present trusted certificates valid for their domain.
- `s2s_insecure_domains`: listed domains may use weaker mechanisms such as dialback.
- `s2s_secure_domains`: listed domains must always present valid certificates, regardless of `s2s_secure_auth`.

```lua
s2s_insecure_domains = { "gmail.com" }
s2s_secure_domains = { "jabber.org", "xmpp.org" }
```

Many servers on the XMPP network use self-signed or invalid certificates, or do not support TLS at all (the page names gmail.com and Google-hosted domains), which is why the insecure-domains exception exists. Certificate verification requires LuaSec 0.5 or higher.

## Checked

2026-11-04: confirmed against prosody.im/doc/s2s (Security section: defaults, the three options with the page's examples, LuaSec version). Removed the trigger "s2s_secure_auth is off" for fallback and a generic verify line with a `prosodyctl check certs` claim that the page does not make.
Method: documentation only; no commands were run.
