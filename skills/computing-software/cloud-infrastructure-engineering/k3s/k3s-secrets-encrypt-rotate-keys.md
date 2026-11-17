---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-secrets-encrypt-rotate-keys
name: k3s-secrets-encrypt-rotate-keys
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, secrets-encrypt, rotate-keys, reencrypt-finished]
level: advanced
status: docs-checked
description: "Rotate secrets encryption keys with k3s secrets-encrypt rotate-keys on single-server and HA clusters."
sources:
  - https://docs.k3s.io/cli/secrets-encrypt
  - https://docs.k3s.io/security/secrets-encryption
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Warning: improper rotation can leave the cluster permanently corrupted.

Single server (started with --secrets-encryption):

```
k3s secrets-encrypt rotate-keys
k3s secrets-encrypt status
```

Wait until status shows `Encryption Status: Enabled` and `Current Rotation Stage: reencrypt_finished`. K3s reencrypts about 5 secrets per second, so large clusters can take minutes; follow progress in the server logs.

HA (all servers started with --secrets-encryption), S1 being the node you run commands on:

1. `k3s secrets-encrypt rotate-keys` on S1.
2. Wait for reencrypt_finished.
3. Restart K3s on S1 with the same arguments (`systemctl restart k3s` or `rc-service k3s restart`).
4. Once S1 is up, restart K3s on S2 and S3.

Legacy procedure (the docs recommend rotate-keys on v1.30+ instead): `prepare`, restart, `rotate`, restart, `reencrypt`, restart; on HA run each step on S1 and restart S2 and S3 after S1 is up.

To migrate between providers (aescbc to secretbox), set `secrets-encryption-provider` and then rotate the keys.

## Checked

2026-11-08. Read the full k3s secrets-encrypt CLI page (docs/cli/secrets-encrypt.md) and the full Secrets Encryption page (docs/security/secrets-encryption.md) in the k3s-io/docs repo. Confirmed: the corruption warning, single-server and HA rotate-keys steps, reencrypt_finished status, about 5 secrets per second, restart commands, the legacy prepare/rotate/reencrypt procedure and the v1.30+ recommendation, and the aescbc to secretbox migration. Removed the closing sentence about running status on S1 and other servers (not on the page).

Method: documentation only; no commands were run.
