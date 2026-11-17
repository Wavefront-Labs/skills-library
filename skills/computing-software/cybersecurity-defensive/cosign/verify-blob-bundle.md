---
id: computing-software.cybersecurity-defensive.cosign.verify-blob-bundle
name: verify-blob-bundle
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, verify-blob, blob-stdin, bundle, keyless]
level: practitioner
status: docs-checked
description: "Verify a file with cosign verify-blob using --bundle plus identity, public key or KMS, read the blob from stdin, and trusted-root options."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify-blob.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# verify-blob

You may verify against "a key, a bundle (optionally with trusted root), or a kms reference". The preferred input is a Sigstore bundle via `--bundle`. The blob is a file path or `-` for stdin.

```
# keyless
cosign verify-blob --bundle artifact.sigstore.json \
  --certificate-identity foo@example.com \
  --certificate-oidc-issuer https://accounts.google.com <blob>

# bundle plus trusted root
cosign verify-blob --bundle artifact.sigstore.json --trusted-root trusted_root.json <blob>

# public key
cosign verify-blob --bundle artifact.sigstore.json --key cosign.pub <blob>

```

For stdin, pass `-` as the blob argument instead of a path.

Also in the examples: `--key` as awskms, gcpkms, azurekms or hashivault URIs, or `gitlab://[OWNER]/[PROJECT_NAME]` / `gitlab://[PROJECT_ID]`. If you use a key, bundle or trusted root you must give its path on disk.

Flags: `--insecure-ignore-tlog`, `--insecure-ignore-sct` (skip the embedded SCT check), `--use-signed-timestamps` (verify rfc3161 timestamps), `--allow-certificate-chain` (allow X.509 certificate chains in bundle verification material for v0.3+ bundles), and the `--certificate-github-workflow-*` set (name, ref, repository, sha, trigger).

For keyless flows, either `--certificate-identity` or `--certificate-identity-regexp` must be set, and either `--certificate-oidc-issuer` or `--certificate-oidc-issuer-regexp` must be set.

## Checked

2026-11-04. Confirmed against the cosign verify-blob docs: synopsis quotes, examples, KMS and GitLab forms, flag descriptions, keyless requirement. Removed: the curl stdin example (the page says only that `-` means stdin) and the claim that a one-byte change fails the check.
Method: documentation only; no commands were run.
