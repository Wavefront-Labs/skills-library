---
id: computing-software.cloud-infrastructure-engineering.azure.capture-vm-to-managed-or-gallery-image
name: capture-vm-to-managed-or-gallery-image
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vm-images, capture-vm-image, managed-image, compute-gallery, generalize]
level: practitioner
status: docs-checked
description: "Capture an existing VM as an image: generalized vs specialized, deallocate/generalize steps, direct capture into a Compute Gallery version, and legacy managed images."
sources: ["https://learn.microsoft.com/azure/virtual-machines/capture-image-portal", "https://learn.microsoft.com/azure/virtual-machines/image-version", "https://learn.microsoft.com/azure/virtual-machines/generalize"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capture a VM to an image

**Goal:** turn a hand-configured VM into a reusable image without breaking the source by surprise.

## Decide: generalized or specialized
- **Generalized**: machine-specific information such as user accounts is removed (Sysprep on Windows,
  `waagent -deprovision` on Linux). Use for templates. Plan on the source VM no longer being usable as a server.
- **Specialized**: keeps machine-specific information and accounts. Gallery images do not require generalizing
  (generalize page). Use for cloning a known-good server for DR/test - not for scale.

## Generalized capture into a gallery
```bash
# inside the VM
#   Windows: run Sysprep with Generalize and Shutdown (steps on the generalize page)
#   Linux:   sudo waagent -deprovision+user -force   (then shut down)
az vm deallocate -g rg -n golden01
az vm generalize -g rg -n golden01
az sig image-definition create -g rg-img -r galCorp -i web-base --publisher Contoso --offer web --sku 2022 \
  --os-type Windows --os-state Generalized --hyper-v-generation V2 --features SecurityType=TrustedLaunchSupported
az sig image-version create -g rg-img -r galCorp -i web-base -e 1.0.0 \
  --virtual-machine $(az vm show -g rg -n golden01 --query id -o tsv) \
  --target-regions westeurope=2 northeurope=1 --replica-count 1
```
Create the definition with `--os-state generalized` for a generalized source (image-version page); make the other
definition settings fit the source VM.

## Specialized capture
Skip sysprep/generalize; create the definition with `--os-state Specialized`, then `az sig image-version create
--virtual-machine <id>`.

## Legacy managed image
```bash
az image create -g rg -n img-web-2022 --source golden01 --hyper-v-generation V2
```
Prefer galleries; a gallery image version can also be created from a managed image (`--managed-image`), which
must be in the same region as the version's instance details.

## Gotchas
- Snapshot the source disks before sysprep so a failed run does not cost you the VM.
- Don't capture VMs with secrets baked in; clean caches, logs, keys and agent IDs first.
- Long-term, automate image builds with Image Builder or Packer instead of capturing pets.

## Verify
- [ ] New VM from the image boots, has fresh machine identity (generalized), and passes app smoke tests.

## Checked
2026-10-28. Confirmed against the generalize, capture-image and image-version pages and the CLI checker:
generalizing is optional for gallery images, specialized images keep machine-specific information,
image sources (VM, managed image, snapshot, version), `--os-state`, `--managed-image`, `waagent -deprovision`
with `-force`, `TrustedLaunchSupported` feature value. Removed as unconfirmed: the sysprep `/mode:vm` switch,
`TrustedLaunch` as a feature value, the definition-must-match rule, the no-OS-profile statement and the
single-region/no-replication claim for managed images, sysprep failure causes.
Method: documentation only; no commands were run.
