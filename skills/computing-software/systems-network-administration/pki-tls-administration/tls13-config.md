---
id: computing-software.systems-network-administration.pki-tls-administration.tls13-config
name: tls13-config
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [tls13-config, pki-tls-versions, tls13, rfc8446, handshake, tls-config, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Know what TLS 1.3 changes from 1.2: fixed AEAD cipher suites, mandatory forward secrecy, encrypted handshake, no compression or renegotiation."
sources:
  - https://www.rfc-editor.org/rfc/rfc8446
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS 1.3 handshake and what it changes
Goal: enable TLS 1.3 knowing what it removes.
- Suites defined by RFC 8446: TLS_AES_128_GCM_SHA256, TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256, TLS_AES_128_CCM_SHA256, TLS_AES_128_CCM_8_SHA256. A TLS-compliant application must implement TLS_AES_128_GCM_SHA256.
- Public-key based key exchange mechanisms now provide forward secrecy.
- All handshake messages after the ServerHello are encrypted; the new EncryptedExtensions message carries extensions previously sent in the clear.
- Removed or replaced: compression, DSA, custom DHE groups, ChangeCipherSpec (except for middlebox compatibility), point format negotiation and the TLS 1.2 PSK/resumption mechanisms (replaced by a single PSK exchange). RSA signatures use RSASSA-PSS.
- Version negotiation moved to a version list in the `supported_versions` extension.
- Renegotiation is forbidden in TLS 1.3. A client performing renegotiation with TLS 1.2 or earlier that receives a TLS 1.3 ServerHello must abort.
- 0-RTT data is an optional extension of the 1-RTT handshake and has weaker replay protection than ordinary 1-RTT data.
Verify:
- [ ] The server negotiates TLS 1.3 with a client that supports it, using one of the suites above.

## Checked
Method: docs-checked 2026-11-09 against RFC 8446 (section 1.2 list of differences from TLS 1.2, section 9.1 mandatory suites, appendix B.4 cipher suites, renegotiation and 0-RTT sections). The NIST SP 800-52 landing page was not read and was dropped. Removed: the nginx/Apache directives, the `ssl_conf_command` note, the `openssl s_client` and testssl commands, the NIST requirement claims, the middlebox/SSLKEYLOGFILE gotcha, and "certificates must use signature algorithms the client lists", none confirmed on the page read.
