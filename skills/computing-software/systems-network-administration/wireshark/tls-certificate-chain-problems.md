---
id: computing-software.systems-network-administration.wireshark.tls-certificate-chain-problems
name: tls-certificate-chain-problems
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tls, certificate-chain, x509, handshake-failure]
level: practitioner
status: verified
description: "Diagnose TLS certificate chain problems from captures: missing intermediates, wrong order, expired or mismatched certificates and the alerts they trigger."
sources:
  - https://www.rfc-editor.org/rfc/rfc8446#section-4.4.2
  - https://www.wireshark.org/docs/dfref/x/x509af.html
  - https://www.wireshark.org/docs/dfref/t/tls.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate chain problems in captures

In TLS 1.2 the Certificate message is in clear text; in TLS 1.3 it is encrypted (decrypt with a key log).

## Inspect
```
tls.handshake.type == 11
```
Expand Certificates: each entry shows subject, issuer, validity (`x509af.utcTime` lists notBefore and notAfter;
`x509af.notBefore` and `x509af.notAfter` are only the CHOICE wrappers and print 0), SAN (`x509ce.dNSName`). Export with right-click > Export Packet Bytes on a certificate to `.der`, then:
```
openssl x509 -inform der -in cert1.der -noout -subject -issuer -dates -ext subjectAltName
```

## What goes wrong
| Symptom in capture | Cause |
|--------------------|-------|
| Only the leaf certificate sent | missing intermediate; whether a client repairs it (for example by fetching the Authority Information Access URL) depends on the client, so test the failing client |
| Client sends Alert 48 (unknown_ca) after Certificate | chain does not lead to a trusted root on the client |
| Alert 42/45 (bad_certificate / certificate_expired) | expired leaf or intermediate |
| Alert 46 (certificate_unknown) | generic rejection; read the client log for the real reason |
| Client gets wrong certificate | SNI not sent, or LB default cert served (compare `tls.handshake.extensions_server_name`) |
| Chain includes the root | harmless but wasteful |

Filters:
```
tls.alert_message.desc == 48
tls.handshake.certificates_length > 6000      # huge chains causing extra round trips
x509ce.dNSName contains "example.com"
```

## Order
RFC 8446 section 4.4.2: the end-entity certificate MUST be first; each following certificate SHOULD directly certify
the one before it, and implementations SHOULD tolerate extra certificates and arbitrary order from any TLS version.
Strict older clients may still require leaf, then issuing intermediate, upward. Fix server config to send leaf + intermediates in order.

## Verify
- [ ] `openssl s_client -connect host:443 -servername host -showcerts` matches the capture and returns `Verify return code: 0`.

## Checked (2026-10-22)
- Ran on Wireshark 4.4.1 over a loopback capture with a self-signed server certificate: the TLS 1.2 flow showed `tls.handshake.type == 11` in clear without any key, while the TLS 1.3 flow showed its Certificate (length 808) only after the capture was given a key log (DSB), confirming the TLS 1.3 statement. `tls.handshake.certificates_length` (806 in the test) and `x509ce.dNSName` (`localhost`) work; `x509af.notBefore`/`notAfter` printed 0 while `x509af.utcTime` printed the two dates (fixed in the skill).
- Extracted the DER via `tshark -T fields -e tls.handshake.certificate`, then the skill's `openssl x509 -inform der ... -noout -subject -issuer -dates -ext subjectAltName` (OpenSSL 3.2.3) printed subject, issuer, dates and `DNS:localhost`, matching the capture.
- RFC 8446 section 4.4.2 ordering text read at https://www.rfc-editor.org/rfc/rfc8446.txt (this corrected the old "any order" wording); alert numbers from the IANA TLS alert registry.
