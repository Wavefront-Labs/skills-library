---
id: computing-software.systems-network-administration.virtualisation.vlcm-baselines-legacy
name: vlcm-baselines-legacy
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vlcm, vlcm-baseline, update-manager, vum, baseline-group, patch-baseline, upgrade-baseline, esxi-patching, vmware, vsphere]
level: practitioner
status: draft
description: "Patch hosts with vLCM baselines (the old Update Manager model): predefined vs custom baselines, baseline groups, attach/scan/stage/remediate, and the deprecation path."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vLCM baselines and baseline groups (Update Manager model)

**Goal:** keep older or mixed clusters patched where images cannot be used yet, and know
this model is on its way out.

## Concepts
- **Patch baselines:** predefined "Critical Host Patches" and "Non-Critical Host Patches"
  (dynamic: new matching patches are included automatically), or custom fixed/dynamic
  baselines.
- **Extension baselines:** third-party VIBs (drivers, agents).
- **Upgrade baselines:** an imported ESXi ISO for major/minor upgrades.
- **Baseline group:** one upgrade baseline plus patch and extension baselines, remediated
  together in the correct order.

## Workflow
1. Lifecycle Manager → Settings → patch download source; sync updates (or import offline
   bundles; air-gapped vCenters use UMDS to build a shared depot).
2. Create/attach baselines to the **cluster** (inherit to hosts).
3. **Check compliance** (scan): hosts show compliant / non-compliant / incompatible.
4. **Stage** patches to hosts to shorten the window.
5. **Remediate** with cluster settings: disable DPM/HA admission control temporarily if
   capacity is tight, parallel remediation, migrate powered-off VMs.

## Gotchas
- Baselines are **deprecated** in vSphere 8 and removed in the following major release;
  plan conversion to images (third-party VIBs without depots block conversion).
- Dynamic "critical" baselines can pull a patch the hardware vendor has not qualified;
  for vendor-customised hosts check driver compatibility before remediating.
- Upgrade baselines from a generic VMware ISO on OEM hardware drop vendor drivers; use
  the OEM custom ISO.
- Extension baselines for drivers must match the target ESXi version after upgrade.

## Verify
After remediation all hosts in the cluster show Compliant against the attached baseline
group and the same build in `Get-VMHost | Select Name, Version, Build`.
