---
id: computing-software.systems-network-administration.patch-management.storage-array-non-disruptive-upgrades
name: storage-array-non-disruptive-upgrades
category: computing-software
field: systems-network-administration
product: patch-management
tags: [ontap-ndu, non-disruptive-upgrade, netapp, storage-upgrade, network-device-patching, patch-management]
level: practitioner
status: draft
description: "Run storage array non-disruptive upgrades: NetApp ONTAP automated NDU with takeover/giveback, pre-checks (Active IQ, host multipath), and vendor-assisted upgrades elsewhere."
sources:
  - https://docs.netapp.com/us-en/ontap/upgrade/automated-upgrade-task.html
  - https://docs.netapp.com/us-en/ontap/upgrade/prepare.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage array non-disruptive upgrades

Arrays with dual controllers upgrade one controller at a time while the partner serves I/O. "Non-disruptive" depends on hosts having healthy multipathing.

## NetApp ONTAP automated NDU
1. Plan: Active IQ Digital Advisor Upgrade Advisor for path and risks; supported upgrade paths (direct within some releases, multi-hop for older).
2. Pre-checks:
```text
cluster image validate -version 9.15.1        ! runs pre-update checks
storage failover show                          ! takeover possible = true
network interface show -is-home false          ! all LIFs home
system health alert show
```
Hosts: verify multipath (ALUA) on every initiator (`multipath -ll`, `Get-MPIOSetting`, ESXi `esxcli storage nmp device list`), and SAN host utilities versions per Interoperability Matrix.
3. Upload and run:
```text
cluster image package get -url http://webserver/96_q_image.tgz
cluster image update -version 9.15.1
cluster image show-update-progress
```
ONTAP does takeover of node A, upgrades, giveback, then node B (rolling per HA pair; batches for large clusters).
4. Post: `cluster image show`, `version`, LIFs home, aggregates online.

## Other arrays
- Pure Storage Purity upgrades are usually performed or monitored by Pure support (self-service via Pure1 on newer releases), controller failover based.
- Dell PowerStore/Unity, HPE Alletra/Primera: built-in NDU wizards with health checks; follow the vendor pre-check report.

## Gotchas
- Hosts with a single path or misconfigured timeouts (iSCSI, NFS hard mounts, Windows disk timeout) drop during takeover; fix before NDU.
- CIFS/SMB sessions without continuous availability reconnect; long-running copies may fail.
- Do not combine NDU with disk shelf firmware or switch changes in one window.

## Verify
Both nodes on target version, no LIFs off home, storage failover enabled, no host path errors logged during the window.
