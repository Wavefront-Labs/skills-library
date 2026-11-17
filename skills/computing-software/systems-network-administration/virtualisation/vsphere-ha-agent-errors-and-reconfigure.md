---
id: computing-software.systems-network-administration.virtualisation.vsphere-ha-agent-errors-and-reconfigure
name: vsphere-ha-agent-errors-and-reconfigure
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [ha-agent-error, vsphere-ha, fdm, reconfigure-ha, vmware, vsphere]
level: practitioner
status: draft
description: "Fix vSphere HA agent errors (cannot install, unreachable, not initialized, election issues): check the fdm agent, logs and ports, then reconfigure HA on the host."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=1003714
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSphere HA agent errors and reconfigure

**Goal:** every host shows *Running (Primary)* or *Connected (Secondary)* in the HA state.

## Common states
- *vSphere HA agent cannot be installed/configured*: VIB push failed, often low disk/RAM on host, or a stuck vLCM operation.
- *Agent unreachable*: vCenter cannot reach fdm on TCP/UDP 8182.
- *Not initialized / Uninitialization error*: fdm failed to start or the host cannot see heartbeat datastores.
- *Election in progress* for a long time: management network partition.

## First moves
1. Host -> right click -> **Reconfigure for vSphere HA**. Fixes most transient issues.
2. If that fails: turn HA off and on at cluster level (all hosts reconfigure; protection off for minutes).

## Host-side checks
```sh
/etc/init.d/vmware-fdm status
/etc/init.d/vmware-fdm restart
esxcli software vib list | grep -i fdm        # vmware-fdm VIB version should match vCenter
tail -f /var/log/fdm.log                      # election, heartbeat, isolation messages
esxcli network firewall ruleset list | grep -i fdm
```
`/var/run/log/fdm*` and vCenter `vpxd.log` show the install/configure error text.

## Reinstall the agent
```sh
cp /opt/vmware/uninstallers/VMware-fdm-uninstall.sh /tmp/ && sh /tmp/VMware-fdm-uninstall.sh
```
Then *Reconfigure for vSphere HA*; vCenter pushes a fresh fdm VIB.

## Other causes
- DNS: HA needs the host to resolve its own name and vCenter's; check `/etc/hosts` overrides.
- Isolation addresses unreachable (default gateway blocked ICMP): set `das.isolationaddress0` to a pingable address.
- Heartbeat datastores: fewer than two shared datastores gives a config warning, not an agent failure.

## Verify
Cluster -> Monitor -> vSphere HA -> Summary shows one primary and all others connected; no HA config issues listed.
