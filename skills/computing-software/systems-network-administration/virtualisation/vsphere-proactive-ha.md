---
id: computing-software.systems-network-administration.virtualisation.vsphere-proactive-ha
name: vsphere-proactive-ha
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [proactive-ha, vsphere-ha, drs, quarantine-mode, health-provider, openmanage-integration, hpe-oneview, hardware-health, vmware, vsphere]
level: practitioner
status: draft
description: "Enable vSphere Proactive HA with a vendor health provider so DRS evacuates hosts with degraded fans, PSUs or memory; choose quarantine vs maintenance remediation."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSphere Proactive HA

**Goal:** move VMs off a host when its hardware starts failing (a redundant PSU or fan
lost, correctable memory errors) before it actually crashes.

## Requirements
- DRS enabled (Proactive HA uses DRS to migrate).
- A **health provider** from the server vendor registered in vCenter, e.g. Dell
  OpenManage Integration for VMware vCenter (OMIVV), HPE OneView for vCenter, Lenovo
  XClarity Integrator, Cisco UCS. Without one, the feature has nothing to react to.

## Configure (Cluster → Configure → vSphere Availability → Proactive HA → Edit)
- **Automation level:** Manual (recommendations) or Automated.
- **Remediation:**
  - *Quarantine mode for all failures*: avoid placing new VMs on the host, migrate only
    if it does not hurt performance. Good for moderate degradation.
  - *Quarantine for moderate, maintenance mode for severe*: recommended mixed setting.
  - *Maintenance mode for all failures*: evacuate on any alert; needs N+1 spare capacity.
- Select the provider and which failure conditions it should act on; you can block
  individual conditions per host.

## Interaction with other features
- Quarantine is a DRS soft rule; HA still restarts VMs there in a real failure.
- Maintenance mode remediation respects DRS rules; must-rules can block evacuation.
- vSAN hosts: maintenance remediation uses the default "ensure accessibility" mode.

## Gotchas
- Health provider appliances need their own patching, credentials to iDRAC/iLO, and
  certificates; if the provider is down, Proactive HA silently does nothing.
- Over-sensitive conditions in small clusters can evacuate several hosts and leave too
  little capacity; begin with Manual automation for a month.

## Verify
Cluster → Monitor → vSphere HA → Proactive HA shows the provider and host states
Healthy; simulate a failure via the provider's test feature (many have one) and confirm
the host enters quarantine and DRS migrates VMs.
