---
id: computing-software.systems-network-administration.pki-tls-administration.openssl-ca-sign-revoke
name: openssl-ca-sign-revoke
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [openssl-ca-sign-revoke, pki-openssl-ca, openssl, openssl-ca, gencrl, revoke, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Sign a CSR with a chosen extensions section, revoke a certificate and publish a CRL using openssl ca."
sources:
  - https://docs.openssl.org/master/man1/openssl-ca/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signing and revoking with openssl ca
Goal: issue and revoke certificates with an auditable database.
```
openssl ca -config openssl.cnf -extfile ext.cnf -extensions server_ext \
  -in leaf.csr -out certs/leaf.crt -notext -batch
openssl ca -config openssl.cnf -revoke certs/leaf.crt -crl_reason keyCompromise
openssl ca -config openssl.cnf -gencrl -out crl/ca.crl
openssl crl -in crl/ca.crl -noout -text | head
```
- Always use `-notext` to keep outputs clean.
- Reasons (case insensitive): unspecified, keyCompromise, CACompromise, affiliationChanged, superseded, cessationOfOperation, certificateHold, removeFromCRL. Setting any reason makes the CRL v2.
- Regenerate the CRL before nextUpdate and after every revocation, then publish it to the CDP URL.
Gotcha: `-batch` asks no questions and certifies automatically, so a wrong CSR is signed silently; inspect the CSR first.
Verify:
- [ ] `openssl verify -CAfile ca.crt -crl_check -CRLfile ca.crl leaf.crt` fails with a revoked-certificate error after revocation.
- [ ] `openssl ca -config openssl.cnf -status <serial>` shows the revoked state.

## Checked
2026-11-03. Confirmed in the openssl-ca and openssl-verify manual pages: `-extfile` with `-extensions`, `-in`, `-out`, `-notext`, `-batch` (no questions, certify automatically), `-revoke`, `-crl_reason` values, `-gencrl`, `-status serial`, `-crl_check` and `-CRLfile` on `openssl verify`. Removed: the same-key renewal claim, the quoted prompt and error strings, and the `R` index-line claim (not on the page).
Method: documentation only; no commands were run.
