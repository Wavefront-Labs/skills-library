---
id: computing-software.systems-network-administration.virtualisation.vcenter-high-availability-vcha
name: vcenter-high-availability-vcha
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vcenter-ha, vcha, vcenter-availability, witness, active-passive, vsphere-ha, vmware, vcenter, vsphere]
level: advanced
status: draft
description: "Decide on and configure vCenter HA (active, passive, witness): network prerequisites, failover behaviour, maintenance mode and why plain vSphere HA is often enough."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vCenter High Availability (VCHA)

**Goal:** protect vCenter against host, hardware and appliance failures where the
minutes vSphere HA takes to restart it are not acceptable.

## Do you need it?
vSphere HA already restarts a failed VCSA VM on another host (2-5 minutes plus service
start). VCHA cuts that to a few minutes of failover but adds two extra appliances, a
dedicated network and more upgrade steps. It does **not** protect against logical
corruption: that is what file-based backup is for. Many shops choose HA restart
priority "highest" plus backups instead.

## Architecture
- **Active** node serves clients; **Passive** receives synchronous PostgreSQL
  replication and file sync; **Witness** breaks ties.
- A separate **HA network** (own subnet, latency < 10 ms between nodes) besides the
  management network. The management IP moves to the passive node on failover.
- Place the three nodes on different hosts and ideally different datastores (DRS
  anti-affinity rule).

## Configure
vCenter → Configure → vCenter HA → Set Up: choose HA network port group, IPs for the
three HA interfaces, and placement. Automatic clones the active node to make passive and
witness (requires vCenter to manage its own host).

## Operations
- **Maintenance mode:** use it before network or host work; replication continues but
  automatic failover is off.
- **Disable/Enable** during upgrades or large changes; patches are applied by the
  workflow to all nodes (VCSA patch via VAMI handles VCHA in 7/8, check the release notes).
- **Manual failover** to test: Initiate Failover; expect client sessions to drop.
- Snapshots of VCHA nodes are not supported as a rollback mechanism; remove VCHA before
  reverting.

## Failure modes
- HA network latency or MTU mismatch → replication falls behind → cluster degraded.
- Passive node on the same host as active: one host failure loses both.
- Certificates replaced on active not reflected on passive when done outside the
  supported workflow.

## Verify
vCenter HA page shows mode Enabled, state Healthy, all three nodes up; a test failover
completes and clients reconnect to the same FQDN.
