---
id: computing-software.systems-network-administration.virtualisation.vsphere-ha-vm-monitoring-and-vmcp
name: vsphere-ha-vm-monitoring-and-vmcp
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsphere-ha, vm-monitoring, vm-component-protection, vmcp, apd, pdl, application-monitoring, vmware-tools-heartbeat, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Configure vSphere HA VM monitoring (VMware Tools heartbeats), application monitoring and VM Component Protection for APD/PDL storage failures, with sane sensitivity."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-availability/creating-and-using-vsphere-ha-clusters/configuring-cluster-settings/set-advanced-options/vsphere-ha-advanced-options.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# vSphere HA VM monitoring and VM Component Protection

**Goal:** HA restarts not only VMs on failed hosts, but also hung guests and VMs that lost
their storage, without rebooting healthy VMs by mistake.

## VM monitoring
- Uses **VMware Tools heartbeats** plus disk and network I/O. If heartbeats stop and
  there was no I/O within the window, HA resets the VM.
- **Sensitivity** presets trade reset speed against false positives; the default I/O stats
  interval for VM Monitoring sensitivity is 120 seconds (`das.iostatsinterval`; values
  below 50 are not recommended, 0 deactivates the check). Start at Medium or Low; High
  resets VMs that are merely busy.
- **Application monitoring** needs an app that calls the Tools guest SDK heartbeat
  (few do, mostly vendor appliances).
- Per-VM overrides: disable monitoring for VMs that are frequently suspended or have
  Tools uninstalled on purpose.

## VM Component Protection (VMCP)
Responds when a host loses access to a VM's datastore while the host itself is fine.
| Condition | Meaning | Typical response |
|---|---|---|
| PDL (permanent device loss) | Array says LUN is gone (SCSI sense codes) | Power off and restart VMs |
| APD (all paths down) | No response, may come back | Wait the APD timeout plus delay, then restart conservatively or aggressively |
"Conservative" restarts only if another host can run the VM; "aggressive" powers off
even when placement is not confirmed. VMCP requires HA host monitoring enabled.

## Gotchas
- VMs without VMware Tools trigger VM monitoring false positives only if Tools was
  previously running; a Tools upgrade that hangs can look like a guest hang.
- An APD response that does nothing leaves VMs hung indefinitely on a dead path; enable
  at least event reporting so someone sees it.
- VMCP does not help NFS mounts that hang without APD semantics on old versions.

## Verify
Cluster → Configure → vSphere Availability shows VM monitoring and VMCP settings;
test in a lab by freezing a guest (e.g. kernel `echo c > /proc/sysrq-trigger` on a Linux
test VM) and confirm HA resets it with an event logged.

## Checked
2026-10-31: `das.iostatsinterval` (default 120 s, values below 50 not recommended, 0 deactivates the check) and the VMCP reset/terminate retry options (`das.maxresets`, `das.maxterminates`) confirmed on the vSphere HA Advanced Options page. Removed unconfirmed figures: the 30/60/120 s sensitivity presets, the 3-resets-per-hour limit, the screenshot-on-reset claim, the 140 s APD timeout and the 3-minute delay.
Method: documentation only; no commands were run.
