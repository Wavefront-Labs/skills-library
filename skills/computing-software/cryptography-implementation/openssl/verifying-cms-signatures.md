---
id: computing-software.cryptography-implementation.openssl.verifying-cms-signatures
name: verifying-cms-signatures
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, cms-verify, openssl-cms, pkcs7, smime, detached-signature, signature-verification, signed-attributes]
level: practitioner
status: verified
description: "Verify CMS/PKCS#7 and S/MIME signatures with openssl cms -verify: detached content, signer chains, -purpose, inspecting signed attributes and extracting signers."
sources: ["https://docs.openssl.org/3.0/man1/openssl-cms/", "https://www.rfc-editor.org/rfc/rfc5652", "https://www.rfc-editor.org/rfc/rfc8551"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Verifying CMS signatures

## Detached signature over a file
```
openssl cms -verify -binary -inform DER -in file.p7s -content file.bin \
  -CAfile trust.pem -purpose any -out verified.bin
# "CMS Verification successful"
```
- `-binary` stops canonical text (CRLF) conversion; omit it only for S/MIME text.
- `-purpose any` disables the default S/MIME purpose check (tested: a code-signing-only certificate failed with
  `unsuitable certificate purpose` until `-purpose any` was added). For code or
  document signing, prefer an explicit policy check in your application rather than `any`.
- `-untrusted intermediates.pem` supplies intermediates not embedded in the signature.

## Attached (encapsulated) signature
```
openssl cms -verify -binary -inform DER -in signed.p7m -CAfile trust.pem -out content.bin
```
Keep `-binary` for non-text content: without it a test on Windows wrote output that differed from the signed file.

## S/MIME mail
```
openssl cms -verify -in message.eml -CAfile trust.pem -out body.txt
```

## Inspect and extract
```
openssl cms -cmsout -print -inform DER -in file.p7s | less     # signed attributes: contentType, messageDigest, signingTime
openssl cms -verify ... -signer signer.pem                     # writes signer certificate(s)
openssl pkcs7 -inform DER -in file.p7s -print_certs            # embedded certificates
```

## What verification does and does not prove
- Proves: content hash matches messageDigest, signature over signed attributes verifies, signer chain to your trust
  anchors (unless `-noverify`).
- Does not prove: the signer was authorised for this content (check subject/EKU/policy yourself), the time of
  signing (signingTime is self-asserted; use an RFC 3161 timestamp).

## Gotchas
- `-noverify` skips chain validation and is for debugging only.
- Signed attributes must be DER-sorted; some signers produce BER that strict verifiers reject.
- PEM vs DER vs S/MIME input formats: `-inform` must match.

Tested on 3.2.3: detached and attached DER signatures verify (`CMS Verification successful`); a changed content byte gives
`CMS Verification failure`; an untrusted self-signed signer gives `Verify error: self-signed certificate`; `-noverify`
skips the chain check; `-signer` writes the signer certificate.

## Verify
- [ ] Modified content byte makes verification fail.
- [ ] Untrusted signer chain fails without `-noverify`.
