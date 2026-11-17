---
id: computing-software.systems-network-administration.virtualisation.vsphere-ha-advanced-options
name: vsphere-ha-advanced-options
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [das-isolationaddress, ha-advanced-options, vsphere-ha, isolation-response, datastore-heartbeat, vmware, vsphere]
level: advanced
status: docs-checked
description: "Set the vSphere HA advanced options that matter: das.isolationaddress, usedefaultisolationaddress, heartbeatDsPerHost, ignoreRedundantNetWarning and more, with when to use each."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-availability/creating-and-using-vsphere-ha-clusters/configuring-cluster-settings/set-advanced-options/vsphere-ha-advanced-options.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# vSphere HA advanced options

Set at Cluster → Configure → vSphere Availability → Edit → Advanced Options. After
changing `das.isolationaddress[...]`, `das.usedefaultisolationaddress` or
`das.isolationshutdowntimeout`, you must deactivate and re-activate vSphere HA for the
change to take effect.

## Options worth knowing
| Option | Value | Why |
|---|---|---|
| `das.isolationaddress0` … `9` | IP | Addresses pinged to detect isolation when no heartbeats are received; up to 10, typically one per management network; too many slow detection down |
| `das.usedefaultisolationaddress` | true/false | Whether the default gateway of the console network is used as the isolation address |
| `das.heartbeatDsPerHost` | 2–5 | Number of heartbeat datastores required (default 2) |
| `das.ignoreInsufficientHbDatastore` | true | Silences the insufficient-heartbeat-datastore issue (default false) |
| `das.isolationshutdowntimeout` | seconds (default 300) | Time to wait for guest shutdown before power off when the isolation response is Shut down |
| `das.respectVmVmAntiAffinityRules` | true/false (default true) | HA honours VM-VM anti-affinity on restart, even without DRS |
| `das.maxresets`, `das.maxterminates` | n | VMCP retry limits for resets and terminations (APD) |
| `das.config.fdm.isolationPolicyDelaySec` | seconds (minimum 30) | Delay before acting on isolation (stretched/vSAN designs) |
| `das.slotCpuInMHz`, `das.slotMemInMB` | MHz / MB | Cap slot size when using slot policy admission control |

## Typical recipes
- **vSAN cluster**: `das.usedefaultisolationaddress=false`,
  `das.isolationaddress0=<vSAN network gateway or switch SVI>` (and `1` for second
  fault-domain switch).
- **Stretched cluster**: one isolation address per site on the vSAN network, both
  reachable from each site.
- **Single shared datastore in a small site**: `das.ignoreInsufficientHbDatastore=true`
  rather than leaving a permanent warning that hides real ones.

## Gotchas
- Typos are accepted silently: `das.isolationadress0` does nothing. Check fdm.log
  after reconfigure for the addresses being pinged.
- Options are cluster-wide.
- Do not silence network-redundancy warnings in production to hide a real single point
  of failure.

## Verify
Check the cluster's advanced options in the vSphere Client, and on a host
`grep -i isolationaddress /var/run/log/fdm.log`.

## Checked
2026-10-31: `das.isolationaddress[0-9]` (up to 10), `das.usedefaultisolationaddress`, `das.isolationshutdowntimeout` (default 300 s, and the disable/re-enable HA requirement), `das.heartbeatdsperhost` (2–5, default 2), `das.ignoreinsufficienthbdatastore` (default false), `das.respectvmvmantiaffinityrules` (default true), `das.maxresets`/`das.maxterminates` (VMCP), `das.config.fdm.isolationPolicyDelaySec` (minimum 30 s) and the slot-size options confirmed on the vSphere HA Advanced Options page; multiple isolation addresses and `das.usedefaultisolationaddress=false` confirmed in KB 341627. Removed unconfirmed options: `das.ignoreRedundantNetWarning`, `das.maxresetwindow` and the host-profiles claim.
Method: documentation only; no commands were run.
