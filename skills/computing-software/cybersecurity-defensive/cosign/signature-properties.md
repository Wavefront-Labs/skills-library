---
id: computing-software.cybersecurity-defensive.cosign.signature-properties
name: signature-properties
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, signature-properties, rekor-bundle, signed-entry-timestamp, rfc3161timestamp]
level: sme
status: docs-checked
description: "The properties of a cosign signature object: payload, signature, certificate, chain, Rekor bundle with SignedEntryTimestamp, and RFC 3161 timestamp."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/specs/SIGNATURE_SPEC.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signature properties (spec)

REQUIRED:
- `payload` bytes: signed data; contains the image digest in a well-known place.
- `mediaType` of the payload.
- `signature`: base64, from a supported scheme.

OPTIONAL:
- `certificate`: PEM X.509 that MUST embed the public key verifying the signature.
- `chain`: PEM certificate chain; requires `certificate`. Self-signed or trust-anchor certificates in it must be validated out-of-band.
- `bundle`: JSON for offline verification.
- `rfc3161timestamp`: a timestamp authority's response (RFC3161Timestamp JSON).

Required bundle fields: `SignedEntryTimestamp` (Rekor-signed over logIndex, body and integratedTime) and `Payload` with:
- `body` (Rekor entry body)
- `integratedTime` (UNIX time the entry was integrated)
- `logIndex`
- `logID` (SHA256 of the DER-encoded log public key at inclusion time)

In the registry the signature, certificate and chain are stored as layer annotations. Verification itself follows the Sigstore client specification (architecture-docs client-spec section 4).

## Checked

2026-11-04. Confirmed in the cosign Signature Specification Properties section: required and optional properties, certificate and chain rules, required bundle fields and their definitions, rfc3161timestamp, the layer annotations for signature, certificate and chain, and the pointer to the client specification. Removed: the claim that the bundle is also a layer annotation, the download signature suggestion and the claim about confirming log inclusion without Rekor.

Method: documentation only; no commands were run.
