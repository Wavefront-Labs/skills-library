---
id: computing-software.cryptography-implementation.protocol-implementation.tls-client-fingerprinting-ja3-and-ja4
name: tls-client-fingerprinting-ja3-and-ja4
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, ja4, ja3, tls-fingerprinting, bot-detection, clienthello, ja4s]
level: advanced
status: docs-checked
description: "Compute TLS client fingerprints with JA3 and JA4: fields hashed, GREASE handling, JA4 layout, tools that support them, and gaps such as session resumption."
sources: ["https://github.com/FoxIO-LLC/ja4", "https://github.com/salesforce/ja3", "https://developers.cloudflare.com/bots/concepts/ja3-ja4-fingerprint/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS client fingerprinting with JA3 and JA4

## JA3 (salesforce/ja3)

Decimal values of five ClientHello fields, in order: SSL version, accepted
ciphers, list of extensions, elliptic curves, elliptic curve point formats.
Fields are joined with `,` and values within a field with `-`; empty fields
stay empty. The string is MD5 hashed to a 32-character fingerprint. GREASE
values are ignored so GREASE clients keep a single hash.

## JA4 (FoxIO technical_details/JA4.md)

Format `t13d1516h2_8daaf6152771_e5627efa2ab1`, ignoring GREASE everywhere:
- Part a: `q` QUIC, `d` DTLS or `t` TLS over TCP; two-character TLS version
  (highest supported_versions value, else the protocol version; 13, 12, 11,
  10, s3, s2, d1, d2, d3, 00 unknown); `d` if SNI present else `i`;
  two-character cipher count (capped at 99); two-character extension count
  (SNI and ALPN included); first and last character of the first ALPN value
  (`00` if none).
- Part b: SHA-256 of the cipher list as 4-hex-digit values, sorted, comma
  separated, truncated to 12 characters. `000000000000` if there are none.
- Part c: SHA-256 of the sorted extension list (SNI 0000 and ALPN 0010
  removed) followed by `_` and the signature algorithms in their original
  order, truncated to 12 characters. Lowercase hex throughout.
- Raw outputs: `-r` sorted, `-o` original order.
- Cloudflare: JA4 sorts ClientHello extensions, which reduces the number of
  unique fingerprints for modern browsers and makes grouping easier.
- Licensing: JA4 (the TLS client method) is BSD 3-Clause, the same as JA3; the
  wider JA4+ family has its own licensing (see the FoxIO licence FAQ).
- JA4+ family from the FoxIO README: JA4S (TLS server response), JA4H (HTTP
  client), JA4L / JA4LS (latency), JA4X (X.509), JA4SSH, JA4T / JA4TS (TCP).
- The FoxIO README lists tool and vendor support, including Wireshark, Zeek,
  Arkime, Nginx and HAProxy plugins, Cloudflare, AWS CloudFront and AWS WAF.

## Limits and use (Cloudflare docs)

- Fingerprints are computed during the TLS handshake: not present for
  unencrypted HTTP, and with session resumption no further fingerprint
  calculation happens after the first handshake.
- Similar requests may share a fingerprint, so a fingerprint can be used in
  rules to block, challenge or allow a group of traffic, and mobile app traffic
  often shares one fingerprint across devices. Treat it as one signal and
  handle missing values.

## Verify

- [ ] The capture pipeline's JA4 matches the reference implementation on a sample capture.
- [ ] Rules handle a missing fingerprint.

## Checked

Method: docs-checked 2026-11-09 against salesforce/ja3 README, FoxIO-LLC/ja4 README and technical_details/JA4.md, Cloudflare JA3/JA4 page. Removed: the claim that Chrome 110 randomises extension order, "JA3 unreliable for modern browsers", the Cloudflare field name, Wireshark 4.2 field name, Suricata and AWS header details, threat-hunting for static TLS stacks, and the claim that clients can mimic fingerprints with uTLS and curl-impersonate.
