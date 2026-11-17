---
id: computing-software.devops-ci-cd.flux.sops-cloud-kms-and-gpg
name: sops-cloud-kms-and-gpg
category: computing-software
field: devops-ci-cd
product: flux
tags: [sops, kms, gpg, openpgp, workload-identity]
level: advanced
status: docs-checked
description: "Decrypt SOPS secrets in Flux with OpenPGP keys or AWS, Azure and GCP KMS using secret-less workload identity."
sources:
  - https://fluxcd.io/flux/guides/mozilla-sops/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Besides age, Flux supports OpenPGP and cloud key management services for SOPS decryption.

OpenPGP: generate a key with no passphrase (`%no-protection`), export the secret key into a Secret named in `decryption.secretRef`, and commit only the public key if teammates need to create files:

```sh
gpg --export-secret-keys --armor "${KEY_FP}" |
kubectl create secret generic sops-gpg \
  --namespace=flux-system --from-file=sops.asc=/dev/stdin
```

Add a `.sops.yaml` with `creation_rules` using `pgp: ${KEY_FP}` and `encrypted_regex: ^(data|stringData)$`. The public key can create new files, but editing existing files needs the private key because SOPS computes a MAC over all values.

AWS KMS and GCP KMS: you do not need the `secretRef` under the decryption block (skip `--decryption-secret` in `flux create kustomization`). Bind an IAM role with access to the KMS keys to the `kustomize-controller` ServiceAccount in `flux-system`. For setting up SOPS authentication for AWS KMS, Azure Key Vault and GCP KMS, see the Flux AWS, Azure and GCP integration docs.

## Checked

2026-11-08. Read in full: https://fluxcd.io/flux/guides/mozilla-sops/ (raw source in the fluxcd/website repository).

Removed or corrected: the serviceAccountName, OpenBao/Vault, static cloud credentials and verification paragraphs, which are not on this guide, and the Azure no-secretRef claim (the page states it for AWS and GCP KMS).

Method: documentation only; no commands were run.
