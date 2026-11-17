---
id: computing-software.systems-network-administration.virtualisation.proxmox-cluster-create-and-join
name: proxmox-cluster-create-and-join
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pvecm, pvecm-create, pvecm-add, corosync, proxmox-cluster, cluster-join, quorum, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Create a Proxmox VE cluster and join nodes: prerequisites (empty node, unique hostnames, corosync network), pvecm create/add with link addresses, and checking quorum."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvecm.html
  - https://github.com/proxmox/pve-docs/blob/master/pvecm.adoc
  - https://github.com/corosync/corosync/blob/main/man/corosync-cfgtool.8
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating and joining a Proxmox VE cluster

**Goal:** a quorate multi-node cluster with corosync on its own low-latency network, built
so it can be extended later.

## Prerequisites
- Same version on all nodes, date and time synchronized, UDP 5405-5412 and TCP 22 open between nodes.
- Install each node with its final hostname and IP: they cannot be changed after cluster creation. Referencing nodes by IP address in the cluster configuration is recommended; resolvable names are optional.
- The **joining node must hold no guests** (guest IDs could conflict); all existing configuration in `/etc/pve` is overwritten and the node inherits the cluster's storage configuration. Workaround: `vzdump` each guest and restore it under a different ID after joining; re-add node-local storages and adapt their node restriction.
- A dedicated physical NIC for corosync (1 Gbit is enough, latency under 5 ms), plus a second link on a different physical network. Heavy traffic on the corosync network raises latency.
- At least three nodes for HA quorum; 2-node clusters can use a QDevice as third vote.
- Use a unique cluster name; it cannot be changed later.

## Create (first node)
```sh
pvecm create prod-cluster --link0 10.99.0.11 --link1 10.98.0.11
pvecm status
```
GUI: Datacenter → Cluster → Create Cluster, choose link addresses.

## Join (each additional node, run on the new node)
```sh
pvecm add 10.99.0.11 --link0 10.99.0.12 --link1 10.98.0.12
```
GUI: on the cluster, Datacenter → Cluster → Join Information → Copy Information; on the new node, Join Cluster → paste → enter the cluster password manually → Join. By default `pvecm add` authenticates against the existing node's API with its `root@pam` password and verifies its SHA-256 certificate fingerprint, so SSH password authentication is not required; `--use_ssh` selects the legacy SSH-based join. The new node's certificate is replaced by one signed by the cluster CA, so the web session ends after a few seconds.

## After joining
- `pvecm nodes` and `pvecm status` show all members and a quorate cluster.
- Storage definitions are cluster-wide (`/etc/pve/storage.cfg`); restrict node-local storage to the nodes that have it.
- Add the node to HA rules and backup jobs as needed.

## Gotchas
- Without `--link0` the corosync network is generally shared with the web interface and guest network; moving it later means editing `/etc/pve/corosync.conf` carefully (increment `config_version`), so choose links up front.
- With a separate cluster network, pass `--link0` (and `--link1`) to `pvecm add` too.
- Several clusters on one network need unique cluster names; they also compete for latency and packet rate.
- With HA enabled, a node that loses quorum while it has active services is fenced (reset by its watchdog), so an unreliable corosync network causes outages.

## Verify
`pvecm status` shows the expected votes and a quorate cluster; `corosync-cfgtool -s` shows all links connected on every node; a test guest migrates between new and old nodes.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, pvecm.adoc, last pushed 2026-10-17) and corosync man pages (github.com/corosync/corosync, man/). Confirmed: requirements (ports, time, hostname and IP fixed after creation, unique cluster name, three nodes for HA, QDevice for two nodes, NIC and latency guidance); join overwrite and no-guests rule and the `vzdump` workaround; `pvecm create --linkX`, `pvecm add --link0/--link1`, GUI join steps, API authentication and `--use_ssh`; certificate replacement on join; multiple-cluster naming. Removed: chrony, the 2 ms latency target, the odd-vote statement, and the rename-and-rejoin claim (not documented).

Method: documentation only; no commands were run.
