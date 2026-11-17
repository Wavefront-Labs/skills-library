---
id: computing-software.cryptography-implementation.key-management.encrypted-secrets-in-git-with-sops
name: encrypted-secrets-in-git-with-sops
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, sops-encrypted-secrets, sops, sealed-secrets, kubeseal, gitops, age, kms, secret-storage, key-rotation]
level: practitioner
status: draft
description: "Keep secrets in git safely with SOPS (age/KMS recipients, .sops.yaml rules, updatekeys, rotate) and Bitnami Sealed Secrets, including key backup and offboarding."
sources: ["https://github.com/getsops/sops", "https://getsops.io/docs/", "https://github.com/bitnami-labs/sealed-secrets"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Encrypted secrets in git with SOPS and Sealed Secrets

## SOPS
SOPS encrypts values (not keys) in YAML/JSON/ENV/INI files with a data key, wrapped for each recipient (age, PGP,
AWS/GCP/Azure KMS, Vault transit).

`.sops.yaml`:
```yaml
creation_rules:
  - path_regex: environments/prod/.*\.yaml$
    encrypted_regex: '^(data|stringData|password|token)$'
    kms: arn:aws:kms:eu-west-1:111122223333:key/abcd-...
    age: age1qprodops...,age1breakglass...
  - path_regex: environments/dev/.*
    age: age1devteam...
```
Commands:
```
sops -e -i environments/prod/db.yaml        # encrypt in place
sops environments/prod/db.yaml              # edit decrypted in $EDITOR, re-encrypts on save
sops -d environments/prod/db.yaml | kubectl apply -f -
sops updatekeys environments/prod/db.yaml   # apply recipient changes from .sops.yaml
sops rotate -i environments/prod/db.yaml    # new data key (after offboarding)
```
- Offboarding: remove the person's age key from `.sops.yaml`, run `updatekeys`, then `rotate`, **and** rotate the
  underlying secret values; they could read them before.
- Always include a break-glass recipient (KMS or an offline age key).
- The MAC in the file detects tampering; `sops -d` fails if values were edited outside SOPS.

## Sealed Secrets (Kubernetes)
```
kubeseal --fetch-cert > pub-cert.pem
kubectl create secret generic db --from-literal=password=... --dry-run=client -o yaml \
  | kubeseal --cert pub-cert.pem -o yaml > sealed-db.yaml
```
- Only the in-cluster controller can decrypt. The controller renews its sealing key every 30 days and keeps old ones
  for decryption.
- **Back up the controller keys** (`kubectl get secret -n kube-system -l sealedsecrets.bitnami.com/sealed-secrets-key -o yaml`)
  into a secure store, or a cluster rebuild loses every secret.
- Scope (strict / namespace-wide / cluster-wide) is part of the encryption; renaming a secret breaks strict scope.

## Gotchas
- Plaintext must never be committed even once; add pre-commit hooks (gitleaks) to catch slips.
- Diffs of SOPS files show changed values as changed ciphertext; reviewers cannot see what changed without
  decrypting (`sops diff` helpers exist).

## Verify
- [ ] A clone without recipient keys cannot decrypt.
- [ ] Break-glass recipient decrypts in a drill.
- [ ] Sealed Secrets keys backup restores into a new cluster.
