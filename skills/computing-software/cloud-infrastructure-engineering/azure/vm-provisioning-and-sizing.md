---
id: computing-software.cloud-infrastructure-engineering.azure.vm-provisioning-and-sizing
name: vm-provisioning-and-sizing
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, virtual-machines, vm-sizing, vm-sizes, vm-creation, vm-series, az-vm, cloud-init, trusted-launch, generation-2, nested-virtualization, accelerated-networking, ephemeral-os-disk, vm-resize, deallocate, quotas, vcpu-quota, capacity-planning, dsv5, ebsv5, spot-vms, ssh-keys, windows-admin-password, nic-per-size]
level: practitioner
status: docs-checked
description: "Create and size Azure VMs: decode size names, Trusted Launch, ephemeral OS disks, billing by power state, quotas, capacity errors and az vm create flags."
sources: ["https://learn.microsoft.com/en-us/azure/virtual-machines/vm-naming-conventions", "https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/overview", "https://learn.microsoft.com/en-us/azure/virtual-machines/linux/quick-create-cli", "https://learn.microsoft.com/en-us/azure/virtual-machines/trusted-launch", "https://learn.microsoft.com/en-us/azure/virtual-machines/ephemeral-os-disks", "https://learn.microsoft.com/en-us/azure/virtual-machines/states-billing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM provisioning and sizing — the right series, created repeatably

**Goal:** a VM whose size name you can decode, that boots secure by default, and that was
created by a command you can rerun.

## 1. Decode the size name
Pattern: family, optional subfamily, number of vCPUs, optional constrained vCPUs, additive
features, optional accelerator, optional memory capacity, version.
`Standard_D4ads_v5` → family **D**, **4** vCPUs, features **a** (AMD processor), **d** (local
temporary disk), **s** (compatible with any Premium SSD type), version **v5**. No CPU letter
means Intel x86-64; `p` means ARM-based (Microsoft Cobalt or Ampere Altra).
Other additive letters: `b` remote storage bandwidth optimised, `i` isolated, `l` low memory,
`m` memory intensive, `n` network optimised, `r` RDMA (InfiniBand) network, `t` tiny memory.
Sizes are grouped by type: general purpose, compute optimised, memory optimised, storage
optimised, GPU accelerated and FPGA accelerated; the B family is the burstable one.
Check per-size limits before choosing: max data disks, **uncached disk IOPS/MBps**
(often the real ceiling for databases), NICs, and whether accelerated networking is
supported — `az vm list-skus -l uksouth --size Standard_E8bds_v5 --query "[].capabilities"`.

## 2. Create
```bash
az vm create -g rg -n vm-app-01 -l uksouth --image <image-urn> --size Standard_D4ads_v5 \
  --zone 1 --admin-username azureuser --ssh-key-values ~/.ssh/id_ed25519.pub \
  --security-type TrustedLaunch --enable-secure-boot true --enable-vtpm true \
  --os-disk-size-gb 64 --storage-sku Premium_LRS --ephemeral-os-disk false \
  --nsg "" --public-ip-address "" --subnet <subnet-id> --accelerated-networking true \
  --custom-data cloud-init.yaml --assign-identity [system] --tags env=prod
```
- `--image`: a URN `Publisher:Offer:Sku:Version`
  (`az vm image list --all -p Canonical -f ubuntu-24_04-lts --query "[].urn" -o tsv`), an
  alias from `az vm image list`, or a Compute Gallery image ID. Some marketplace images need
  `az vm image terms accept`.
- **Trusted Launch** improves the security of Generation 2 VMs (Secure Boot, vTPM); it
  supports x64 and Arm64, but only on supported size families. An existing Gen1 VM can be
  upgraded to Gen2-Trusted launch (see the Trusted Launch page).
- With Secure Boot on, a boot component that is not signed by a trusted publisher makes the
  VM fail to boot; the CUDA driver on Ubuntu needs extra steps and GRID on Linux needs Secure
  Boot off (Trusted Launch page).
- `--public-ip-address ""` and `--nsg ""` — never let the CLI auto-create a public IP/NSG
  in production; reach it via Bastion.
- Windows: `--admin-password` from Key Vault; `--license-type Windows_Server` for Hybrid Benefit.
- **Ephemeral OS disk** (`--ephemeral-os-disk true --ephemeral-os-disk-placement CacheDisk|ResourceDisk|NvmeDisk`):
  lives on local VM storage, lower latency and faster reimage; for stateless workloads. The
  image OS disk must fit the NVMe, temp or cache disk of the size. Placement does not change
  cost or performance; by default Azure picks a placement for the SKU.
- `--custom-data` = cloud-init (Linux) runs once; use for packages/users; config drift tooling after.
- Spot: `--priority Spot --eviction-policy Deallocate --max-price -1`.

## 3. Lifecycle semantics
- Billing follows power state: **Stopped** (allocated, shut down from inside the guest or
  PowerOff) is still billed; **Deallocated** releases the hardware and is not billed for
  compute (States and billing page; check that page for what else keeps billing).
- `az vm deallocate` to release compute; `az vm resize --size Standard_D8ads_v5` to change
  size (`az vm list-vm-resize-options` shows what fits the current hardware).
- `az vm redeploy` and `az vm reapply` exist for host and state problems.
- Deleting: `--os-disk-delete-option Delete --nic-delete-option Delete --data-disk-delete-option Detach`
  at create time decides what `az vm delete` cleans up.

## 4. Quotas and capacity
- Check usage per region with `az vm list-usage -l uksouth -o table`; request increases in
  the Quotas blade or with `az quota create` ahead of launches.
- Capacity and SKU restriction errors: inspect restrictions with
  `az vm list-skus -l uksouth --zone --query "[?name=='Standard_NC24ads_A100_v4'].restrictions"`.
  Mitigate with capacity reservations, alternative sizes, or a flexible VMSS with multiple sizes.
- `az vm list-skus --resource-type virtualMachines -l <region> --all` includes restricted SKUs for your subscription.

## Gotchas
- B-series is the burstable family; confirm it fits a sustained workload before choosing it.
- Check Site Recovery and extension support for Trusted Launch before enabling it on VMs you must protect.

## Verify
- [ ] `az vm show -d --query "{size:hardwareProfile.vmSize,sec:securityProfile.securityType}"` matches intent; no public IP in prod.
- [ ] `az vm get-instance-view --query instanceView.statuses` shows a succeeded provisioning state and a running power state.
- [ ] cloud-init log `/var/log/cloud-init-output.log` ends without errors.
- [ ] Quota headroom covers the planned fleet in `az vm list-usage`.

## Checked
2026-10-28. Confirmed against the VM naming conventions, VM sizes overview, Trusted Launch,
Ephemeral OS disks and States and billing pages: size-name letters, the CPU vendor rule,
power-state billing, ephemeral placement options and the NVMe/temp/cache fit rule, Trusted
Launch scope and Gen1 upgrade path. Removed: family ratio table, default quota figures, the
claim that Gen1 cannot be converted (the page says it can be upgraded), Gen2 default and 2 TB
disk claims, image alias names, public-IP-change, temp-disk-wipe, accelerated-networking and
resize-cap claims, credit metric name.
Commands were checked for existence by the command checker only.
Method: documentation only; no commands were run.
