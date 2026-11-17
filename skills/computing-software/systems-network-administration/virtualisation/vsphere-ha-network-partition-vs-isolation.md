---
id: computing-software.systems-network-administration.virtualisation.vsphere-ha-network-partition-vs-isolation
name: vsphere-ha-network-partition-vs-isolation
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [network-partition, vsphere-ha, isolation-response, fdm, datastore-heartbeat, vmware, vsphere]
level: advanced
status: draft
description: "Tell a vSphere HA network partition from host isolation, how datastore heartbeats decide, what HA does to VMs in each case, and how to diagnose from fdm.log."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HA: network partition vs isolation

## Definitions
- **Isolated host**: a host that cannot reach any other host's HA agent **and** cannot
  ping its isolation address(es) (default gateway of the management network, or
  `das.isolationaddressN`). It applies the **isolation response** (disabled / shut down /
  power off) to its VMs.
- **Partitioned hosts**: a group of hosts that can talk among themselves and ping the
  isolation address, but not the primary. Each partition elects its own primary.
  No isolation response is applied.
- **Failed host**: no network heartbeats, no datastore heartbeats, no ping response.
  HA restarts its VMs elsewhere.

## How HA decides (primary's view of a silent host)
| Network heartbeat | Datastore heartbeat | Pings host IP | Conclusion |
|---|---|---|---|
| no | yes | - | isolated or partitioned (host is alive); no restart unless it powers VMs off |
| no | no | no | failed: restart VMs |
| no | no | yes | partitioned, unknown: wait |
Datastore heartbeats (2 per host by default, `das.heartbeatDsPerHost` up to 5) are why
shared datastores matter even with good networks. vSAN-only clusters have no datastore
heartbeat (vSAN datastore cannot be used); network design carries the whole decision.

## What happens to VMs
- Isolation with response *Power off*: VMs powered off on the isolated host, restarted
  by the primary elsewhere once it sees the power-off via heartbeat datastore
  (poweron file). Use **Power off** for vSAN/IP storage (VMs likely lost storage too),
  **Disabled** when storage is FC and management-network blips are common.
- Partition: VMs keep running where they are; HA in the partition without the VM's host
  does not restart it (it still sees the VM's datastore lock held).

## Diagnose
```sh
grep -iE "isolat|partition|election|primary" /var/run/log/fdm.log | tail -50
/opt/vmware/fdm/fdm/prettyPrint.sh hostlist      # who this agent sees
```
vCenter: Cluster → Monitor → vSphere HA → Summary shows Primary, Connected (secondary),
Network Partitioned, Network Isolated per host.

## Gotchas
- Isolation address must be something that answers ICMP and lives on the management
  path; set two (`das.isolationaddress0/1`) on redundant paths, and
  `das.usedefaultisolationaddress=false` if the gateway does not answer ping.
- vSAN clusters use the vSAN network for HA heartbeats; isolation address should be on
  the vSAN network.

## Verify
Pull the management uplinks on a test host in a window: observe "Network Isolated" in
HA summary and the configured response; restore and confirm it rejoins as secondary.
