---
id: computing-software.systems-network-administration.virtualisation.vsphere-custom-alarm-definitions
name: vsphere-custom-alarm-definitions
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsphere-alarms, alarm-definition, alarm-actions, snmp-traps, vcenter-email, event-based-alarm, vsphere-monitoring, vmware, vcenter, vsphere]
level: practitioner
status: draft
description: "Write vCenter alarms that matter: metric vs event triggers, thresholds with durations, where to define them, email/SNMP/script actions, and pruning noisy defaults."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom vCenter alarm definitions

**Goal:** alerts that page someone only for things that need action, routed to the
monitoring system rather than an unread mailbox.

## Trigger types
- **Metric (condition/state):** e.g. datastore usage > 85% for 5 min, VM CPU ready > 10%,
  host memory > 95%. Always set a duration to avoid flapping.
- **Event:** e.g. `HostConnectionLostEvent`, `vim.event.VmDasBeingResetEvent`
  (HA reset), `com.vmware.vc.HA.VmRestartedByHAEvent`, `esx.problem.storage.apd.start`,
  snapshot consolidation needed (`com.vmware.vc.VmDiskConsolidationNeededEvent`).
- Reset rules: event alarms need a resetting event or manual reset; define one where it
  exists or they stay red forever.

## Where to define
Define at the **highest sensible object** (vCenter root or datacenter) so new objects
inherit; override for exceptions at lower objects. Many defaults are already present;
review rather than duplicate.

## Actions
- **SNMP traps** to the NMS (configure receivers in vCenter Settings → SNMP receivers).
- **Email** (vCenter Settings → Mail sender) for low-volume teams.
- **Run script** on the VCSA (vSphere 7+ scripts must live on the appliance) for
  auto-remediation; keep them idempotent.
- Repeat interval for critical alarms that stay red.
Many shops instead have their monitoring platform poll vCenter alarms/events via API;
either way, one route, not both.

## Useful custom alarms
| Alarm | Trigger |
|---|---|
| Snapshot older than 3 days | Scripted check (alarms can't see age); or size > N GB metric |
| Datastore usage | Warning 80%, critical 90%, 5 min |
| VM CPU ready | > 10% for 15 min (metric "CPU ready" percentage) |
| HA VM restarted / reset | Events above |
| Host hardware sensor | Default "Host hardware ..." alarms, ensure enabled |
| Certificate expiry | Built-in, tune the threshold |

## Hygiene
Export definitions (PowerCLI `Get-AlarmDefinition | Export-Clixml`) to keep them in source
control; review triggered-alarm counts monthly and tune or delete the noisy ones.

## Verify
Trigger a test (fill a test datastore, disconnect a lab host) and confirm the right
person/system receives it within minutes.
