---
id: computing-software.systems-network-administration.virtualisation.drs-affinity-and-vm-host-rules
name: drs-affinity-and-vm-host-rules
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [drs, affinity-rules, anti-affinity, vm-host-rules, drs-groups, must-run-on, should-run-on, licensing-pinning, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Write DRS rules: keep-together and separate VM rules, VM-Host groups with must vs should, licence pinning, how HA and power-on treat rules, and finding rule violations."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-resource-management-8-0/using-drs-clusters-to-manage-resources/using-affinity-rules-without-vsphere-drs.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-resource-management/using-drs-clusters-to-manage-resources/using-affinity-rules-with-vsphere-drs.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-resource-management/using-drs-clusters-to-manage-resources/using-affinity-rules-with-vsphere-drs/vm-host-affinity-rules-with-vsphere-drs.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-resource-management/using-drs-clusters-to-manage-resources/using-affinity-rules-with-vsphere-drs/vm-vm-affinity-rules-with-vsphere-drs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DRS affinity and VM-Host rules

**Goal:** keep redundant VMs apart, keep dependent VMs together, and pin licensed software
to licensed hosts, without rules that block HA or power-on.

## Rule types
| Rule | Use |
|---|---|
| Keep Virtual Machines Together (VM-VM affinity) | VMs that should share a host, for example for performance |
| Separate Virtual Machines (VM-VM anti-affinity) | Resource-intensive or redundant VMs that must not share a host, so one host problem does not take both |
| VM-Host: Must run on / Must not run on hosts in group | Hard rules, for example licensing that ties an application to specific hosts |
| VM-Host: Should run on / Should not run on hosts in group | Soft rules, for example hardware preference in a mixed-hardware cluster |

A VM-Host rule has one VM group, one host group and a must/should and run-on/not-run-on
designation. The VMs and hosts in a rule must all be in the same cluster; a VM removed
from the cluster loses its DRS group affiliation even if it returns later.

## Must vs should
- Hard (must) rules cannot be violated: not by vSphere HA failover, VM power-on or a
  user-initiated migration. If HA would have to break a hard rule it cannot fail the VM over.
- Soft (should) rules can be violated: HA restarts succeed, power-on succeeds and manual
  migrations are not blocked.
- Keep Together and Separate rules are also respected by HA failover and power-on. A
  vMotion you start yourself is not blocked by them when DRS is off.

## When the cluster is already in violation
When you add or edit a rule and the cluster violates it, the system keeps operating and
tries to correct the violation. In manual and partially automated DRS clusters the
recommendations stay until the rule is fulfilled. Without DRS nothing remediates
placement, so you must fix it yourself. VM-Host groups and rules can be created, edited
and deleted with DRS off.

## Finding violations
Select the cluster, open the DRS tab and click Faults. Any enabled rule being violated
that DRS cannot correct has a fault there; read it to see why. Violations also produce a
log event.

## Verify
DRS Faults lists no rule violations for the cluster.

## Checked
Date: 2026-11-07. Read in full from the Broadcom vSphere 8.0 Resource Management pages:
"Using Affinity Rules without vSphere DRS", "Using Affinity Rules with vSphere DRS",
"VM-Host Affinity Rules with vSphere DRS" and "VM-VM Affinity Rules with vSphere DRS"
(navigation text ignored). Confirmed: the four VM-Host sub-rules and hard/soft
persistence, HA/power-on/vMotion behaviour, the same-cluster and group-affiliation
statements, and the DRS tab Faults check. Removed as not on those pages: the PowerCLI
cmdlet block, the "HA should respect VM to Host affinity rules" option, "older rule wins"
conflict handling, Configure menu paths, maintenance-mode blocking, the more-VMs-than-hosts
remark, licensing-audit advice and the Get-DrsRule verify step. The "Create a VM-Host
Affinity Rule" and "VM-VM Affinity Rule Conflicts" pages were not opened (URL guesses 404).
Method: documentation only; no commands were run.
