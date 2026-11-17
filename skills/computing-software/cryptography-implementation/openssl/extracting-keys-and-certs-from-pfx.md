---
id: computing-software.cryptography-implementation.openssl.extracting-keys-and-certs-from-pfx
name: extracting-keys-and-certs-from-pfx
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, pkcs12, pfx, pkcs12-extract, private-key-extraction, certificate-chain, pem]
level: practitioner
status: verified
description: "Extract the private key, leaf and chain from a PFX/PKCS#12 into clean PEM files: -nocerts, -clcerts, -cacerts, stripping bag attributes and handling passwords."
sources: ["https://docs.openssl.org/3.0/man1/openssl-pkcs12/", "https://docs.openssl.org/3.0/man1/openssl-pkey/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extracting keys and certs from PFX

Typical case: someone exported a `.pfx` from Windows or a vendor portal and nginx, HAProxy or a
Kubernetes secret needs `key.pem`, `cert.pem` and `chain.pem`.

## Extract
```
P='-passin file:pfxpass.txt'
openssl pkcs12 -in site.pfx $P -nocerts -noenc | openssl pkey -out site.key
openssl pkcs12 -in site.pfx $P -clcerts -nokeys | openssl x509 -out site.crt
openssl pkcs12 -in site.pfx $P -cacerts -nokeys -out chain-raw.pem
chmod 600 site.key
```
- `-noenc` (OpenSSL 3; `-nodes` on 1.1.1) leaves the extracted key unencrypted. Omit it to get
  an encrypted PKCS#8 key and supply `-passout`.
- Piping through `openssl pkey` / `openssl x509` drops the `Bag Attributes` and `friendlyName`
  lines that confuse some parsers.
- `-clcerts` gives the certificate(s) whose localKeyID matches a key; `-cacerts` everything else (tested: with only
  the leaf and one intermediate in the file, `-cacerts` returned just the intermediate).
- Old PFX files may need `-legacy` (see the legacy PKCS#12 skill).

## Clean the chain
`-cacerts` output can include the root and is in no guaranteed order. Rebuild:
```
openssl storeutl -noout -text -certs chain-raw.pem | grep -E "Subject:|Issuer:"
```
Keep intermediates only, ordered from the one that issued the leaf upward, then:
`cat site.crt intermediates.pem > fullchain.pem`.

## Confirm the pieces match
```
openssl pkey -in site.key -pubout -outform DER | openssl sha256
openssl x509 -in site.crt -noout -pubkey | openssl pkey -pubin -outform DER | openssl sha256
openssl verify -untrusted intermediates.pem site.crt
```

## Passwords and errors
- `Mac verify error: invalid password?` = wrong password, or an empty vs absent password.
  Try `-passin pass:` (empty) once; some Windows exports use empty, others no MAC at all
  (`-nomacver` skips the check; use only for files whose origin you trust).
- Multiple keys in one PFX: extract with `-info` to list localKeyIDs and match by hash.
- A PFX with no key bag has no key to extract; list the bags with `-info` (a key shows as `Shrouded Keybag`).

## Handle the key safely
The extracted unencrypted key is the crown jewel. Extract into a tmpfs or directly into the
destination secret store (`kubectl create secret tls site --cert=fullchain.pem --key=site.key`),
then delete local copies (`shred -u` on spinning disks; on SSDs rely on full-disk encryption).

## Verify
- [ ] Key and certificate SPKI hashes match.
- [ ] `fullchain.pem` has leaf first, then intermediates, no root.
- [ ] No unencrypted key copies remain outside the destination.
