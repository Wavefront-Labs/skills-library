---
id: computing-software.cybersecurity-defensive.suricata.tls-certificate-and-version-keywords
name: tls-certificate-and-version-keywords
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [tls-sni, tls-cert-subject, tls-version, ssl-state, tls-certs]
level: practitioner
status: docs-checked
description: "Match TLS fields: tls.sni, cert subject, issuer, serial, fingerprint, validity dates, tls.version, ssl_state, random and alpn buffers."
sources: ["https://docs.suricata.io/en/latest/rules/tls-keywords.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TLS keywords

Most are sticky buffers supporting `fast_pattern`; legacy names (`tls_sni`, `tls_cert_subject`...) still work.

- `tls.sni`, `tls.cert_subject`, `tls.cert_issuer`, `tls.cert_serial` (colon-separated hex), `tls.cert_fingerprint` (SHA-1), `tls.subjectaltname`, `tls.certs` (raw match per chain certificate).
- `tls.cert_chain_len`: unsigned 32-bit, with `<`, `>`, `<>`, `!`.
- `tls.store`: stores certificates to the directory `output.tls-store.certs-log-dir`.
- Dates: `tls_cert_notbefore:1998-05-01<>2008-05-01;`, `tls_cert_notafter:>2015;`. `YYYY` means `YYYY-01-01`. `tls_cert_expired` and `tls_cert_valid` check dates only, not chain validity.
- `tls.version:1.2;` (1.0 to 1.3, or hex); `ssl_version:sslv2,sslv3;` accepts lists and `!`.
- `ssl_state`: client_hello, server_hello, client_keyx, server_keyx, unknown.
- `tls.random`, `tls.random_time` (first 4 bytes), `tls.random_bytes` (last 28), `tls.alpn`.

Example: `tls.sni; content:"oisf.net"; nocase; isdataat:!1,relative;`

## Checked

2026-11-04. Every keyword, value list and example above confirmed against the Suricata SSL/TLS Keywords page.

Method: documentation only; no commands were run.
