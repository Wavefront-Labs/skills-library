---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-secrets-encrypt-status
name: k3s-secrets-encrypt-status
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, secrets-encrypt-status, encryption-hashes, rotation-stages]
level: practitioner
status: docs-checked
description: "Read the output of k3s secrets-encrypt status: stages, server hashes and the active key table."
sources:
  - https://docs.k3s.io/cli/secrets-encrypt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Run `k3s secrets-encrypt status` on a node. Example output:

```
Encryption Status: Enabled
Current Rotation Stage: start
Server Encryption Hashes: All hashes match
Active  Key Type  Name
------  --------  ----
 *      AES-CBC   aescbckey
```

Fields:

- Encryption Status: whether secrets encryption is enabled or disabled on the node.
- Current Rotation Stage: one of start, prepare, rotate, reencrypt_request, reencrypt_active, reencrypt_finished.
- Server Encryption Hashes: for HA, whether every server has the same local encryption files. After rotating keys but before restarting servers it can read `hash does not match between node-1 and node-2`; restarting the servers syncs their configuration, so use it to decide whether a restart is needed before the next stage.
- Key table: Active marks (with *) the key used to encrypt new secrets; Key Type is AES-CBC or secretbox; Name is the key name, for example aescbckey-2021-12-10T22:54:38Z after a rotation alongside the older aescbckey.

On a cluster started without `--secrets-encryption`, status reports `Disabled, no configuration file found`; see the enable skill.

## Checked

2026-11-08. Read the full k3s secrets-encrypt CLI page (docs/cli/secrets-encrypt.md in the k3s-io/docs repo). Confirmed: the status example output, the six rotation stages, server hash semantics with the node-1 and node-2 example, the key table fields, AES-CBC and secretbox key types, and the Disabled, no configuration file found output. Reworded the last sentence to match the page.

Method: documentation only; no commands were run.
