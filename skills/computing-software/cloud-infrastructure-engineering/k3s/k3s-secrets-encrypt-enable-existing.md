---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-secrets-encrypt-enable-existing
name: k3s-secrets-encrypt-enable-existing
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, secrets-encrypt-enable, existing-cluster, rotation-stage]
level: advanced
status: docs-checked
description: "Enable secrets encryption on a cluster that started without --secrets-encryption using k3s secrets-encrypt enable."
sources:
  - https://docs.k3s.io/cli/secrets-encrypt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Version gate: available as of the March 2026 releases v1.33.10+k3s1, v1.34.6+k3s1 and v1.35.3+k3s1.

Single server:

1. Check: `k3s secrets-encrypt status` reports `Encryption Status: Disabled, no configuration file found`.
2. `k3s secrets-encrypt enable`.
3. Add --secrets-encryption to the server args or config, then restart the server.
4. Status should show Disabled with `Current Rotation Stage: start` and `Server Encryption Hashes: All hashes match`.
5. `k3s secrets-encrypt rotate-keys` to enable encryption for new secrets.
6. Restart the server with the same arguments.
7. Verify `Encryption Status: Enabled` and `Current Rotation Stage: reencrypt_finished`.

HA (S1, S2, S3): run `enable` on S1; restart all servers with --secrets-encryption; confirm stage start and matching hashes; run `rotate-keys` on S1; restart all servers with the same arguments; verify Enabled, reencrypt_finished and matching hashes.

Disable and re-enable later (run on one chosen server, restart it, then restart the others once it is up):

```
k3s secrets-encrypt disable
k3s secrets-encrypt reencrypt --force --skip
k3s secrets-encrypt enable
k3s secrets-encrypt reencrypt --force --skip
```

Restart K3s with the same arguments between steps.

## Checked

2026-11-03: read docs.k3s.io cli/secrets-encrypt. Confirmed: the March 2026 release gate and the single-server, HA and disable/re-enable command sequences with expected status output.

Method: documentation only; no commands were run.
