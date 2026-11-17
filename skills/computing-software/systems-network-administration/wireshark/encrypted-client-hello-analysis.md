---
id: computing-software.systems-network-administration.wireshark.encrypted-client-hello-analysis
name: encrypted-client-hello-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tls, encrypted-client-hello, ech, sni, privacy]
level: practitioner
status: verified
description: "Recognise Encrypted Client Hello in captures: outer vs inner ClientHello, public_name SNI, HTTPS record ECH config and what monitoring loses."
sources:
  - https://www.rfc-editor.org/rfc/rfc9849
  - https://www.rfc-editor.org/rfc/rfc9460
  - https://www.wireshark.org/docs/dfref/t/tls.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encrypted Client Hello

ECH (RFC 9849, March 2026, formerly draft-ietf-tls-esni) encrypts the real ClientHello (including SNI and ALPN)
inside an outer ClientHello addressed to a public "client-facing" server name. Which browsers and CDNs enable it
varies by version and setting: check each vendor's current documentation rather than assuming.

## How a client gets the key
The DNS HTTPS record (type 65, RFC 9460) carries an `ech=` parameter (SvcParamKey 5, an ECHConfigList; the IANA
SVCB registry lists it as defined by RFC 9848):
Capturing the DNS (or noticing DoH) tells you whether ECH is possible. Windows `nslookup` rejected `-type=HTTPS` in
this test ("unknown query type"), so use a resolver tool that supports type 65.

## In Wireshark
```
tls.handshake.extension.type == 65037      # encrypted_client_hello (0xfe0d, IANA TLS ExtensionType 65037)
tls.handshake.extensions_server_name       # shows the public_name, e.g. cloudflare-ech.com
tls.ech.client_hello_type                  # 0 = outer, with tls.ech.config_id, tls.ech.enc, tls.ech.payload
```
In TShark 4.4.1 a ClientHello with the extension prints `encrypted_client_hello (65037)` and the `tls.ech.*`
fields (checked on a generated ClientHello: type 0, config_id 5, enc 32 bytes, payload 128 bytes).
- The outer SNI is the provider's public name, not the destination site.
- Decrypting the inner ClientHello needs ECH secrets in the key log. TShark 4.4.1 does not (its binaries contain no
  `ECH_SECRET` handling and the 4.2 to 4.6 release notes do not mention ECH decryption); the development source
  reads `ECH_SECRET` and `ECH_CONFIG` key-log lines. Check the release notes of the version you run.
- GREASE ECH (RFC 9849 section 6.2): clients send a dummy ECH extension when they hold no ECH config, so presence
  of 0xfe0d does not prove real ECH. A real offer uses the config's `public_name` as the outer SNI.

## Server rejection
If the server cannot decrypt, it completes the handshake for the public name and can send `retry_configs` in the
EncryptedExtensions message (so it is itself encrypted in TLS 1.3); the client may retry with the new config. Expect
two handshakes in the capture when that happens.

## Monitoring impact
SNI-based filtering and logging see only the outer hello, and JA3/JA4 are computed from it (the generated outer
hello gave `t12d010200_...`). Where the inner name matters, get it from somewhere other than the wire: your own DNS logs, a TLS-inspecting proxy you
operate, or endpoint telemetry.

## Verify
- [ ] Outer SNI equals the public_name from the HTTPS record, and the site is still reached.

## Checked
Run with TShark 4.4.1 on a generated pair of ClientHellos (one with SNI only, one with SNI `cloudflare-ech.com` plus an
extension of type 0xfe0d): `tls.handshake.extension.type == 65037` matched only the second, the `tls.ech.*` fields
decoded, SNI and JA4 printed. 65037 = 0xfe0d computed and matched against the IANA TLS ExtensionType registry
(encrypted_client_hello, CH/HRR/EE, RFC 9849). RFC 9849 (rfc-editor.org) read for GREASE, public_name and
`retry_configs` in EncryptedExtensions; IANA SVCB registry for key 5. No real ECH site was queried.
