---
id: computing-software.cybersecurity-defensive.cosign.k8s-keychain
name: k8s-keychain
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, k8s-keychain, kubernetes, workload-identity, k8s-secret]
level: practitioner
status: docs-checked
description: "Use cosign inside Kubernetes with --k8s-keychain for registry credentials and k8s:// URIs for keys stored in Secrets."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_generate-key-pair.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes keychain and secret keys

Registry credentials: `--k8s-keychain` means "whether to use the kubernetes keychain instead of the default keychain (supports workload identity)". It is available on sign, verify, attest, tree, clean, download, save and load.

```
cosign sign --k8s-keychain --key k8s://[NAMESPACE]/[KEY] <IMAGE DIGEST>
cosign verify --k8s-keychain --key k8s://[NAMESPACE]/[KEY] <IMAGE>
```

Keys: `--key` accepts a "path to the private key file, KMS URI or Kubernetes Secret", with the form `k8s://[NAMESPACE]/[KEY]`.

Create a key pair directly into a Secret:

```
cosign generate-key-pair k8s://[NAMESPACE]/[NAME]
```

Note the Kubernetes form is a positional argument, while KMS providers use `--kms`.

Gotchas:
- Generating prompts for a password; set `COSIGN_PASSWORD` to avoid the prompt.

## Checked

2026-11-04. Confirmed on the cosign sign, verify, attest, tree, clean, download, save, load and generate-key-pair reference pages: `--k8s-keychain` quote and commands, the `--key` description including Kubernetes Secret, `k8s://[NAMESPACE]/[KEY]` examples, the positional `k8s://` form versus `--kms`, and COSIGN_PASSWORD. Removed: the RBAC remark.

Method: documentation only; no commands were run.
