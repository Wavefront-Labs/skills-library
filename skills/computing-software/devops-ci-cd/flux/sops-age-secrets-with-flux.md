---
id: computing-software.devops-ci-cd.flux.sops-age-secrets-with-flux
name: sops-age-secrets-with-flux
category: computing-software
field: devops-ci-cd
product: flux
tags: [sops, age, decryption, secrets, kustomization]
level: sme
status: docs-checked
description: "Encrypt Kubernetes Secrets with SOPS and age, store them in Git, and let kustomize-controller decrypt them in-cluster."
sources:
  - https://fluxcd.io/flux/guides/mozilla-sops/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Flux decrypts SOPS-encrypted Secrets in kustomize-controller just before apply. age is recommended over OpenPGP when possible.

1. Generate a key and give the private half to the cluster. The key name must end in `.agekey`:

```sh
age-keygen -o age.agekey
cat age.agekey | kubectl create secret generic sops-age \
  --namespace=flux-system --from-file=age.agekey=/dev/stdin
```

2. Encrypt only the data fields, leaving `metadata`, `kind` and `apiVersion` in plain text:

```sh
sops --age=<public-key> --encrypt \
  --encrypted-regex '^(data|stringData)$' --in-place basic-auth.yaml
```

3. Point the Kustomization at the key Secret:

```yaml
spec:
  decryption:
    provider: sops
    secretRef:
      name: sops-age
```

or `flux create kustomization ... --decryption-provider=sops --decryption-secret=sops-age`.

A `.sops.yaml` with `creation_rules` (`path_regex`, `encrypted_regex`, and the key, shown on the page as `pgp: <fingerprint>`) in the cluster directory applies recursively and spares contributors from passing flags. The decryption Secret may hold several keys; SOPS tries each. Back the key secret up in a password manager or offline storage. Do not apply SOPS-encrypted Secrets with kubectl; they are for kustomize-controller.

Gotcha: patches that add fields matching `encrypted_regex` can make decryption fail, so keep encrypted fields to Secret `data` and `stringData`.

## Checked

2026-11-08. Read in full: https://fluxcd.io/flux/guides/mozilla-sops/ (raw source in the fluxcd/website repository).

Removed or corrected: the claim that only SOPS is a supported provider and the age creation_rules example (the page shows pgp).

Method: documentation only; no commands were run.
