---
id: computing-software.cybersecurity-defensive.security-architecture.tls-configuration
name: tls-configuration
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [cryptography, tls-configuration, tls-1-3, cipher-suites, mozilla-ssl-config, testssl, ssl-labs, forward-secrecy, ocsp-stapling, mtls]
level: practitioner
status: draft
description: "Configure TLS on servers and load balancers to a modern profile (TLS 1.2/1.3, AEAD ciphers, forward secrecy), test with testssl.sh/SSL Labs and handle legacy clients."
sources: ["Mozilla Server Side TLS guidelines and SSL Configuration Generator", "NIST SP 800-52 Rev. 2 TLS implementation guidelines", "testssl.sh documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TLS configuration

**Goal:** encrypted connections that resist downgrade and known attacks, without breaking the
clients you must support.

## Profiles (Mozilla guidelines)
- **Modern**: TLS 1.3 only. For services whose clients you control.
- **Intermediate** (default for most): TLS 1.2 and 1.3; TLS 1.2 ciphers limited to ECDHE with
  AES-GCM or ChaCha20-Poly1305.
- **Old**: only for documented legacy clients, isolated on separate endpoints.

## NGINX (intermediate)
```
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
ssl_prefer_server_ciphers off;
ssl_session_timeout 1d;
ssl_session_tickets off;
ssl_stapling on; ssl_stapling_verify on;
add_header Strict-Transport-Security "max-age=63072000" always;
```
Generate per-server configs with the Mozilla SSL Configuration Generator for Apache, HAProxy,
IIS, AWS ELB security policies, etc. For cloud load balancers choose the provider's TLS 1.2+
policy (e.g. `ELBSecurityPolicy-TLS13-1-2-2021-06`).

## Windows / IIS
Disable SSL 2/3, TLS 1.0/1.1 via SCHANNEL registry keys or IIS Crypto (test first: old
.NET apps and SQL clients may depend on TLS 1.0).

## Test
```
testssl.sh --severity MEDIUM https://www.example.com
nmap --script ssl-enum-ciphers -p 443 www.example.com
openssl s_client -connect www.example.com:443 -tls1_1   # should fail
```
Public sites: Qualys SSL Labs (aim for A/A+).

## mTLS
For service-to-service, require client certificates from an internal CA; check revocation
and pin the expected CA, not any public CA.

## Gotchas
- Disabling TLS 1.0/1.1 breaks old Java, Windows 7, embedded devices: inventory clients via connection logs first.
- Certificate chain incomplete: browsers may cope, APIs and mobile clients fail.
- TLS termination at a load balancer leaves the backend hop in clear unless re-encrypted.
- Session tickets without key rotation weaken forward secrecy.

## Verify
- [ ] testssl.sh shows no TLS < 1.2, no CBC/RC4/3DES/NULL ciphers, forward secrecy on all suites.
- [ ] Legacy exceptions documented with owner and end date.
