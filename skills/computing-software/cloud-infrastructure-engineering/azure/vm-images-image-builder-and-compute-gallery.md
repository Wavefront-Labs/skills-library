---
id: computing-software.cloud-infrastructure-engineering.azure.vm-images-image-builder-and-compute-gallery
name: vm-images-image-builder-and-compute-gallery
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vm-images, image-builder, vm-image-builder, aib, custom-images, image-definitions, image-versions, generalized-image, specialized-image, azure-compute-gallery, shared-image-gallery, sysprep, waagent-deprovision, packer, image-replication, community-gallery, direct-shared-gallery, image-lifecycle, golden-image, trusted-launch-images]
level: practitioner
status: docs-checked
description: "Build and ship golden VM images: Image Builder templates distributing to Compute Gallery, generalized vs specialized, versioning, replication, end-of-life and logs."
sources: ["https://learn.microsoft.com/en-us/azure/virtual-machines/image-builder-overview", "https://learn.microsoft.com/en-us/azure/virtual-machines/shared-image-galleries", "https://learn.microsoft.com/en-us/azure/virtual-machines/image-version", "https://learn.microsoft.com/en-us/azure/virtual-machines/linux/image-builder-troubleshoot", "https://learn.microsoft.com/en-us/cli/azure/sig/image-definition", "https://learn.microsoft.com/en-us/cli/azure/sig/image-version", "https://learn.microsoft.com/en-us/cli/azure/image/builder"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM images — golden images built by pipeline, versioned in a gallery

**Goal:** every VM boots from an image built from code last week, replicated where it's
needed, and old versions age out automatically.

## 1. Compute Gallery structure
Gallery → **image definition** (publisher/offer/sku, OS, `--os-state Generalized|Specialized`,
`--hyper-v-generation V2`, `--features SecurityType=TrustedLaunchSupported`, architecture) →
**image versions** (`1.2.3`, replicated to N regions with replica counts, `--end-of-life-date`,
`--exclude-from-latest`).
```bash
az sig create -g rg-images -r gal_platform
az sig image-definition create -g rg-images -r gal_platform -i ubuntu-2404-hardened \
  --publisher platform --offer ubuntu --sku 2404-hardened --os-type Linux --os-state Generalized \
  --hyper-v-generation V2 --features SecurityType=TrustedLaunchSupported
az vm create ... --image /subscriptions/<s>/resourceGroups/rg-images/providers/Microsoft.Compute/galleries/gal_platform/images/ubuntu-2404-hardened   # resolves "latest"
```
Share: RBAC on the gallery, **direct shared gallery**, or **community gallery** (public); the
sharing page lists which options each gallery type supports. Replication is per version: set
`--target-regions uksouth=2 ukwest=1` (region=replica count) to choose the replica count per region.

## 2. Generalized vs specialized
- **Generalized**: deprovision inside the VM (`waagent -deprovision` on Linux, Sysprep on
  Windows), deallocate, `az vm generalize`, then capture. New VMs get fresh host identity
  and credentials. The normal golden image.
- **Specialized**: a straight disk copy of a configured VM; keeps its machine identity and
  accounts. For cloning a configured box or images you can't sysprep.
- Image Builder adds a hidden deprovision step itself.
- A deprovisioned source VM is not reusable; capture, then delete it.

## 3. Image Builder (AIB)
A managed service built on HashiCorp Packer: a template (ARM/Bicep) with a source
(marketplace, gallery or managed image), customizer steps (for example Shell, PowerShell,
File, `WindowsRestart`, `WindowsUpdate`) and distribute targets (Compute Gallery, managed
image, VHD). The distributed image keeps the generation (Gen1/Gen2) of the source; with
`TrustedLaunchSupported` both source and distribute must be TrustedLaunchSupported.
```bash
az identity create -n id-aib -g rg-images   # user-assigned identity with permission to read and write images
az image builder create -g rg-images -n ubuntu-hardened --image-source Canonical:ubuntu-24_04-lts:server:latest \
  --identity id-aib --scripts https://.../harden.sh --shared-image-destinations ubuntu-2404-hardened=uksouth,ukwest \
  --build-timeout 120 --vm-size Standard_D4ds_v5 [--vnet vnet-build --subnet snet-aib]
az image builder run -g rg-images -n ubuntu-hardened
az image builder show-runs -g rg-images -n ubuntu-hardened
```
- Builds run in a staging resource group named `IT_<DestinationResourceGroup>_<TemplateName>_<GUID>`;
  you can supply your own with `stagingResourceGroup`. Logs (`customization.log`) sit in the
  `packerlogs` container of the staging storage account (troubleshooting page).
- `--vnet` builds into your own network when scripts need private resources.
- `az image builder trigger` manages triggers; a pipeline cron also works.
- Distribution to other regions can incur network egress charges.

## 4. Packer
Image Builder is built on Packer; running Packer yourself gives local control and non-Azure
targets. Choose AIB for a managed service without a build host; Packer when the same
pipeline also builds images for other clouds.

## 5. Lifecycle
- `az sig image-version update` with `--end-of-life-date` and `--exclude-from-latest true`
  on broken builds; delete versions no VM references.
- Policy: restrict VM creation to images from your gallery with Azure Policy.
- Rebuild on a regular cadence from a marketplace base plus updates.

## Gotchas
- `latest` is per-definition and resolves at create; pin a version where instances must match.
- Image definition properties such as the hyper-v generation and features cannot be assumed
  changeable; create a new definition if they were wrong.
- Check replication status of a version (`az sig image-version show --expand ReplicationStatus`)
  before creating VMs in a new region.

## Verify
- [ ] `az sig image-version show --expand ReplicationStatus` shows every target region complete.
- [ ] A VM from `latest` boots; identity is fresh (generalized) or preserved (specialized) as intended.
- [ ] Image Builder `show-runs` shows `runState` succeeded; `customization.log` has no errors.
- [ ] Policy audit shows no VMs from non-gallery images in production.

## Checked
2026-10-28. Confirmed against the Image Builder overview, Compute Gallery sharing, image-version
and troubleshooting pages and the `az sig` / `az image builder` CLI pages: `--features
SecurityType=TrustedLaunchSupported`, `--target-regions region=count`, `--exclude-from-latest`,
staging group `IT_` naming and `stagingResourceGroup`, `packerlogs` and `customization.log`,
`runState`, built-on-Packer, generation carry-over and the TrustedLaunchSupported pairing rule.
Removed as unconfirmed: the replicas-per-VM-creates rule, 1001-reseal limit, private-link subnet
setting, replication and Windows Update durations, custom-role details, Packer parameter names,
Defender and policy alias names, VMSS auto-upgrade claim.
Method: documentation only; no commands were run.
