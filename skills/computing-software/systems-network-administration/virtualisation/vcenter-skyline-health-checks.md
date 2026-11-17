---
id: computing-software.systems-network-administration.virtualisation.vcenter-skyline-health-checks
name: vcenter-skyline-health-checks
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vcenter-skyline-health, skyline-health, health-checks, vmware, vsphere]
level: intro
status: draft
description: "Run and act on Skyline Health findings in vCenter: online health checks, CEIP requirement, retesting, silencing and following the linked KBs."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
  - https://knowledge.broadcom.com/external/article?legacyId=57187
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Skyline Health checks in vCenter

**Goal:** catch known configuration and compatibility issues before they cause incidents.

## Where
- vCenter object -> **Monitor** -> *Skyline Health*: vSphere online health checks (known issues, compatibility, security advisories) for vCenter and hosts.
- Cluster with vSAN -> Monitor -> vSAN -> *Skyline Health*: vSAN-specific checks.
- A separate *Skyline Health Diagnostics* appliance analyses log bundles offline for deeper findings.

## Requirements
Online checks need the **Customer Experience Improvement Program** (CEIP) enabled (Administration -> Deployment -> Customer Experience Improvement Program) and outbound HTTPS from vCenter to the VMware/Broadcom endpoints, directly or via proxy configured in VAMI.

## Working the findings
1. Sort by severity; each finding links a KB with cause and fix.
2. Fix, then click **Retest** to confirm.
3. *Silence alert* only for accepted, documented exceptions (for example a lab-only setting); record why.
4. Recheck after every patch cycle; new checks arrive without upgrades.

## Gotchas
- "Online health connectivity" warnings mean the checks themselves are not running; fix proxy/DNS before trusting a green state.
- Offline/air-gapped sites cannot use online checks; use the vSAN HCL DB offline file for vSAN and Skyline Health Diagnostics for log analysis.

## Verify
Online health connectivity is green and the remaining findings are fixed or documented as silenced exceptions.
