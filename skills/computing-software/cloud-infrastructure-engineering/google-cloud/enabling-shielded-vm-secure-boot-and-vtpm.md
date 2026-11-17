---
id: computing-software.cloud-infrastructure-engineering.google-cloud.enabling-shielded-vm-secure-boot-and-vtpm
name: enabling-shielded-vm-secure-boot-and-vtpm
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, shielded-confidential-vms, shielded-vm-enable, enable-vtpm-secure-boot, org-policy, uefi]
level: practitioner
status: docs-checked
description: "Turn on Shielded VM Secure Boot, vTPM and integrity monitoring for new and existing instances, require it with org policy, and handle unsigned drivers that break Secure Boot."
sources: ["https://cloud.google.com/compute/shielded-vm/docs/modifying-shielded-vm", "https://cloud.google.com/compute/shielded-vm/docs/shielded-vm", "https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enabling Shielded VM Secure Boot and vTPM

Shielded VM needs a Shielded VM-capable (UEFI-compatible) image. vTPM and integrity
monitoring are on by default (integrity monitoring relies on the vTPM, so disabling the vTPM disables it); **Secure Boot is off by default**.

## 1. New instances
```bash
gcloud compute instances create web-1 --zone=<Z> --image-family=debian-12 --image-project=debian-cloud \
  --shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring
```
Put the same flags in instance templates.

## 2. Existing instances (must be stopped)
```bash
gcloud compute instances stop web-1 --zone=<Z>
gcloud compute instances update web-1 --zone=<Z> --shielded-secure-boot
gcloud compute instances start web-1 --zone=<Z>
gcloud compute instances describe web-1 --zone=<Z> --format='value(shieldedInstanceConfig)'
```

## 3. Enforce
Org policy `constraints/compute.requireShieldedVm` (boolean): new VMs must use Shielded disk images with
Secure Boot, vTPM and Integrity Monitoring enabled (Secure Boot can be disabled after creation; running VMs are unaffected). Apply at org/folder:
```bash
gcloud resource-manager org-policies enable-enforce compute.requireShieldedVm --organization=<ORG>
```
`constraints/compute.requireOsLogin` is a separate boolean constraint often bundled in a baseline.

## Gotchas
- Many Linux images refuse to load unsigned out-of-tree kernel modules when Secure Boot is on; this most often affects GPU drivers and some security tools. Use signed drivers or add keys to a custom image with `gcloud compute images create --signature-database-file`.
- Custom images must carry the guest OS feature `UEFI_COMPATIBLE` to be Shielded VM-capable.
- On Windows with BitLocker active, changing Secure Boot or the vTPM changes the boot integrity baseline and the next boot asks for the 48-digit recovery key; retrieve it or suspend BitLocker first. Test on a representative VM before changing options.

## Verify
- [ ] `describe` shows `enableSecureBoot: true, enableVtpm: true, enableIntegrityMonitoring: true`.

## Checked

Checked 2026-10-27 against Shielded VM, Modify Shielded VM options, the organization policy constraints list, the gcloud reference for instances create and images create, and the Compute Engine v1 API discovery document. Confirmed: Secure Boot off by default, vTPM and integrity monitoring on by default, the --shielded-* flags, constraints/compute.requireShieldedVm semantics, UEFI_COMPATIBLE and --signature-database-file on images create, the unsigned-module behaviour and the BitLocker recovery-key warning. Removed the unconfirmed mokutil output and the claim that all public images are UEFI.

Method: documentation only; no commands were run.
