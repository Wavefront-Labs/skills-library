---
id: computing-software.cryptography-implementation.openssl.revoking-certificates-with-openssl-ca
name: revoking-certificates-with-openssl-ca
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, ca-revoke, certificate-revocation, openssl-ca, crl, revocation-reason, index-txt, private-ca]
level: practitioner
status: verified
description: "Revoke certificates in an openssl ca private CA with reason codes and compromise dates, regenerate and publish CRLs, and check revocation state in index.txt."
sources: ["https://docs.openssl.org/3.0/man1/openssl-ca/", "https://www.rfc-editor.org/rfc/rfc5280#section-5.3.1", "https://docs.openssl.org/3.0/man1/openssl-crl/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Revoking certificates with openssl ca

## Revoke
```
openssl ca -config ca.cnf -revoke newcerts/1A2B.pem -crl_reason keyCompromise -crl_compromise 20261015120000Z
```
Reason names: `unspecified`, `keyCompromise`, `CACompromise`, `affiliationChanged`, `superseded`,
`cessationOfOperation`, `certificateHold`, `removeFromCRL`. `-crl_compromise` (for keyCompromise) and
`-crl_CA_compromise` record when the compromise happened (invalidityDate-style data).

If you no longer have the certificate file, mark it revoked directly by serial in `index.txt` (status `R`, revocation
date and reason) with care, or keep `newcerts/` (the CA writes every issued cert there by serial).

## Regenerate and publish the CRL
```
openssl ca -config ca.cnf -gencrl -out crl/ca.crl.pem -crldays 7
openssl crl -in crl/ca.crl.pem -noout -text | grep -A3 "Serial Number: 1A2B"
openssl crl -in crl/ca.crl.pem -outform DER -out crl/ca.crl     # what most CDP URLs serve
```
Config needs `crlnumber` file and `[crl_ext] authorityKeyIdentifier=keyid:always`. Publish to the URL in the
certificates' CRL distribution points before nextUpdate every time.

## index.txt columns
`status (V/R/E) | expiry | revocation date[,reason] | serial | filename | subject` (filename is `unknown` for certificates issued by `openssl ca`; `-crl_compromise` stores `revdate,keyTime,compromisedate`). Back it up with the CA key; losing it
means you cannot produce correct CRLs.

## After revoking
- Update the OCSP responder (restart if it reads index.txt at startup).
- If the reason is keyCompromise, find every other certificate with the same public key and revoke those too.
- `certificateHold` is reversible but poorly supported; avoid it.

## Verify
- [ ] `openssl verify -crl_check -CAfile ca.pem -CRLfile crl/ca.crl.pem leaf.pem` reports "certificate revoked".
- [ ] CRL at the CDP URL has the new crlNumber.

## Checked
- OpenSSL 3.2.3 mini CA run: issued, revoked by `newcerts/<serial>.pem` with every listed reason name, used `-crl_compromise`, generated PEM and DER CRLs, and `openssl verify -crl_check` reported "certificate revoked".
- With `-crl_compromise` the index.txt revocation field reads `revdate,keyTime,compromisedate`; a second revoke of the same serial errors "Already revoked".
