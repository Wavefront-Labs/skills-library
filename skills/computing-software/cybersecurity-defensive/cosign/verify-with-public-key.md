---
id: computing-software.cybersecurity-defensive.cosign.verify-with-public-key
name: verify-with-public-key
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, verify, public-key, key-url, cosign-pub]
level: intro
status: docs-checked
description: "Verify image signatures with cosign verify --key using a public key file, URL, KMS or secret reference, what exit 0 means and what the output contains."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Verify with a public key

```
cosign verify --key cosign.pub <IMAGE>
cosign verify --key https://host.for/[FILE] <IMAGE>
cosign verify --key k8s://[NAMESPACE]/[KEY] <IMAGE>
cosign verify --key hashivault://[KEY] <IMAGE>
```

Per the README, the command "returns 0 if at least one cosign formatted signature for the image is found matching the public key". Other signature formats have caveats. Valid payloads print to stdout as JSON.

Typical text output:
- The cosign claims were validated
- The signatures were verified against the specified public key

The payload includes `Docker-manifest-digest`; that digest is how a detached signature is tied to the image.

Tips:
- Several images: `cosign verify --key cosign.pub IMG1 IMG2`.
- Check extra claims with `-a key=value`.
- Output is JSON by default; `-o text` changes it.
- Keyless flows need `--certificate-identity` (or `-regexp`) and an issuer flag instead of `--key`.

## Checked

2026-11-04. Confirmed in the cosign README (Verify a container against a public key: exit 0 wording, JSON payloads on stdout, the two printed checks, the digest in the payload) and on the cosign verify reference page (`--key` forms, `-a`, `-o` json or text, multiple images). Removed: the advice about pinning digests and the claim about what happens without `--key`.

Method: documentation only; no commands were run.
