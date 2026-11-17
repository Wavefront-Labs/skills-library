---
id: computing-software.cryptography-implementation.openssl.running-an-openssl-ocsp-responder
name: running-an-openssl-ocsp-responder
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, ocsp-responder, ocsp, openssl-ocsp, private-ca, revocation, ocsp-signing, ocsp-nocheck]
level: practitioner
status: docs-checked
description: "Run and query an openssl ocsp responder for a private CA: delegated OCSP signing certificate, index file, nextUpdate, nonce handling and production caveats."
sources: ["https://docs.openssl.org/3.0/man1/openssl-ocsp/", "https://docs.openssl.org/3.0/man1/openssl-ca/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running an openssl ocsp responder

## 1. Delegated responder certificate
Issue a certificate from the CA for the responder with:
```
[v3_ocsp]
basicConstraints = critical, CA:FALSE
keyUsage = critical, digitalSignature
extendedKeyUsage = critical, OCSPSigning
```

## 2. Run the responder (uses the `openssl ca` index.txt)
```
openssl ocsp -index index.txt -CA ca.pem -rsigner ocsp.pem -rkey ocsp.key \
  -port 2560 -nmin 60 -text -out ocsp.log
```
`-nmin`/`-ndays` set the number of minutes or days fresh revocation information is available (the `nextUpdate` field); with neither option, `nextUpdate` is omitted, meaning fresh information is immediately available.

## 3. Query
```
openssl ocsp -issuer ca.pem -cert leaf.pem -url http://127.0.0.1:2560 -resp_text -CAfile ca.pem
# Output ends with:  leaf.pem: good   (or revoked, with reason and time)
```
Put the URL in leaf certificates: `authorityInfoAccess = OCSP;URI:http://ocsp.example.internal/`.

## Production caveats
- `-multi N` runs N responder child processes (POSIX systems with fork); children detect changes in the CA index file and reload it. `-timeout` is recommended to bound how long a child waits for a client.
- `-index` requires `-CA` and `-rsigner` as well.
- Responses can also be produced for a given serial on the command line (`-issuer`, `-serial`, `-respout`) without running a server.

## Verify
- [ ] Revoking a cert in the index and restarting yields `revoked` for that serial.
- [ ] Responses verify against the CA and carry the `nextUpdate` you set with `-nmin`/`-ndays`.

## Checked
2026-11-01. Confirmed against the openssl-ocsp man page: `-index`, `-CA`, `-rsigner`, `-rkey`, `-port`, `-nmin`/`-ndays` (nextUpdate omitted when absent), `-multi` (reloads index), `-issuer`, `-serial`, `-cert`, `-url`, `-text`, `-resp_text`, `-respout`, `-CAfile`; and the x509v3_config page for the OCSPSigning extended key usage and the authorityInfoAccess OCSP URI form. Removed: the nocheck OID line, validity advice, third-party responder names, nonce claims and the old single-threaded/restart claim (the man page says `-multi` children reload the index).
Method: documentation only; no commands were run.
