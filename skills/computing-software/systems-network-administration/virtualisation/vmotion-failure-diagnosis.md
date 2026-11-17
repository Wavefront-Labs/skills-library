---
id: computing-software.systems-network-administration.virtualisation.vmotion-failure-diagnosis
name: vmotion-failure-diagnosis
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmotion, vmotion-failure, vmkping, vsphere-troubleshooting, vmkernel-log, migration-timeout, stun-time, vmware, esxi, vsphere]
level: practitioner
status: draft
description: "Diagnose failed or slow vMotions: compatibility errors, vmkping across vMotion vmks, timeouts at 14% and 20%, stun time, devices that block migration, and the logs to read."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=1003734
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-and-host-management-8-0.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Diagnosing vMotion failures

**Goal:** find why a vMotion fails or is slow, in the order that solves most cases fastest.

## 1. Read the compatibility error
The migration wizard's compatibility check is specific; common ones:
- "Currently connected network interface uses network X, which is not accessible":
  port group missing or misnamed on the destination.
- "CPU of the host is incompatible": no EVC or EVC baseline too high; power-cycle the VM
  into the right EVC mode or enable per-VM EVC.
- Device backed by a local resource: connected CD/ISO on local datastore, USB passthrough,
  serial port to file, PCI passthrough, vGPU without vMotion support.
```powershell
Get-VM | Get-CDDrive | Where {$_.IsoPath -or $_.HostDevice} | Set-CDDrive -NoMedia -Confirm:$false
```

## 2. Network test between vMotion vmks
```sh
esxcli network ip interface list ; esxcli network ip interface tag get -i vmk1
vmkping -I vmk1 <dest-vmotion-ip>                 # add -S vmotion if on the vMotion stack
vmkping -I vmk1 -d -s 8972 <dest-vmotion-ip>      # jumbo path check
```
Failure at **14%** usually means the hosts cannot reach each other on vMotion
(wrong VLAN, IP, or vMotion not enabled on the vmk). Failure around **20%** with
"Timed out waiting for migration data" points at MTU mismatch or a firewall dropping
port 8000.

## 3. Logs
- Source and destination `/var/log/vmkernel.log` (search `Migrate:` and the migration ID).
- VM's `vmware.log` in its folder (`MigrateStart`, `stun`).
- `/var/log/hostd.log` for task errors; vCenter task details give the migration ID.

## 4. Slow vMotion or long stun
- Large, fast-changing memory (DBs) needs more bandwidth; check vmnic utilisation and
  use multi-NIC vMotion or 25 GbE.
- Stun During Page Send (SDPS) throttles the vCPU when the page dirty rate exceeds
  bandwidth: visible as brief app latency.
- Snapshots with many delta disks increase switchover time.

## 5. Other usual suspects
- Time skew between hosts, or the destination datastore not mounted by the destination
  host (for compute-only vMotion).
- Licence edition without vMotion on one host.
- Lockdown or certificate issues between hosts after reinstalling one (reconnect host).

## Verify
Fix, rerun the compatibility check, then vMotion the VM back and forth between the pair;
repeat for each host pair if the cause was configuration drift.
