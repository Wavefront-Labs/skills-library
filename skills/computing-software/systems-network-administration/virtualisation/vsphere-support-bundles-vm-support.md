---
id: computing-software.systems-network-administration.virtualisation.vsphere-support-bundles-vm-support
name: vsphere-support-bundles-vm-support
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vm-support, support-bundle, vc-support, log-bundle, performance-snapshot, vsphere-monitoring, vsphere-troubleshooting, vmware, esxi, vcenter]
level: practitioner
status: draft
description: "Collect vSphere diagnostic bundles: vm-support on ESXi, vc-support on VCSA, from the client or API, with performance snapshots, and get them to support without filling disks."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=653
  - https://knowledge.broadcom.com/external/article?legacyId=1010705
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Collecting vSphere support bundles

**Goal:** capture the right logs promptly after an incident (before rotation deletes
them) and hand them to support efficiently.

## ESXi host
```sh
vm-support -w /vmfs/volumes/<datastore>        # writes esx-<host>-<date>.tgz there
vm-support -p -d 300 -i 10 -w /vmfs/volumes/<ds> # include a 5-minute performance snapshot
```
Or from a browser: `https://<host>/cgi-bin/vm-support.cgi`. From the vCenter client:
Actions → Export System Logs → select hosts (and optionally vCenter), include
performance data if relevant. Write to a datastore, not `/tmp` (RAM disk, may fill and
hurt the host).

## vCenter appliance
```sh
vc-support -l           # on VCSA shell, writes to /storage/log by default
```
or `https://<vcsa>/appliance/support-bundle` (with credentials), or VAMI. Bundles can be
GBs; check `/storage/log` free space first (`df -h`).

## Timing
- Collect **soon** after the event: hostd/vmkernel logs rotate within days on busy hosts.
- Note the UTC time of the incident; logs are in UTC.
- For a PSOD, collect after the host returns: the core dump is extracted into the bundle
  (see the PSOD skill) as long as a dump target was configured.

## Uploading
Use the Broadcom support portal upload for the case, or the vendor's file transfer
service. Strip nothing yourself, but be aware bundles contain hostnames, IPs, and
usernames; follow your data-handling policy before sending.

## Partial collection
For a quick look rather than a support case, copy the relevant logs only:
`scp root@<host>:/var/log/{vmkernel,hostd,vobd}.log .` and the VM's `vmware.log`.

## Verify
Bundle opens (`tar tzf` lists `var/log/*` and `commands/*` outputs), its time range covers
the incident, and the case has the upload reference.
