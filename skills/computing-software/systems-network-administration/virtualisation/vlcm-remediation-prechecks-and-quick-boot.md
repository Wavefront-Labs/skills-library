---
id: computing-software.systems-network-administration.virtualisation.vlcm-remediation-prechecks-and-quick-boot
name: vlcm-remediation-prechecks-and-quick-boot
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vlcm-remediation, quick-boot, vlcm, lifecycle-manager, vsphere-upgrade, maintenance-mode, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Run vSphere Lifecycle Manager remediation safely: pre-checks, remediation settings (parallel, Quick Boot, VM power actions), staging, and handling blocked hosts."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/managing-host-and-cluster-lifecycle-8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vLCM remediation: pre-checks, settings, Quick Boot

## Before you click Remediate
1. **Check compliance** (Cluster → Updates → Image → Check Compliance).
2. **Run pre-check**: validates HA admission control headroom, DRS fully automated,
   vSAN health and object accessibility, removable media attached to VMs, passthrough
   devices, FT VMs, host profiles, hardware compatibility (HCL/vSAN HCL).
3. **Stage**: pushing payloads to hosts ahead of the window cuts remediation time.

## Remediation settings (Lifecycle Manager → Settings → Host Remediation, overridable per run)
| Setting | Recommendation |
|---|---|
| VM power state | Do not change (rely on DRS vMotion) |
| Retry entering maintenance mode | several retries with a short wait |
| Disable DPM / HA admission control / FT during remediation | on for tight clusters |
| Migrate powered-off and suspended VMs | on |
| **Quick Boot** | on where hardware supports it: skips firmware POST and shortens the reboot |
| **Parallel remediation** | only for hosts already in maintenance mode; set max concurrent |
| vSAN: maintenance mode data migration | Ensure accessibility (default) |

Check Quick Boot support per host and per remediation run (TPM-based attestation,
passthrough devices or firmware updates can force a full reboot).

## Blocked hosts: what to look for
- "Host cannot enter maintenance mode": VMs pinned by VM-Host must rules, local storage,
  CD/ISO mounted, vGPU without migration support, insufficient capacity (admission control).
- vSAN: inaccessible-object warnings mean a component is already absent elsewhere; fix
  vSAN first.
- Third-party VIBs not in image: add the vendor add-on/component to the image or remove.

## Order of operations for a full stack upgrade
vCenter first → hosts (vLCM) → vSAN disk format → VM hardware/Tools. Check the
interoperability matrix for NSX, backup and storage plug-ins before vCenter.

## Verify
Cluster shows **Compliant**; each host build matches the image; vSAN health green; no
hosts left in maintenance mode.

## Checked
2026-10-31: vSphere Lifecycle Manager remediation settings, images, HCL/hardware compatibility checks and Quick Boot confirmed as documented features in the Managing Host and Cluster Lifecycle guide (TOC and overview pages). Removed unconfirmed specifics: the `loadESXCheckCompat.py` path, the `vmware -vl` command, Quick Boot timing (~1-2 min), version gates (8.0+, 7.0U2+) and the retry counts.
Method: documentation only; no commands were run.
