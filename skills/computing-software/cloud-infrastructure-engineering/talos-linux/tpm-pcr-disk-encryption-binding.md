---
id: computing-software.cloud-infrastructure-engineering.talos-linux.tpm-pcr-disk-encryption-binding
name: tpm-pcr-disk-encryption-binding
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [tpm, pcr, pcr-7, pcr-11, luks2, secureboot, uki, trusted-boot]
level: sme
status: docs-checked
description: "Choose TPM PCR bindings for Talos disk encryption: the default PCR 7, empty list for PCR 11 signed policy only, multi-PCR examples, and how UKI boot phases gate TPM unsealing."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/storage-and-disk-management/disk-encryption.mdx
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/platform-specific-installations/bare-metal-platforms/secureboot.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Talos can seal a LUKS2 key with the TPM (TPM 2.0, strongest with SecureBoot) and bind it to PCR values through `options.pcrs` under the `tpm` key. The default is PCR 7 (SecureBoot state, enrolled PK, KEK, db keys) plus the signed PCR 11 policy covering the UKI and boot phases. Existing installs keep their original binding.

```yaml
apiVersion: v1alpha1
kind: VolumeConfig
name: STATE
encryption:
  provider: luks2
  keys:
    - tpm:
        options:
          pcrs: [0, 7]
      slot: 0
```

An explicit empty list binds only to PCR 11 signed policies and ignores SecureBoot state:

```yaml
tpm:
  options:
    pcrs: []
```

Why configurable: PCR 7 includes the dbx denylist, and tools such as `fwupd` update the SecureBoot database automatically, so literal PCR 7 policies break after firmware or database updates even when policy did not change.

Mechanics: when the UKI is built, expected measurements are combined into a TPM policy signed with the PCR signing key, so unlocking depends on that signature plus the configured PCR states, not exact hashes. `systemd-stub` measures UKI sections (.linux, .osrel, .cmdline, .initrd and others; not .pcrsig) into PCR 11. Talos extends PCR 11 with `enter-initrd`, `leave-initrd`, `enter-machined` and, after the disk is unlocked, `start-the-world`. The key unseals only at `enter-machined`, so workloads cannot unseal it later. Upgrades unlock successfully as long as the new UKI carries a policy signed by the same PCR signing key and the bound PCRs are unchanged.

## Checked

Default and empty PCR lists, multi-PCR example, fwupd and dbx rationale, measurement phases and unseal boundary confirmed on the Disk Encryption and SecureBoot pages.

Method: docs-checked 2026-11-09 against the raw Disk Encryption page (read in full) and the raw SecureBoot page (PCR sections and measurement list read, v1.15 folder).
