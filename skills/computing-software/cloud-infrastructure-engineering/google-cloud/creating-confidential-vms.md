---
id: computing-software.cloud-infrastructure-engineering.google-cloud.creating-confidential-vms
name: creating-confidential-vms
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, shielded-confidential-vms, confidential-vm-create, amd-sev, intel-tdx, memory-encryption]
level: advanced
status: docs-checked
description: "Create Confidential VMs with AMD SEV, SEV-SNP or Intel TDX: machine series, images, zones, maintenance behaviour, org policy and verifying memory encryption."
sources: ["https://cloud.google.com/confidential-computing/confidential-vm/docs/create-a-confidential-vm-instance", "https://cloud.google.com/confidential-computing/confidential-vm/docs/supported-configurations", "https://cloud.google.com/confidential-computing/confidential-vm/docs/monitoring"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating Confidential VMs

## 1. Pick the technology
| Type | Machine series (typical) | Notes |
|---|---|---|
| `SEV` | N2D, C2D, C3D, C4D | AMD SEV memory encryption; live migration only where the docs say so (MIGRATE policy) |
| `SEV_SNP` | N2D (AMD Milan) | AMD SEV-SNP; Debian 12 has no SEV-SNP attestation support |
| `TDX` | c3-standard-*, c3-standard-*-lssd, c4-standard-* | Intel TDX, up to 192 vCPUs; limited zones; also A3 High (H100) with NVIDIA Confidential Computing |
Check the supported-configurations table for current zones and images.

## 2. Create
```bash
gcloud compute instances create conf-1 --zone=us-central1-a \
  --machine-type=n2d-standard-4 --confidential-compute-type=SEV_SNP \
  --maintenance-policy=TERMINATE --min-cpu-platform="AMD Milan" \
  --image-family=ubuntu-2404-lts-amd64 --image-project=ubuntu-os-cloud \
  --shielded-secure-boot
```
- Set `--maintenance-policy=MIGRATE` only where SEV live migration is supported; for all other machine types and for SEV-SNP and TDX use `TERMINATE` (no live migration).
- Image must support the type (guest OS feature `SEV_CAPABLE`, `SEV_SNP_CAPABLE`, `TDX_CAPABLE`).
- For TDX, omit `--min-cpu-platform` (the create page says to remove it).

## 3. Enforce
Org policy `constraints/compute.restrictNonConfidentialComputing` (a list constraint) restricts non-Confidential
services; configure it as described on the Confidential VM and organization policy pages.

## 4. Verify
Follow the Confidential VM monitoring page: SEV launch attestation reports appear in Cloud Logging
under the `sevLaunchAttestationReportEvent` key of `jsonPayload`. Confirm memory encryption inside the guest with the
commands in the Confidential VM documentation for your image.

## Gotchas
- Not every GPU, Local SSD or Windows image combination is supported; check the supported-configurations page, including its per-technology limitations (for example no kdump on SEV-SNP and TDX, TDX not on sole-tenant node groups).
- Confidential VM protects memory in use; it doesn't replace disk CMEK or IAM.

## Verify
- [ ] `gcloud compute instances describe conf-1 --zone=<Z> --format='value(confidentialInstanceConfig)'` shows the type; dmesg confirms encryption active.

## Checked

Checked 2026-10-27 against Create a Confidential VM instance, Supported configurations, the Confidential VM monitoring page, the organization policy constraints list and the gcloud reference for instances create. Fixed the machine-series table (SEV on N2D, C2D, C3D and C4D; SEV-SNP on N2D with AMD Milan; TDX on c3-standard-*, c3-standard-*-lssd and c4-standard-*) and the maintenance-policy rule (MIGRATE only where SEV live migration is supported, TERMINATE otherwise). Confirmed --confidential-compute-type, the TDX rule to omit --min-cpu-platform, the image feature names and sevLaunchAttestationReportEvent. Removed unconfirmed dmesg output, the performance figure and the fixed-at-creation claim.

Method: documentation only; no commands were run.
