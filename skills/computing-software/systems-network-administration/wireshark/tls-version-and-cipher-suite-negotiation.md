---
id: computing-software.systems-network-administration.wireshark.tls-version-and-cipher-suite-negotiation
name: tls-version-and-cipher-suite-negotiation
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tls, tls-version, cipher-suite, supported-versions, handshake-failure, protocol-version-alert]
level: practitioner
status: verified
description: "Find which TLS version and cipher suite each connection negotiated, why handshakes fail on version or cipher mismatch, and inventory legacy TLS 1.0/1.1 clients from a capture."
sources:
  - https://www.rfc-editor.org/rfc/rfc8446#section-4.2.1
  - https://www.wireshark.org/docs/dfref/t/tls.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS version and cipher suite negotiation

## Where the version really is
- TLS 1.3 hides behind `legacy_version 0x0303` (1.2) in the record and Client Hello. The real offer
  is the `supported_versions` extension; the chosen version is in the Server Hello's
  `supported_versions`.
- Wireshark's Protocol column shows `TLSv1.3` correctly from the Server Hello.

Filters:
```
tls.handshake.type == 2 && tls.handshake.extensions.supported_version == 0x0304   # TLS 1.3 chosen
tls.handshake.type == 2 && tls.handshake.version == 0x0302                         # TLS 1.1 chosen
tls.handshake.type == 1 && !tls.handshake.extensions.supported_version             # client cannot do 1.3
tls.handshake.ciphersuite                                                          # chosen suite (Server Hello)
```

## Inventory legacy clients
```
tshark -r cap.pcapng -Y "tls.handshake.type == 2" -T fields \
  -e ip.dst -e tls.handshake.version -e tls.handshake.extensions.supported_version \
  -e tls.handshake.ciphersuite | sort | uniq -c | sort -rn
```
`ip.dst` of a Server Hello is the client. Use this before disabling TLS 1.0/1.1 or a cipher on a
server or load balancer.

## Handshake failures
| Alert (tls.alert_message.desc) | Typical meaning |
|---|---|
| 70 protocol_version | no common version (server requires 1.2+, client offers 1.0) |
| 40 handshake_failure | no common cipher suite or signature algorithm |
| 71 insufficient_security | server wants stronger suites than offered |
| 112 unrecognized_name | SNI not matched |
| 42/48 bad_certificate / unknown_ca | certificate trust problem (see chain analysis) |
```
tls.alert_message.level == 2           # fatal alerts
```
Compare the Client Hello cipher list with the server's configuration; a client offering only
CBC/RSA suites against a server allowing only ECDHE-GCM fails with alert 40.

## Gotchas
- Middleboxes doing TLS inspection terminate TLS; the capture on each side shows different
  versions/suites.
- Encrypted Client Hello (ECH) hides the inner hello; you see the outer one only.
- QUIC carries TLS 1.3 inside CRYPTO frames; filter `quic && tls.handshake.type == 1`.

## Verify
- [ ] For a failing client you can name the offered versions, offered suites, the alert, and which
  side sent it.

## Checked (2026-10-22)
- Built a loopback capture (dumpcap + Npcap, Python 3.14 ssl servers/clients and OpenSSL 3.2.3 s_client) with TLS 1.3 (0x1302), TLS 1.2 ECDHE (0xc030), TLS 1.2 RSA kx (0x009c) and two failures, then ran every filter and the `tshark -T fields ... | sort | uniq -c | sort -rn` inventory with Wireshark 4.4.1: `tls.handshake.extensions.supported_version == 0x0304` matched only the TLS 1.3 Server Hello (legacy `tls.handshake.version` stayed 0x0303 in all three); `tls.handshake.type == 1 && !tls.handshake.extensions.supported_version` matched exactly the clients capped at TLS 1.2; `ip.dst` of a Server Hello was the client.
- Alerts seen: a TLS 1.3-only client against a TLS 1.2-only server drew alert 70 (server sent it, level 2), a client with no common cipher suite drew alert 40 from the server; `tls.alert_message.level == 2` matched both. Alert names/numbers (40, 42, 45, 46, 48, 70, 71, 112) checked against the IANA registry https://www.iana.org/assignments/tls-parameters/tls-parameters-6.csv.
- `quic && tls.handshake.type == 1` parses and runs (no QUIC in the test capture).
