---
id: computing-software.digital-forensics-incident-response.incident-response-process.esxi-and-hypervisor-ransomware-response
name: esxi-and-hypervisor-ransomware-response
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [esxi-ransomware, ransomware, vmware-esxi, incident-recovery, dfir]
level: advanced
status: draft
description: "Respond to ransomware that encrypts ESXi datastores: containment, log and evidence collection on the host, encryption scoping, vCenter compromise and rebuild."
sources: ["https://docs.vmware.com/en/VMware-vSphere/8.0/vsphere-monitoring-performance/GUID-832A2618-6B11-4A28-9672-93296DA931D0.html", "https://www.cisa.gov/stopransomware/ransomware-guide"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESXi and hypervisor ransomware response

**Goal:** many ransomware families ship Linux/ESXi encryptors that encrypt `.vmdk`, `.vmx`,
`.vmsn` on datastores, taking down hundreds of VMs at once.

## Contain
- Isolate ESXi management interfaces (vmk0) from the network except the IR jump host; disable SSH
  and ESXi Shell if attacker enabled them.
- Check vCenter: attackers usually come in via vCenter or AD-joined ESXi ("ESX Admins" group
  abuse); treat vCenter as compromised until proven otherwise.
- Do not reboot hosts: encryptors and logs live in ramdisk on ESXi (`/tmp`, `/var/log` is partly volatile).

## Collect from the host (via SSH or vm-support)
- `vm-support` bundle (includes logs); copy `/var/log/` and `/scratch/log/` immediately: `shell.log`
  (commands typed), `hostd.log`, `auth.log`, `vobd.log`, `vmkernel.log`.
- Encryptor binary and ransom note (often in `/tmp` or datastore root).
- `esxcli network ip connection list`, `esxcli system account list`, `esxcli software vib list` (malicious VIBs = persistence).
- vCenter: `vpxd.log`, events/tasks export, SSO logs.

## Scope encryption
- Per datastore: list files and extensions; check whether flat VMDKs were fully or partially
  encrypted (many encryptors encrypt only every Nth MB; `-flat.vmdk` data may be recoverable).
- ESXiArgs-style cases: the `.vmx`/descriptor was encrypted but flat VMDK intact - CISA recovery script rebuilds config.

## Recover
- Rebuild ESXi hosts from installation media (never trust a compromised host), patch, remove AD
  join or tighten "ESX Admins", lockdown mode, disable SSH.
- Restore VMs from backups stored off the encrypted datastores; verify backup console was not compromised.

## Gotchas
- Logs in `/var/log` are overwritten on reboot unless a persistent scratch location or syslog forwarding exists.
- Snapshots on the same datastore are encrypted too.

## Verify
Rebuilt hosts have no unknown VIBs, SSH disabled, syslog forwarding on, and vCenter credentials rotated.
