---
id: computing-software.systems-network-administration.backup-and-recovery.vmware-cbt-reset
name: vmware-cbt-reset
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [cbt-reset, changed-block-tracking, cbt, vadp, image-level-backup, vmware]
level: advanced
status: docs-checked
description: "Reset VMware Changed Block Tracking when incrementals look wrong: powered-off ctkEnabled steps, the KB PowerCLI script, and the full that follows."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=2139574
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resetting Changed Block Tracking (CBT)

CBT (`-ctk.vmdk` files) tells backup software which blocks changed, enabling fast incrementals. A wrong CBT map can silently produce bad incrementals, so reset it when a vendor or VMware KB says so, or after CBT errors in backup logs.

## Method 1: powered off (Broadcom KB)
1. Power off the VM.
2. In Snapshot Manager make sure there are no active snapshots; if there are, consolidate them.
3. Edit Settings > Advanced > Configuration Parameters: set `ctkEnabled` to false, and set `scsiX:Y.ctkEnabled` to false for every attached virtual disk.
4. SSH to the host, go to the VM folder under `/vmfs/volumes/<datastore>/<VM>` and remove the `.vmsd` file and any `ctk.vmdk` files (or move them to a subfolder).
5. Power the VM on. If your backup application uses CBT, re-enable CBT manually; some tools enable it automatically.

## Method 2: PowerCLI script (many VMs, no power cycle)
The KB attaches a script, `CBT-Reset.PS1` (in `2139574_CBT-Reset.zip`). Run it in PowerCLI after `Connect-VIServer`. It reports which VMs can be reset and which cannot (VMs powered off or with snapshots), takes a temporary snapshot instead of a power cycle, asks for confirmation, then resets CBT on powered-on VMs without snapshots. Running it needs unsigned scripts allowed (the KB uses `Set-ExecutionPolicy Bypass` and warns to disable it after use).

## After reset
The first backup after a reset is a full; later incrementals reference only change IDs generated after that full. Schedule it, because it is slow.

## Verify
The next incremental after the full is normal in size, and a test restore from it boots and passes application checks.

## Checked
2026-11-09. Read in full: Broadcom KB "Resetting Changed Block Tracking for VMware vSphere virtual machines" (applies to ESXi 6.x to 8.x). Removed as unstated: the hand-written snapshot-cycle PowerCLI, named CBT bugs and the 128 GB claim, specific backup error strings, pRDM/independent-disk limits, Veeam "Reset CBT" option, and the vSphere 8 admin guide source (landing page only).
Method: documentation only; no commands were run.
