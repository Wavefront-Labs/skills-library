---
id: computing-software.systems-network-administration.virtualisation.esxi-uefi-secure-boot-and-tpm-attestation
name: esxi-uefi-secure-boot-and-tpm-attestation
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-secure-boot, tpm-host-attestation, tpm-2-0, secure-boot, vmware, esxi, vsphere]
level: advanced
status: draft
description: "Turn on UEFI Secure Boot and TPM 2.0 for ESXi hosts, check attestation status in vCenter, fix 'host TPM attestation alarm', and enforce secure boot settings."
sources:
  - https://knowledge.broadcom.com/external/article/312162
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UEFI Secure Boot and TPM attestation for ESXi

**Goal:** hosts boot only signed code, and vCenter can attest that through the TPM.

## Pre-check before enabling Secure Boot
Unsigned VIBs (community drivers) stop a secure-booted host from booting. Run on the host:
```sh
/usr/lib/vmware/secureboot/bin/secureBoot.py -c   # "Secure boot can be enabled" or lists blockers
/usr/lib/vmware/secureboot/bin/secureBoot.py -s   # current state
esxcli software acceptance get                    # must be PartnerSupported or higher
```
Then enable Secure Boot in the server firmware (UEFI mode required).

## TPM 2.0
- Fit a TPM 2.0 module, firmware setting: TPM on, **SHA-256** PCR bank, TIS/FIFO interface (not CRB on some older builds).
- In vCenter, host -> Monitor -> Security shows attestation status: *Passed*, *Failed*, or *N/A* (no TPM).
- Alarm "Host TPM attestation alarm" usually means the TPM was cleared, firmware changed hashing, or the host was not rebooted after enabling the TPM. Fix: set SHA-256, reboot, then disconnect/reconnect the host.

## Enforce
- `esxcli system settings encryption set --require-secure-boot=T` (with `--mode=TPM`) makes ESXi refuse to unseal the configuration if Secure Boot is turned off.
- Back up the recovery key: `esxcli system settings encryption recovery list`. Without it, a motherboard replacement means reinstalling.
- vSphere Trust Authority (vTA) builds on TPM attestation for key-provider gating.

## Gotchas
- Enabling Secure Boot on an upgraded host with old VIBs: run the check script first.
- Replacing the TPM or motherboard: you need the recovery key to boot with TPM-sealed config.

## Verify
`secureBoot.py -s` returns Enabled, vCenter Security tab shows *Passed* for every host, recovery keys stored in the password vault.
