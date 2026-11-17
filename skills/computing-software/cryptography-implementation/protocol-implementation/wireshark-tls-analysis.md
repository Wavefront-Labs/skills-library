---
id: computing-software.cryptography-implementation.protocol-implementation.wireshark-tls-analysis
name: wireshark-tls-analysis
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, wireshark-tls, wireshark, tls-analysis, sslkeylogfile, packet-capture, tshark]
level: practitioner
status: docs-checked
description: "Analyse TLS in Wireshark: display filters for handshakes and alerts, decrypting with SSLKEYLOGFILE, following streams, and spotting version, cipher and certificate issues."
sources: ["https://wiki.wireshark.org/TLS", "https://www.wireshark.org/docs/dfref/t/tls.html", "https://tshark.dev/", "https://datatracker.ietf.org/doc/html/rfc8446"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wireshark TLS analysis

## Decrypting with a key log
Firefox, Chrome and curl write per-session secrets to a file when the `SSLKEYLOGFILE` environment variable is set to
the absolute path of a writable file (their underlying library, NSS, OpenSSL or BoringSSL, does the writing).
In Wireshark: Edit > Preferences > Protocols > TLS, set the (Pre)-Master-Secret log filename (`tls.keylog_file`) to
that file. To decode non-standard ports, right-click a TLS packet and use Decode As to change the protocol for that
TLS port.

## Display filters
Field names are from the Wireshark TLS display filter reference; the numeric values are the TLS 1.3 (RFC 8446)
code points.

| Goal | Filter |
|---|---|
| ClientHello | `tls.handshake.type == 1` |
| ServerHello | `tls.handshake.type == 2` |
| Certificate message | `tls.handshake.type == 11` |
| Alerts (content type 21) | `tls.record.content_type == 21` |
| SNI | `tls.handshake.extensions_server_name == "api.example.com"` |
| TLS 1.3 offered or selected | `tls.handshake.extensions.supported_version == 0x0304` |
| Alert description | `tls.alert_message.desc` |

## Reading failures
- Alert after the server's Certificate, from the client: certificate verification failures include `unknown_ca` (48)
  and `bad_certificate` (42).
- TLS 1.3 alert messages are encrypted like other messages after the handshake keys are in use, so you need the key
  log to see their description.

## Verify
- [ ] Decrypted capture shows application data for the session under investigation; keylog files deleted after.

## Checked

2026-11-01. Confirmed against the Wireshark TLS wiki (SSLKEYLOGFILE producers, menu path, `tls.keylog_file`,
Decode As), the Wireshark TLS display filter reference (field names `tls.handshake.type`, `tls.record.content_type`,
`tls.handshake.extensions_server_name`, `tls.handshake.extensions.supported_version`, `tls.alert_message.desc`) and
RFC 8446 (code points 1, 2, 11, alert 21, 0x0304, alert 42 and 48, encrypted alerts). Removed: tcpdump and tshark
command lines, Node's `--tls-keylog`, and the RST and mismatch heuristics (not in the sources).
Method: documentation only; no commands were run.
