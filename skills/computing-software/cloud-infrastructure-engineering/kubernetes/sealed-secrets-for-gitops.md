---
id: computing-software.cloud-infrastructure-engineering.kubernetes.sealed-secrets-for-gitops
name: sealed-secrets-for-gitops
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, sealed-secrets, bitnami-sealed-secrets, kubeseal, gitops, secret-management, asymmetric-encryption, sealing-scope, key-rotation, disaster-recovery, encrypted-secrets-in-git]
level: practitioner
status: docs-checked
description: "Store secrets in a GitOps repo with Bitnami Sealed Secrets: kubeseal encryption, the controller's keypair rotation, sealing scope, and the mandatory backup before you need it."
sources: ["https://github.com/bitnami-labs/sealed-secrets#readme", "https://fluxcd.io/flux/guides/sealed-secrets/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sealed Secrets — encrypt once, decrypt only in-cluster

**Model:** `kubeseal` encrypts a `Secret` client-side with the **controller's public
key** (fetchable, not sensitive) into a `SealedSecret` CRD that's safe to commit to
git. Only the controller, holding the private key inside the cluster, can decrypt it
back into a real `Secret`. This is the simplest of the three GitOps-secrets patterns
(compare `external-secrets-operator-patterns`, `sops-encrypted-secrets-in-git`) —
no external secret store, pure in-cluster asymmetric crypto.

## 1. Basic flow
```bash
kubectl create secret generic db-creds --dry-run=client -o yaml \
  --from-literal=password=<REAL_PASSWORD> > secret.yaml
kubeseal --format yaml --cert pub-cert.pem < secret.yaml > sealed-secret.yaml
rm secret.yaml                      # never commit the plaintext intermediate
kubectl apply -f sealed-secret.yaml # or let Argo CD/Flux apply it from git
```
`pub-cert.pem` comes from `kubeseal --fetch-cert` against a live cluster, or is
distributed out-of-band — fetching it live means your sealing step needs network
access to the target cluster's controller, a common CI setup requirement people
miss on first try.

## 2. Sealing scope — the setting that decides reusability
`kubeseal` defaults to **strict** scope: the `SealedSecret` is bound to the exact
`name` + `namespace` it was sealed for; changing either on the resulting resource
makes it fail to decrypt. Two looser scopes exist, selected with `kubeseal --scope` (stored as annotations on the SealedSecret):
- `namespace-wide` (`sealedsecrets.bitnami.com/namespace-wide: "true"`): decrypts
  into any Secret name within the same namespace — lets you rename the Secret
  without resealing.
- `cluster-wide` (`sealedsecrets.bitnami.com/cluster-wide: "true"`): decrypts
  anywhere in the cluster — convenient for copying one sealed value across many
  namespaces, but it also means anyone who can read that `SealedSecret` YAML and
  apply it into a namespace they control gets the plaintext back; scope this only
  to values that are genuinely fine cluster-wide (rarely true for real secrets).
Pick strict unless you have a specific reason not to — it's the scope that matches
"this secret belongs to this one Deployment" and limits what a compromised sealed
value can be repurposed into.

## 3. Key rotation and disaster recovery
- The controller auto-generates a new encryption keypair on a schedule (default 30
  days, configurable) but **keeps old private keys** so previously sealed secrets
  still decrypt — rotation here means "stop using the old key for new seals," not
  "invalidate old seals."
- **The private key lives only as a Secret in the cluster.** If the cluster is
  rebuilt without restoring that Secret, every `SealedSecret` ever committed becomes
  permanently undecryptable — there is no recovery path, not even from Bitnami.
  Back up the controller's keypair Secret (`kubectl get secret -n kube-system -l
  sealedsecrets.bitnami.com/sealed-secrets-key -o yaml`) to a separate secure store
  *before* you need it; this is the single most important operational step for this
  tool and the most commonly skipped one.
- To renew the sealing key early after a suspected compromise, pass the current time to the
  controller with `--key-cutoff-time` (or `SEALED_SECRETS_KEY_CUTOFF_TIME`, RFC1123 format, for example
  from `date -R`) before sealing newly rotated secrets. Renewal alone does not revoke old sealed
  values: also rotate the real secret values, and re-encrypt files with `kubeseal --re-encrypt`.
  Recreate your key backup after every renewal, or it cannot decrypt secrets sealed with the new key.

## Gotchas
- A `SealedSecret`'s encrypted blob is **per-field**, not whole-object — use
  `kubeseal --merge-into <file>` to add or update keys in an existing sealed secret; keys can be
  renamed without losing decryptability.
- Restoring a cluster from a backup that includes the `SealedSecret` CRDs but not the
  controller's key Secret leaves every secret unrecoverable — the backup/DR plan
  must treat the key Secret with at least the same rigor as the secrets it protects.
- CI pipelines that seal secrets need `kubeseal --cert` pointed at the *target*
  cluster's public cert; sealing against the wrong cluster's cert produces a
  `SealedSecret` that silently fails to decrypt only when applied to the intended
  cluster — a classic cross-environment mixup.
- Unlike `external-secrets-operator-patterns`, there is no live sync with an
  external authority (Vault, cloud secret manager) — rotating the underlying
  credential (e.g. a rotated DB password) still requires a human/CI step to reseal
  and recommit, not just a refresh interval.

## Verify
- [ ] The controller's keypair Secret is backed up somewhere outside the cluster,
      and that backup has actually been tested by restoring it into a scratch
      cluster and decrypting an old `SealedSecret` against it.
- [ ] Sealing scope matches intent — a strict-scoped secret fails to apply under a
      renamed Secret/namespace (confirms it's not accidentally cluster-wide).
- [ ] `kubeseal --fetch-cert` in CI is pointed at the correct target cluster per
      environment, not a single shared cert reused across dev/staging/prod.
- [ ] No plaintext intermediate `secret.yaml` file was ever committed (check git
      history, not just the current tree).

## Checked

Checked 2026-10-27 against the Sealed Secrets README (bitnami-labs/sealed-secrets, main).

- Scopes `strict` (default), `namespace-wide`, `cluster-wide`, the `--scope` flag and the `sealedsecrets.bitnami.com/namespace-wide` and `cluster-wide` annotations confirmed.
- Sealing keys renew every 30 days by default (`--key-renew-period`), old keys are kept, keys are Secrets labelled `sealedsecrets.bitnami.com/sealed-secrets-key`, the backup command, the loss-of-private-key warning ("no backdoors"), and `--fetch-cert` / `--cert` confirmed.
- Corrected: early renewal uses `--key-cutoff-time` (not deleting the key Secret), `kubeseal --merge-into` exists for incremental updates, and `kubeseal --re-encrypt` re-encrypts with the latest key.

Method: documentation only; no commands were run.
