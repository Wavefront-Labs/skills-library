---
id: computing-software.cybersecurity-defensive.application-security.sops-encrypted-secrets
name: sops-encrypted-secrets
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [sops, encrypted-secrets, age, kms, gitops, secrets-in-git]
level: practitioner
status: docs-checked
description: "Keep secrets encrypted in git with SOPS: supported formats and key backends, .sops.yaml encrypted_regex, age keys, and decrypting in Flux with age or cloud KMS."
sources: ["https://getsops.io/docs/", "https://raw.githubusercontent.com/getsops/sops/main/README.rst", "https://fluxcd.io/flux/guides/mozilla-sops/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SOPS encrypted secrets

SOPS (Secrets OPerationS) is an editor of encrypted files supporting YAML, JSON, ENV, INI and BINARY formats.
It encrypts with AWS KMS, GCP KMS, Azure Key Vault, HuaweiCloud KMS, age and PGP. It began at Mozilla (2015)
and was donated to the CNCF as a Sandbox project in 2023. Licence: Mozilla Public License 2.0. Report
security issues privately via the GitHub advisory form.

## Configuration
A `.sops.yaml` holds `creation_rules` with `path_regex` and `encrypted_regex`. For Kubernetes Secrets the
Flux guide uses `encrypted_regex: ^(data|stringData)$` so only the payload fields are encrypted; add other
fields if you encrypt other object kinds. The file applies recursively to sub-directories, and different
directories can have their own configs, so contributors need not name the key by hand.

## Encrypting
`sops --encrypt --in-place file.yaml` (PGP, per the Flux guide). With age: generate a key with
`age-keygen -o age.agekey`, then `sops --age=<public key> ...` to encrypt. The Flux guide recommends age
over OpenPGP where possible.

## Decrypting in Flux
- Create a Kubernetes secret from the private key; for age the key name must end with `.agekey` to be
  detected. The secret can hold more than one key; SOPS tries them until one works.
- Set the decryption provider to `sops` and `secretRef` on the Flux Kustomization (CLI:
  `--decryption-provider=sops --decryption-secret=<name>`).
- With AWS or GCP KMS no `secretRef` is needed: bind an IAM role with access to the KMS keys to the
  kustomize-controller service account (see Flux's AWS/GCP integration docs).
- Gotcha: Flux patches applied to an encrypted resource can introduce fields matching `encrypted_regex`,
  and SOPS then fails to decrypt.

## Hygiene
Back up decryption keys offline (password manager or offline storage) and consider deleting the secret key
from your workstation. Check the encrypted file before committing that sensitive fields are encrypted. If
someone loses access or leaves, rotate the secret values themselves, not only the key list.
For details of editing, rotation and key management, read the SOPS Usage and Reference pages.

## Checked
2026-11-01. Confirmed against the SOPS docs landing page and README, and the Flux "Manage Kubernetes secrets
with SOPS" guide. Removed: Vault transit, every sops CLI subcommand beyond `--encrypt --in-place` and
`--age`, `SOPS_AGE_KEY_FILE`, `updatekeys`, `-r` rotation, `exec-env`, ciphertext prefix check, Argo CD
plugins, OIDC-in-CI advice (not on the pages read; the rotation advice above is general practice).
Method: documentation only; no commands were run.
