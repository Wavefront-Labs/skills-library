---
id: computing-software.cloud-infrastructure-engineering.kubernetes.sops-encrypted-secrets-in-git
name: sops-encrypted-secrets-in-git
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, sops, mozilla-sops, age, kms, pgp, sops-yaml, encryption-rules, ksops, kustomize-plugin, fluxcd, helm-secrets, gitops, encrypted-secrets-in-git, partial-encryption]
level: practitioner
status: docs-checked
description: "Encrypt secrets in place with SOPS: age/KMS key setup, .sops.yaml creation rules, and decrypting via Flux's native SOPS support or the ksops Kustomize plugin."
sources: ["https://github.com/getsops/sops", "https://fluxcd.io/flux/guides/mozilla-sops/", "https://github.com/viaduct-ai/kustomize-sops"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SOPS — encrypt the secret file itself, keep editing it like YAML

**Model, contrasted with Sealed Secrets and ESO:** SOPS encrypts individual **values**
within a structured file (YAML/JSON) in place, leaving keys and structure readable —
`git diff` on a SOPS file shows which key changed even though you can't read the new
value. Unlike Sealed Secrets there's no in-cluster controller holding the decryption
key; unlike ESO there's no live external store being polled — decryption happens at
apply/reconcile time using a key (age or a cloud KMS) the decrypting party holds.

## 1. Key setup
```bash
age-keygen -o key.txt                      # -> public key age1..., private stays local/in a K8s Secret
export SOPS_AGE_KEY_FILE=key.txt
```
`age` keys are the common lightweight choice; `sops` also supports AWS
KMS/GCP KMS/Azure Key Vault/HashiCorp Vault and PGP. KMS-backed keys avoid managing
a private key file at all (IAM/workload identity gates decryption instead), at the
cost of a cloud dependency; age is simpler and works offline, which many teams prefer
for the GitOps controller's own decryption step.

## 2. `.sops.yaml` — creation rules, not per-file flags
```yaml
creation_rules:
  - path_regex: clusters/prod/.*\.sops\.yaml$
    encrypted_regex: "^(data|stringData)$"
    age: age1prod_public_key_...
  - path_regex: clusters/dev/.*\.sops\.yaml$
    age: age1dev_public_key_...
```
- `sops` looks for `.sops.yaml` in the working directory and its parents, so a file at the repo root means
  `sops -e secret.yaml` auto-picks the right key(s) and encryption scope by path —
  no per-invocation flags, and critically, **different environments can use
  different keys**, so a dev key leak doesn't expose prod secrets.
- `encrypted_regex` scopes *which fields* get encrypted — `^(data|stringData)$`
  encrypts only Secret payload fields, leaving `apiVersion`/`kind`/`metadata` (and
  thus `metadata.name`, labels) in plaintext so the file stays diffable and
  Kustomize/Flux can still route it by name without decrypting first.
- Encrypting with multiple recipients (`age: key1,key2` or combined `age`+`kms`)
  means any one of them can decrypt — the standard way to let both a human operator
  and a CI service account decrypt the same file independently.

## 3. Consuming decrypted secrets, two integration points
- **Flux's native SOPS support**: `Kustomization.spec.decryption: {provider: sops,
  secretRef: {name: sops-age}}` where `sops-age` is a cluster Secret holding the
  private age key (or KMS role binding) — kustomize-controller decrypts the
  manifests before applying them.
- **`ksops`** (a Kustomize exec plugin, `viaduct-ai/kustomize-sops`): for plain
  Kustomize or Argo CD (the ksops README documents the Argo CD setup),
  `generators: [ksops-generator.yaml]` invokes `sops -d` as part of `kustomize
  build --enable-alpha-plugins --enable-exec`. Requires the decrypting
  environment (CI runner, or the Argo CD repo-server if run there) to have the
  private key available — for Argo CD the ksops README mounts the key into the
  repo-server and sets `SOPS_AGE_KEY_FILE`.

## Gotchas
- SOPS encrypts **values under the matched keys**, not arbitrary nested structure
  changes — reordering map keys or renaming a field produces a different diff
  footprint than you might expect; this rarely matters in practice but surprises
  people expecting whole-file binary diffs like Sealed Secrets.
- Losing the private key (age key file, or losing KMS access) makes every file
  encrypted against it permanently unrecoverable, the same disaster-recovery
  exposure as Sealed Secrets' controller key — back up age private keys (encrypted
  at rest, e.g. in a password manager or a separate KMS-wrapped blob) before you
  need them.
- `sops updatekeys` re-encrypts a file's data key for a changed `creation_rules`
  recipient list — editing `.sops.yaml` alone does **not** retroactively update
  already-encrypted files; forgetting this step means old files stay encrypted
  against the old recipient set.
- For ksops under Argo CD, verify the key is actually present inside the repo-server pod (the
  ksops README mounts it and sets `SOPS_AGE_KEY_FILE`), not just configured in principle.
- CI needs the private key to run `sops -e`/`-d` for encryption *and* for any
  pre-merge validation step that renders the manifest — treat that CI credential
  with the same care as the secrets it protects.

## Verify
- [ ] `sops -d <file>` succeeds for every environment's intended decryptor
      (correct key per `.sops.yaml` path rule) and fails for a key that shouldn't
      have access.
- [ ] `git diff` on a changed secret shows the field name changed but not the
      plaintext value — confirms `encrypted_regex` scope is correct.
- [ ] After editing `.sops.yaml` recipients, `sops updatekeys` was run on affected
      files (check `sops -d --verbose` or the file's `sops.kms`/`sops.age` metadata
      block for the current recipient list).
- [ ] The decrypting environment (Flux controller / Argo repo-server / CI) actually
      has the private key available at the moment it needs it, tested end to end.

## Checked

Checked 2026-10-27 against the SOPS README and `.sops.yaml` configuration source (getsops/sops, main), the Flux SOPS guide source (fluxcd/website) and the ksops README (viaduct-ai/kustomize-sops).

- SOPS formats and key services (AWS KMS, GCP KMS, Azure Key Vault, age, PGP), `.sops.yaml` discovery from the working directory upwards, `creation_rules` with `path_regex` and `encrypted_regex`, and the `updatekeys` sub-command confirmed in the SOPS source and README.
- Flux `Kustomization.spec.decryption` with `provider: sops` and `secretRef` (for example `sops-age`), `age-keygen -o`, and the `encrypted_regex: ^(data|stringData)$` example confirmed in the Flux guide.
- ksops: `viaduct.ai/v1` `ksops` generator, `kustomize build --enable-alpha-plugins --enable-exec`, Argo CD `kustomize.buildOptions` and repo-server `SOPS_AGE_KEY_FILE` confirmed in its README; the project name is `kustomize-sops` (ksops).
- Removed unconfirmed claims: Flux decrypting purely in memory, the helm-secrets bullet, and the Argo CD repo-server cache behaviour.

Method: documentation only; no commands were run.
