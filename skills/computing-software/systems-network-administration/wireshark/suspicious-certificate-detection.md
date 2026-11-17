---
id: computing-software.systems-network-administration.wireshark.suspicious-certificate-detection
name: suspicious-certificate-detection
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tls, certificate-anomalies, threat-hunting, x509, malware-traffic]
level: practitioner
status: verified
description: "Spot suspicious TLS certificates in captures: self-signed, default OpenSSL subjects, very new or short-lived certs, odd issuers and SAN mismatches."
sources:
  - https://www.wireshark.org/docs/dfref/x/x509sat.html
  - https://www.wireshark.org/docs/dfref/x/x509af.html
  - https://attack.mitre.org/techniques/T1573/002/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Suspicious certificates

Malware C2 often uses certificates that legitimate services do not. TLS 1.2 certificates are visible
without decryption; in TLS 1.3 all handshake messages after the ServerHello are encrypted (RFC 8446), so you need a key
log.

## Extract certificate data
```
tshark -r in.pcapng -Y "tls.handshake.type==11" -T fields \
  -e ip.src -e tls.handshake.extensions_server_name \
  -e x509sat.printableString -e x509sat.uTF8String -e x509af.utcTime -e x509af.generalizedTime | sort -u
```
`x509af.utcTime` only carries dates before 2050; a `notAfter` of 2099 is a GeneralizedTime and shows in
`x509af.generalizedTime` (RFC 5280). The fields are multi-valued (subject and issuer values come out comma-joined)
and times print in the analysing machine's time zone. In a test, a self-signed certificate with `O=Internet
Widgits Pty Ltd, CN=localhost` and notAfter 2099 printed exactly like that.
Or export certificates (right-click > Export Packet Bytes) and inspect with `openssl x509 -text`.

## Red flags
| Indicator | Example |
|-----------|---------|
| Self-signed (issuer = subject) to an internet IP | C2 servers, misconfigured devices |
| Default subjects | `O=Internet Widgits Pty Ltd`, `CN=localhost`, `ST=Some-State`, `CN=example.com` |
| Very recent notBefore | issued hours before first contact |
| Validity in years with no CA | `notAfter` 2099 self-signed |
| SAN/SNI mismatch | SNI `cdn.example.com`, cert for something else |
| Free CA + new domain + low traffic + beaconing | combine with timing analysis |

Filters:
```
x509sat.uTF8String == "Internet Widgits Pty Ltd" || x509sat.printableString == "Internet Widgits Pty Ltd"
tls.handshake.type == 1 && !tls.handshake.extensions_server_name      # ClientHello without SNI (IP-only destination)
```
Do not combine `type == 11` (Certificate) with `!tls.handshake.extensions_server_name`: the SNI lives in the
ClientHello, a different packet, so that filter matches every certificate message (it matched a certificate for a
connection whose ClientHello had an SNI).

## Enrichment
Hash the certificate (SHA-1/SHA-256 of the DER; `tls.handshake.certificate` printed as hex gives the DER, and its
SHA-256 equalled `openssl x509 -inform der -noout -fingerprint -sha256`) and search your threat intelligence and certificate-transparency sources.
Wireshark 4.4.1 has `tls.handshake.ja3s`/`ja3s_full` for the server hello but no JA4S field (only `ja4`, `ja4_r`).

## Verify
- [ ] Each suspicious cert is confirmed with certificate transparency or intel, and the internal host is identified.

## Checked
OpenSSL's default `openssl.cnf` supplies `Some-State` and `Internet Widgits Pty Ltd` as default subject values (found with grep).
Run with TShark 4.4.1 and openssl on a generated TLS 1.2 exchange carrying a self-signed ECDSA certificate
(`C=AU, ST=Some-State, O=Internet Widgits Pty Ltd, CN=localhost`, notBefore 2026-10-22, notAfter 2099-01-01):
the field pipeline printed the subject strings, `x509af.utcTime` for notBefore and `x509af.generalizedTime` for 2099;
the `x509sat` OR filter matched; the old no-SNI filter matched two certificate packets (one for a connection whose
ClientHello had an SNI) while the ClientHello version matched only the no-SNI hello; the certificate hash equalled
openssl's SHA-256 and SHA-1; `openssl x509 -text` fields printed. RFC 8446 and RFC 5280 text fetched. Named malware framework subjects and
threat-intel services were left out.
