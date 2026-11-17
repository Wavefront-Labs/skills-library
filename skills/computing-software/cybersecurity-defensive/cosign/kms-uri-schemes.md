---
id: computing-software.cybersecurity-defensive.cosign.kms-uri-schemes
name: kms-uri-schemes
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, kms, kms-uri, key-from-env, awskms, gcpkms, azurekms, hashivault]
level: practitioner
status: docs-checked
description: "The --key URI forms cosign accepts for AWS KMS, GCP KMS, Azure Key Vault, HashiCorp Vault, env variables, GitLab and Kubernetes, with sign and verify examples."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KMS and reference key URIs

`--key` takes a file path or a URI:

```
--key awskms://[ENDPOINT]/[ID/ALIAS/ARN]
--key gcpkms://projects/[PROJECT]/locations/global/keyRings/[KEYRING]/cryptoKeys/[KEY]/versions/[VERSION]
--key azurekms://[VAULT_NAME][VAULT_URI]/[KEY]
--key hashivault://[KEY]
--key k8s://[NAMESPACE]/[KEY]
--key env://[ENV_VAR]
--key gitlab://[OWNER]/[PROJECT_NAME]      (verify example)
--key gitlab://[PROJECT_ID]                (verify example)
--key https://host.for/[FILE]              (verify example, key by URL)
```

The flag text is "path to the private key file, KMS URI or Kubernetes Secret" for `cosign sign` and "path to the public key file, KMS URI or Kubernetes Secret" for `cosign verify`. Sign example: `cosign sign --key gcpkms://... <IMAGE DIGEST>`; verify examples use the same URI forms, for example `cosign verify --key hashivault://[KEY] <IMAGE>`.

Notes:
- The sign docs show a `/versions/[VERSION]` suffix for GCP; the verify docs omit it.
- The awskms and azurekms forms appear in the sign examples; the gitlab, https and (for verify) gcpkms, hashivault and k8s forms appear in the verify examples; env and k8s and hashivault appear in both.
- Create a key pair in a KMS with `cosign generate-key-pair --kms <KMS URI>`; the generate-key-pair page lists awskms, azurekms, gcpkms and hashivault.
- The README says cosign supports HashiCorp Vault, AWS KMS, GCP KMS and Azure Key Vault, and that additional providers, such as OVHcloud KMS, are available as external plugins.

## Checked

2026-11-04. Confirmed against the cosign sign, verify and generate-key-pair docs and the README: every URI form, flag text, GCP version-suffix difference, provider list, OVHcloud plugin. Removed: the claim that the private key never leaves the KMS and verify fetches the public key, the "(verify, public-key)" scope on gitlab, and the line that env:// reads the key from the variable (examples show only the form).
Method: documentation only; no commands were run.
