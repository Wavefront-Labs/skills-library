---
id: computing-software.cryptography-implementation.openssl.cms-smime-signing
name: cms-smime-signing
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, openssl-cms, cms-signing, smime, pkcs7, detached-signature, signeddata, as2, rfc5652]
level: advanced
status: verified
description: "Create and verify CMS/S/MIME SignedData with openssl cms: detached vs attached, binary mode, including chain certs, -purpose any for non-email certs, and common verify errors."
sources: ["https://docs.openssl.org/3.0/man1/openssl-cms/", "https://datatracker.ietf.org/doc/html/rfc5652", "https://datatracker.ietf.org/doc/html/rfc8551"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CMS and S/MIME signing with openssl cms

CMS SignedData (RFC 5652) is the signature container behind S/MIME, AS2/EDI,
code signing (Authenticode is PKCS#7), firmware formats and many government
e-filing systems. `openssl cms` supersedes `openssl smime` (supports PSS,
ECDSA, newer content types).

## Sign

```bash
# Detached DER signature over a binary file
openssl cms -sign -binary -in invoice.xml -signer signer.crt -inkey signer.key \
  -certfile intermediate.crt -md sha256 -outform DER -out invoice.xml.p7s
# Attached (content inside) S/MIME email body
openssl cms -sign -in msg.txt -signer signer.crt -inkey signer.key -nodetach -out msg.smime
# RSA-PSS signer
openssl cms -sign ... -keyopt rsa_padding_mode:pss
```

- `-binary` stops MIME canonicalisation (CRLF conversion). Without it, text
  mode alters line endings and signatures over binary files fail elsewhere.
- `-certfile` adds intermediates so verifiers can build the chain.
- `-nocerts` omits even the signer cert (verifier must have it).
- Signed attributes (signing time, content type, message digest) are added by
  default; `-noattr` removes them - only for formats that require it.

## Verify

```bash
openssl cms -verify -binary -inform DER -in invoice.xml.p7s -content invoice.xml \
  -CAfile root.crt -out /dev/null
# Certificate whose EKU lacks emailProtection (for example a TLS server cert):
openssl cms -verify ... -purpose any
# Inspect structure
openssl cms -cmsout -print -inform DER -in invoice.xml.p7s | less
```

`Verification successful` and exit code 0 means signature and chain are OK.

## Common errors

| Error | Cause |
|---|---|
| `Verify error: unsuitable certificate purpose` | Signer cert has an extendedKeyUsage that does not include emailProtection (a cert with no EKU at all verifies); use `-purpose any` if appropriate |
| `unable to get local issuer certificate` | Missing intermediate: embed it at signing time with `-certfile`, or put it in the `-CAfile` bundle on verify (`cms` has no `-untrusted`, and a verify-side `-certfile` did not supply the chain on 3.2.3) |
| `content verify error` / `digest failure` | Content changed, or text vs binary mode mismatch |
| `no content` (`CMS routines:check_content`) | Detached sig verified without `-content` |

Use `-noverify` (skips verifying the signer certificate; `-no_signer_cert_verify` is not an `openssl cms` option) only to debug signature vs chain issues, never in production.

## Verify

- [ ] Signature verifies with the partner's tooling, not only OpenSSL.
- [ ] Chain includes intermediates; signer cert EKU fits the purpose.
- [ ] Binary files signed with `-binary`; tampered content fails.

## Checked
- OpenSSL 3.2.3 end-to-end with a private root, an intermediate and RSA/EC test certificates: detached DER sign and verify; tampered content and missing `-content` errors; TLS-EKU signer rejected and accepted with `-purpose any`; a no-EKU signer verifies; `-nocerts`, `-noattr`, RSA-PSS (`rsassaPss` in the output); chain errors with and without an embedded intermediate; `-binary` versus text-mode canonicalisation mismatch in both directions; `-noverify`.
- Not claimed beyond that: partner-tool interoperability.
