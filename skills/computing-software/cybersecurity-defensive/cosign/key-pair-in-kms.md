---
id: computing-software.cybersecurity-defensive.cosign.key-pair-in-kms
name: key-pair-in-kms
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, kms-key-pair, gitlab-key, github-key, k8s-secret, hashivault]
level: advanced
status: docs-checked
description: "Generate cosign key pairs inside AWS, GCP, Azure or Vault KMS, or store them in Kubernetes Secrets, GitHub and GitLab, with the exact command forms."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_generate-key-pair.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key pairs in KMS and platforms

KMS providers use `--kms`:

```
cosign generate-key-pair --kms awskms://[ENDPOINT]/[ID/ALIAS/ARN]
cosign generate-key-pair --kms gcpkms://projects/[PROJECT]/locations/global/keyRings/[KEYRING]/cryptoKeys/[KEY]
cosign generate-key-pair --kms azurekms://[VAULT_NAME][VAULT_URI]/[KEY]
cosign generate-key-pair --kms hashivault://[KEY]
```

Platform stores are positional arguments:

```
cosign generate-key-pair k8s://[NAMESPACE]/[NAME]
cosign generate-key-pair github://[OWNER]/[PROJECT_NAME]
cosign generate-key-pair gitlab://[OWNER]/[PROJECT_NAME]
cosign generate-key-pair gitlab://[PROJECT_ID]
cosign generate-key-pair gitlab://[GROUP_NAME]              # accessible to all projects in the group
cosign generate-key-pair gitlab://[GROUP_NAME]/[SUBGROUP_NAME]
```

Local files: `cosign generate-key-pair` writes `cosign.key` and `cosign.pub`; `--output-key-prefix my-name` writes `my-name.key` and `my-name.pub` (defaults to `cosign`). The `--kms` flag text is "create key pair in KMS service to use for signing". The inherited `-t, --timeout` defaults to 3m0s.

Caveat from the page: the command interactively prompts for a password; the `COSIGN_PASSWORD` environment variable can provide one.

## Checked

2026-11-04. Confirmed against the cosign generate-key-pair docs page: every KMS and platform command form, local file naming, flag text, timeout default, password caveat. Removed: the claim that a KMS private key stays in the service, the instruction to sign and verify with the same URI (not on this page), and the gotchas about whether platform stores prompt and where cloud credentials are documented.
Method: documentation only; no commands were run.
