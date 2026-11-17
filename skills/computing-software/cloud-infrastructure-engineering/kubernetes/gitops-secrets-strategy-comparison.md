---
id: computing-software.cloud-infrastructure-engineering.kubernetes.gitops-secrets-strategy-comparison
name: gitops-secrets-strategy-comparison
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, gitops, secrets-management, sealed-secrets, external-secrets-operator, sops, vault, vault-secrets-operator, decision-guide, trust-model, secret-rotation, comparison]
level: practitioner
status: docs-checked
description: "Pick between Sealed Secrets, External Secrets Operator, SOPS and Vault Agent/VSO for GitOps secrets: trust model, rotation story, ops burden, and failure modes compared."
sources: ["https://github.com/bitnami-labs/sealed-secrets/blob/main/README.md", "https://github.com/external-secrets/external-secrets/blob/main/docs/introduction/overview.md", "https://github.com/external-secrets/external-secrets/blob/main/docs/api/externalsecret.md", "https://github.com/getsops/sops", "https://github.com/fluxcd/kustomize-controller/blob/main/docs/spec/v1/kustomizations.md", "https://developer.hashicorp.com/vault/docs/deploy/kubernetes/vso/api-reference"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a GitOps secrets strategy — the decision, not the how-to

This is a decision guide across four skills, each of which already covers its own
mechanics in depth — `sealed-secrets-for-gitops`, `external-secrets-operator-patterns`,
`sops-encrypted-secrets-in-git`, and
`computing-software.devops-ci-cd.secrets-management.vault-dynamic-secrets-and-leases`.
Read this first to pick one (or two, deliberately), then go implement with the
matching skill.

## The four real decision axes
1. **Where does the secret's source of truth live?** Sealed Secrets and SOPS:
   the secret's *encrypted form* lives in git; nothing else holds the plaintext
   except whoever/whatever has the decryption key. ESO and Vault-based approaches:
   the plaintext lives in an external store (Vault, cloud secret manager); git holds
   only a pointer. This is the single biggest fork — "git is the vault" vs. "git
   points at the vault."
2. **How does rotation propagate?** Sealed Secrets/SOPS: rotating the underlying
   credential requires re-sealing/re-encrypting and recommitting — a human or CI
   step, every time. ESO/Vault: rotation in the backend store propagates on the
   next `refreshInterval` (an `ExternalSecret` with `refreshInterval: 0` is created once and never
   updated) or lease renewal with **no git commit at all** — faster, but
   means the live cluster state can now differ from "what git currently says" at
   any given instant, which is a small philosophical tension with strict GitOps
   (mitigated by git holding the *pointer*, which hasn't changed, even though the
   *value* behind it has).
3. **What's the blast radius of a leaked key?** Sealed Secrets sealing key leak: every
   SealedSecret encrypted to that key can be decrypted by whoever holds it, including copies in
   Git history; the Sealed Secrets README says a compromised sealing key requires its "Early key
   renewal" procedure before rotating your actual secret values, and that key renewal is not a
   substitute for rotating the secrets themselves. SOPS key leak: every file encrypted against that
   recipient, decryptable. ESO/Vault credential leak: whatever that workload identity's
   policy allows reading from the external store right now — scoped by IAM/Vault
   policy, often narrower and revocable without touching git history at all. This
   favors ESO/Vault for anything high-value, and favors Sealed Secrets/SOPS only
   when you specifically want to avoid depending on an external store.
4. **Operational burden to stand up.** Sealed Secrets: one controller, no external
   dependency, simplest to bootstrap from zero. SOPS: no controller of its own, just a
   key and a CLI step in CI (it encrypts with age, PGP and cloud KMS keys), at the cost of
   decryption integration that varies by GitOps tool; Flux's Kustomization has native SOPS
   decryption via `.spec.decryption`, and other tools need their own plugin. ESO/Vault: requires running and operating a real secret store (or
   paying for a managed one) plus workload-identity federation — more setup, but
   that store usually already exists in orgs doing this at scale for non-K8s
   secrets too, making ESO additive rather than new infrastructure.

## Which axis to decide first
Decide axis 1 first (git-is-the-vault vs. git-points-at-the-vault) — it determines
which two of the four tools are even in play. Then decide axis 3 (blast radius
tolerance) to pick within that pair. Axes 2 and 4 are usually deciding factors only
when 1 and 3 leave a genuine tie.

## Common combinations in practice
- **Small team, no existing secret store, want simplicity**: Sealed Secrets alone.
  Lowest new infrastructure, acceptable because the team can commit to the
  disaster-recovery backup discipline it requires.
- **Org already running Vault/cloud secret manager for everything else**: ESO,
  so Kubernetes consumes the same store non-K8s services already use — one
  rotation story, one audit trail, instead of a second secrets system just for the
  cluster.
- **Multi-cloud/offline-friendly, no desire to run a store**: SOPS with age keys —
  works without any cloud dependency and is natively supported by Flux's Kustomization
  decryption; other GitOps tools need a SOPS plugin.
- **High-value, short-lived, per-workload credentials (DB creds, cloud API keys)
  that should never sit static anywhere**: Vault dynamic secrets (for example through the Vault
  Secrets Operator's `VaultDynamicSecret` resource) rather than any of the above three — those three all materialize a long-lived credential
  into a Secret object; dynamic secrets avoid a long-lived credential existing at
  all. See `vault-dynamic-secrets-and-leases` for the mechanics.
- **Mixed fleet**: nothing stops combining — e.g. SOPS for low-churn platform
  config secrets, ESO for app credentials rotated by an external system, Vault
  dynamic secrets for database access. Pick per secret class, not one tool for
  the whole org by default.

## Acceptance criteria for "this choice is working"
- A rotated credential reaches the cluster within the agreed SLA for that secret
  class, through the mechanism the chosen tool actually provides (recommit vs.
  auto-refresh vs. lease renewal) — not assumed, tested.
- A leaked key/credential's blast radius matches what was accepted when the tool
  was chosen — if it doesn't, the choice (not just the incident response) needs
  revisiting.
- Disaster recovery for the chosen tool's own key material (Sealed Secrets
  controller key, SOPS private key, Vault unseal/root material) is backed up and
  has been test-restored at least once.

## Failure modes this guide exists to prevent
- Picking Sealed Secrets or SOPS by default without ever testing the key-loss DR
  path, discovering the gap during an actual cluster rebuild.
- Running ESO against a `ClusterSecretStore` with store-wide credentials far
  broader than any single namespace needs, because "it worked in the tutorial."
- Treating a long-lived database password synced by ESO as equivalent to a Vault dynamic
  secret — both end up as Kubernetes Secrets, but the credential lifetime and revocation story
  differ; confirm which one you actually have per secret class, not just per tool.

## Verify
- [ ] Each secret class in the repo has one deliberately chosen strategy, not an
      accidental mix from different people picking differently over time.
- [ ] The DR path for whichever tool(s) are chosen has been tested, not just
      documented.
- [ ] Rotation SLA per secret class is known and matches what the chosen tool can
      actually deliver.

## Checked

Checked 2026-10-27. Documentation checked: Sealed Secrets README (bitnami-labs, main), External Secrets Operator docs (overview, ExternalSecret API; main), SOPS README (getsops, main), Flux kustomize-controller Kustomization spec (main), Vault Secrets Operator API reference page (developer.hashicorp.com). Confirmed: Sealed Secrets sealing-key renewal every 30 days by default and the compromise procedure; ESO `refreshInterval` semantics and `ClusterSecretStore` being cluster-wide; SOPS encrypts with age, PGP and cloud KMS; Flux `.spec.decryption` supports SOPS; `VaultDynamicSecret` exists in VSO. Fixed: "forever" wording for Sealed Secrets key leaks, the `ExternalSecret` CRD shape claim for Vault dynamic secrets, and the unverified ksops/helm-secrets/Vault Agent references. The comparison itself is design guidance; the tool facts listed above were checked.

Method: documentation only; no commands were run.
