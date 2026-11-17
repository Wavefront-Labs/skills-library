---
id: computing-software.cryptography-implementation.openssl.offline-root-ca-operation
name: offline-root-ca-operation
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, offline-root-ca, root-ca, key-ceremony, openssl-ca, crl, air-gapped]
level: advanced
status: docs-checked
description: "Operate an offline root CA with OpenSSL: air-gapped host, key on HSM or protected media, scripted signing ceremonies for intermediates and CRLs, and records."
sources: ["https://docs.openssl.org/3.0/man1/openssl-ca/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Offline root CA operation

## Setup
- Dedicated air-gapped machine (or live USB) with no network; root key in an HSM or as an encrypted private key on
  protected media held in separate safes. The openssl-ca man page advises keeping signing keys on an HSM or smart
  card accessed through a crypto provider.
- Root certificate: set pathlen and a critical keyUsage with `keyCertSign, cRLSign` in the extensions section.
- Intermediates issued by the root sign everything day to day; the root signs only intermediates and CRLs.
- `openssl ca` is effectively single-user (no locking), which suits one operator at a ceremony.

## Signing session (ceremony)
1. Two or more people present; checklist and log sheet.
2. Boot the offline host, verify checksums of the tooling, mount the root key.
3. Bring the intermediate CSR on fresh media; verify its fingerprint against a value received over another channel.
4. Sign:
   ```sh
   openssl ca -config root.cnf -extensions v3_intermediate_ca -days 1825 -notext \
     -in int.csr -out int.pem
   openssl ca -config root.cnf -gencrl -crldays 180 -out root.crl
   ```
5. Export only the certificate and CRL; back up the CA database (`index.txt`, `serial`, `crlnumber`).
6. Unmount and store key media; sign the log.

## CRL cadence
Choose `-crldays` to cover the time until the next ceremony plus margin, and schedule ceremonies before the CRL's
`nextUpdate`.

## Verify
- [ ] Ceremony log and hashes of issued artifacts archived.
- [ ] `openssl verify -CAfile root.pem int.pem` passes and the CRL `nextUpdate` is checked.

## Checked

2026-11-01. Confirmed in the OpenSSL openssl-ca man page: `-config`, `-extensions`, `-days`, `-notext`, `-in`, `-out`, `-gencrl`, `-crldays`, the `database`/`serial`/`crlnumber` files, the no-locking single-user note and the HSM or smart card advice for signing keys. Removed: root validity range, AES-256 PKCS#8 storage detail, and the CA/Browser Forum and tutorial references, which were not read.
Method: documentation only; no commands were run.
