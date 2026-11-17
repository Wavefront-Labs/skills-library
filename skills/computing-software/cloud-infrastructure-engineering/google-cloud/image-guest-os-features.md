---
id: computing-software.cloud-infrastructure-engineering.google-cloud.image-guest-os-features
name: image-guest-os-features
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, custom-images, guest-os-features, uefi-compatible, gvnic, sev-capable, multi-ip-subnet, image-flags]
level: practitioner
status: docs-checked
description: "Set Compute Engine image guest OS features (UEFI_COMPATIBLE, GVNIC, SEV_CAPABLE, SEV_SNP_CAPABLE, TDX_CAPABLE, IDPF) with the valid gcloud values for each."
sources: ["https://cloud.google.com/compute/docs/images/create-custom#guest-os-features", "https://cloud.google.com/compute/docs/networking/using-gvnic", "https://cloud.google.com/compute/docs/images/os-details"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image guest OS features

Guest OS features are flags on an image (and its disks) declaring what the OS supports. Without
them, VMs from the image cannot use certain hardware or security options.

## Common features
| Feature | Needed for |
|---|---|
| `UEFI_COMPATIBLE` | boot with UEFI firmware and Shielded VM features (vTPM and integrity monitoring on by default) |
| `GVNIC` | gVNIC network interface (higher network bandwidths, up to 50 to 100 Gbps) |
| `SEV_CAPABLE` / `SEV_SNP_CAPABLE` / `TDX_CAPABLE` | Confidential VM variants (also `SEV_LIVE_MIGRATABLE_V2` for SEV live migration) |
| `IDPF` | Intel Infrastructure Data Path Function network interfaces |
| `VIRTIO_SCSI_MULTIQUEUE` | use on Local SSD devices as an alternative to NVMe |
| `MULTI_IP_SUBNET` | interfaces with a netmask other than /32 |
| `WINDOWS` | tag Windows Server custom boot images as Windows images |
The `--guest-os-features` flag of `gcloud compute images create` accepts: BARE_METAL_LINUX_COMPATIBLE, BMSAI_CAPABLE, CCA_CAPABLE, GVNIC, IDPF, MULTI_IP_SUBNET, SEV_CAPABLE, SEV_LIVE_MIGRATABLE, SEV_LIVE_MIGRATABLE_V2, SEV_SNP_CAPABLE, SNP_SVSM_CAPABLE, SUSPEND_SAFE_FPR, TDX_CAPABLE, UEFI_COMPATIBLE, VIRTIO_SCSI_MULTIQUEUE, WINDOWS.

## Set when creating
```bash
gcloud compute images create app-golden-v12 --source-disk=build-disk --source-disk-zone=<Z> \
  --family=app-golden \
  --guest-os-features=UEFI_COMPATIBLE,GVNIC,VIRTIO_SCSI_MULTIQUEUE,SEV_CAPABLE
gcloud compute images describe app-golden-v12 --format="value(guestOsFeatures[].type)"
```
To change features on an existing image, create a new image from it with the flag set
(`--source-image=app-golden-v11 --guest-os-features=...`). After importing an image, verify its features with `describe`.

## Gotchas
- Only tag features the guest OS really supports (for example GVNIC needs the gVNIC driver in the guest); check the kernel driver before tagging.
- A custom image built from a disk keeps only the features you set on the new image, so list them explicitly.

## Verify
- [ ] Creating a Shielded or Confidential VM / `--network-interface=nic-type=GVNIC` from the image succeeds and boots.

## Checked

Checked 2026-10-27 against Create custom images and the gcloud reference for images create. Fixed: SECURE_BOOT is not a valid guest OS feature; the full list of accepted values is now stated, with the documented purpose of UEFI_COMPATIBLE, GVNIC, IDPF, SEV and TDX tags, VIRTIO_SCSI_MULTIQUEUE, MULTI_IP_SUBNET and WINDOWS. Removed unconfirmed Tier_1, series-specific and Packer claims.

Method: documentation only; no commands were run.
