---
id: computing-software.systems-network-administration.pki-tls-administration.openssl-inspect-certs
name: openssl-inspect-certs
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [openssl-inspect-certs, pki-openssl-tools, openssl, x509, inspect, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Read certificates and chains with openssl x509 and s_client, print selected fields, fingerprints and dates."
sources:
  - https://docs.openssl.org/master/man1/openssl-x509/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspect certificates, CSRs and CRLs
Goal: answer "what is in this file" in one command.
```
openssl x509 -in c.pem -noout -subject -issuer -serial -dates -fingerprint
openssl x509 -in c.pem -noout -ext subjectAltName,keyUsage,extendedKeyUsage
openssl x509 -in c.der -inform DER -text -noout
openssl crl  -in x.crl -noout -issuer -lastupdate -nextupdate
openssl x509 -in c.pem -checkend 1209600 -noout   # non-zero exit if it expires within 14 days (1209600 s)
openssl storeutl -noout -text -certs bundle.pem   # every cert in a bundle
```
- `-ext` takes a comma-separated list of extension names, for example `subjectAltName,keyUsage`.
- `-fingerprint` prints the digest of the DER certificate; the digest algorithm is chosen with the digest options on the openssl-x509 page.
- `-checkend` without `-multi` checks one certificate; with `-multi` it fails if any certificate in the input will expire within the period.
- Fetch a live chain: `openssl s_client -connect host:443 -servername host -showcerts </dev/null`.
Gotcha: a chain file passed to `-checkend` without `-multi` is not fully checked; add `-multi` so an expiring intermediate is caught.
Verify:
- [ ] Output names match the CSR you submitted.
- [ ] `-checkend` returns 0 for every cert in the deployment.

## Checked
2026-11-03. Confirmed in the openssl-x509, openssl-crl, openssl-storeutl and openssl-s_client manual pages: `-subject`, `-issuer`, `-serial`, `-dates`, `-fingerprint`, `-ext`, `-checkend` and `-multi`, `openssl crl -issuer -lastupdate -nextupdate -noout`, `storeutl -noout -text -certs`, `s_client -connect -servername -showcerts`. Removed: the `-sha256` flag, the OpenSSL 1.1.1 claim for `-ext`, the claim that `x509` shows only the first bundle cert and the `awk` split, and the GMT claim (none is on the pages). The `-checkend 1209600` comment is arithmetic (14 days in seconds).
Method: documentation only; no commands were run.
