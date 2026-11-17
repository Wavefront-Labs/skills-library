---
id: computing-software.cybersecurity-defensive.cosign.attach-certificate-chain
name: attach-certificate-chain
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, certificate-chain, bring-your-own-pki, x509, certificate]
level: advanced
status: docs-checked
description: "Bring-your-own-PKI signing with cosign: attach an X.509 certificate and chain to a key-based signature, with chain ordering rules and the verify-side chain flag."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/specs/SIGNATURE_SPEC.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attaching a certificate and chain

```
cosign sign --key cosign.key --cert cosign.crt --cert-chain chain.crt <IMAGE DIGEST>
```

Flag text (long names `--certificate` and `--certificate-chain`):
- certificate: "path to the X.509 certificate in PEM format to include in the OCI Signature".
- chain: PEM list of CA certificates "Must start with the parent intermediate CA certificate of the signing certificate and end with the root certificate."

Order matters: intermediate first, root last.

Spec rules (SIGNATURE_SPEC):
- The certificate MUST embed the public key that verifies the signature.
- A chain requires the certificate to be present.
- Clients MUST validate any self-signed or trust-anchor certificates in the chain through an out-of-band mechanism, so a chain shipped with the signature is not itself trusted.
- Stored as registry annotations `dev.sigstore.cosign/certificate` and `dev.sigstore.cosign/chain` (the spec text also shows a `dev.cosignproject.cosign/` prefix in places).

Verify side: `--allow-certificate-chain` allows X.509 certificate chains in bundle verification material for v0.3+ bundles. The certificate flags also exist on `attest` and `sign-blob`.

## Checked

2026-11-08. Read in full: the `cosign sign`, `cosign verify` and `cosign sign-blob` references, SIGNATURE_SPEC.md, and the `--certificate` and `--certificate-chain` lines of the `cosign attest` reference. Confirmed the flag wording, the intermediate-first ordering, the spec MUST rules and the annotation keys (the spec text mixes the `dev.cosignproject.cosign/` and `dev.sigstore.cosign/` prefixes).

Method: documentation only; no commands were run.
