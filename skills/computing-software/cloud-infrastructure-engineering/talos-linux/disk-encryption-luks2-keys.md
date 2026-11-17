---
id: computing-software.cloud-infrastructure-engineering.talos-linux.disk-encryption-luks2-keys
name: disk-encryption-luks2-keys
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [disk-encryption, luks2, volumeconfig, uservolumeconfig, nodeid, kms, locktostate, key-rotation]
level: practitioner
status: docs-checked
description: "Configure LUKS2 encryption for STATE, EPHEMERAL and user volumes in Talos: the four key kinds, slots, lockToState, STATE caveats and the two-step key rotation with reboots."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/storage-and-disk-management/disk-encryption.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Talos encrypts the `STATE` (secrets and certs) and `EPHEMERAL` partitions and user volumes with LUKS2. Encryption is off by default and configured with `VolumeConfig` for system volumes or `UserVolumeConfig` for user volumes. Since Talos v1.12 all encrypted volumes map to `/dev/mapper/luks2-<volume-id>`.

```yaml
apiVersion: v1alpha1
kind: VolumeConfig
name: STATE
encryption:
  provider: luks2
  keys:
    - nodeID: {}
      slot: 0
---
apiVersion: v1alpha1
kind: UserVolumeConfig
name: my-user-volume
encryption:
  provider: luks2
  keys:
    - nodeID: {}
      slot: 0
```

Key kinds, weakest to strongest: `static` (passphrase in config; for STATE it is stored in `META`), `nodeID` (derived from node UUID and partition label, protects against removed or recycled drives only), `kms` (sealed by a network KMS), `tpm` (sealed by the TPM, strong with SecureBoot). Kinds can be combined on one partition. With KMS on STATE, network settings cannot come from the machine config and custom KMS CA certificates cannot be used, since both live on STATE.

STATE encryption config is saved cleartext in `META`, so never use `static` keys for STATE; other volumes may use them once STATE itself is encrypted. Every key needs a `slot`; LUKS2 holds up to 32 keys and Talos syncs the list with the real slots, so keep one unchanged key for management. `lockToState: true` mixes a salt stored on STATE into key derivation, making the volume unreadable if STATE is wiped; recommended for EPHEMERAL and user volumes.

Rotation needs repeated `apply-config` with reboots (re-encryption happens at boot): add the new key in another slot, then remove the old one.

```bash
talosctl apply-config -n <node> -f config.yaml
talosctl -n <node> reboot
```

## Checked

2026-11-04. Key kinds, STATE and KMS caveats, slot and lockToState rules and the rotation sequence confirmed on the Disk Encryption page.

Method: documentation only; no commands were run.
