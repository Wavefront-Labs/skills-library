---
id: computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-sealing-key-renewal
name: sealed-secrets-sealing-key-renewal
category: computing-software
field: devops-ci-cd
product: sealed-secrets
tags: [sealed-secrets, key-renewal, key-renew-period, key-order-priority, sealing-key, rotation]
level: advanced
status: docs-checked
description: "How the Sealed Secrets controller renews its sealing key every 30 days, tuning --key-renew-period and --key-order-priority, and why old keys are kept."
sources: ["https://github.com/bitnami/sealed-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed secrets sealing key renewal

Sealing keys are renewed automatically every 30 days: a new key is created and appended to the set of active keys. The newest key seals new secrets and supplies the certificate returned by `kubeseal --fetch-cert`. Older keys remain active so existing SealedSecrets still unseal; they are not deleted. The README stresses that this is renewal, not rotation: the feature was historically named key rotation, which causes the misunderstanding that old keys are bad and should be removed.

Tune the period with the controller flag `--key-renew-period=<value>`, a Go duration such as `720h30m` (no `d` unit exists in the Go standard library). Edit the Deployment:

```bash
kubectl edit deployment/sealed-secrets-controller --namespace=kube-system
```

A value of `0` disables automatic renewal; the README warns that new users often reach for this before understanding the design.

At startup the controller builds a key registry. `--key-order-priority` decides which key counts as most recent:
- `CertNotBefore` (default): ordered by the certificate NotBefore attribute.
- `SecretCreationTimestamp`: ordered by the key Secret's creation timestamp.

This affects which public key encrypts new secrets and which certificate `--fetch-cert` returns.

Sealing keys are more like a GPG key for reading mail than an access password, so deleting one on suspicion of compromise destroys your ability to read existing data without undoing any leak.

## Checked
Date: 2026-11-04. Documentation: bitnami-labs/sealed-secrets README (raw markdown, main branch), sections Sealing key renewal, Key registry init priority order, Common misconceptions.
Confirmed: 30-day renewal, newest key seals and feeds `--fetch-cert`, `--key-renew-period` as Go duration (`720h30m`), `0` disables, `--key-order-priority` values, old keys kept.
Removed: nothing.
Method: documentation only; no commands were run.
