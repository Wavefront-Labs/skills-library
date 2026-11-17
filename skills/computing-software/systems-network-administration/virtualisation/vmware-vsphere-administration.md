---
id: computing-software.systems-network-administration.virtualisation.vmware-vsphere-administration
name: vmware-vsphere-administration
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmware, vsphere, esxi, vcenter, vcsa, vami, vsphere-ha, admission-control, isolation-response, datastore-heartbeat, drs, vmotion, vds, distributed-switch, standard-switch, port-group, nic-teaming, vmkernel, vmfs, nfs-datastore, vsan, multipathing, round-robin, psp, vlcm, lifecycle-manager, maintenance-mode, lockdown-mode, rbac, vcenter-backup, esxcli, powercli, broadcom, vcf, vvf]
level: advanced
status: draft
description: "Run a vSphere cluster: HA admission control and isolation response, DRS, vDS/vmkernel layout, storage multipathing, vLCM image patching, vCenter file backup, RBAC, lockdown."
sources:
  - https://docs.vmware.com/en/VMware-vSphere/index.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere.html
  - https://developer.broadcom.com/powercli
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VMware vSphere administration — a cluster that survives a host loss and your own patching

**Goal:** configure and operate an ESXi cluster under vCenter so that a host failure
restarts VMs automatically, maintenance needs no downtime, and vCenter itself can be
rebuilt. VM templates, snapshots and vMotion prerequisites are in
`computing-software.systems-network-administration.virtualisation.vm-lifecycle-snapshots-and-migration`;
performance tuning in `...virtualisation.vm-performance-tuning`.

Licensing note: since the Broadcom acquisition, vSphere is sold as subscription bundles
(VVF/VCF) and which features (vDS, vSAN, DRS) a given SKU includes has changed more than
once. Check your entitlement before designing around a feature; this file does not track it.

## 1. Network layout (per host)
Separate traffic by VMkernel adapter and port group, on at least two physical uplinks:

| VMkernel / port group | Purpose | Notes |
|---|---|---|
| vmk0 Management | vCenter, SSH, HA heartbeats | its own VLAN |
| vmk1 vMotion | live migration | use the vMotion TCP/IP stack; ≥10 Gb/s |
| vmk2 Storage | iSCSI/NFS | jumbo frames end to end, or none at all |
| VM port groups | guest traffic | one per VLAN, tagged (VST) |

- Prefer a **vSphere Distributed Switch** for consistent config across hosts, Network
  I/O Control and LACP. Back up its config (Export Configuration) before changes.
- NIC teaming: "Route based on originating virtual port" is the safe default with no
  switch config; "IP hash" requires a static EtherChannel on the physical switch; LACP
  requires a vDS LAG. Mixing them up isolates hosts.
- MTU 9000 must match on vDS, vmk, physical switch and storage target. Test with
  `vmkping -I vmk2 -d -s 8972 <storage_ip>` (`-d` = don't fragment).

## 2. Storage
- Present the same datastores to every host in the cluster or HA/DRS cannot place VMs.
- iSCSI/FC block storage: check the array vendor's recommended Path Selection Policy;
  many recommend Round Robin (`esxcli storage nmp device set -d <naa.id> -P VMW_PSP_RR`).
  `esxcli storage core path list` shows dead paths.
- Keep datastore free space above ~20% for snapshots and swap files (rule of thumb).

## 3. vSphere HA
- **Admission control:** reserve capacity as a percentage equal to at least one host
  (N+1). With 4 hosts that is 25% CPU and memory. Without it, HA may have nowhere to
  restart VMs after a failure.
- **Host isolation response:** "Power off and restart VMs" when storage is on a separate
  network that may stay up (avoids split-brain on NFS/iSCSI); "Disabled" (leave running)
  is common when management and storage share fate. Decide; don't leave the default untested.
- Configure **datastore heartbeating** on two datastores so HA can tell an isolated host
  from a failed one. Set `das.isolationaddress` to a pingable gateway if the default
  gateway does not answer ICMP.
- Set VM restart priority (domain controllers and DNS first) and dependencies.

## 4. DRS
- Fully Automated, migration threshold at the middle setting (3) is a sensible start.
- Use VM/Host rules: anti-affinity for redundant pairs (two domain controllers, two
  load-balancer nodes) so one host loss cannot take both.
- If DRS is not licensed, maintenance mode needs manual vMotion of every VM first.

## 5. Patching with vSphere Lifecycle Manager
- Use **image-based** cluster management: one desired image (ESXi version + vendor add-on
  + firmware/drivers) applied to all hosts. Run **Check Compliance** and **Remediation
  pre-check** before remediating.
- Remediation enters each host into maintenance mode in turn; it needs DRS (or manual
  evacuation) and enough HA headroom for one host out.
- Upgrade order: vCenter first, then hosts, then VM hardware/VMware Tools. Check the
  interoperability matrix for backup software and storage plugins before upgrading vCenter.

## 6. Protect vCenter and access
- Schedule **file-based backup** in the appliance management UI (VAMI, port 5480) to
  SFTP/NFS/SMB. A VM-level snapshot of vCenter is not a supported backup.
- Use SSO groups mapped from AD/LDAP or an identity provider, with least-privilege
  custom roles; avoid daily use of `administrator@vsphere.local`.
- Enable **lockdown mode** (Normal) on hosts so they are managed only through vCenter;
  add a break-glass account to the Exception Users list.
- Disable SSH and ESXi Shell except during troubleshooting.

## 7. Useful CLI
```powershell
# PowerCLI: cluster HA/DRS state and hosts not connected
Connect-VIServer vcenter.corp.example
Get-Cluster | Select Name,HAEnabled,HAAdmissionControlEnabled,DrsEnabled,DrsAutomationLevel
Get-VMHost | Where ConnectionState -ne 'Connected'
```
```bash
esxcli network ip interface ipv4 get     # vmk addressing
esxcli system maintenanceMode set -e true
```

## Verify
- [ ] Each host: ≥2 uplinks, separate vmk for management/vMotion/storage, MTU tested with `vmkping -d`.
- [ ] HA admission control reserves ≥ one host; datastore heartbeats on two datastores.
- [ ] A host power-off test restarts its VMs elsewhere within minutes.
- [ ] Anti-affinity rules exist for every redundant VM pair.
- [ ] vLCM image compliant on all hosts; vCenter file backup ran successfully this week.
- [ ] Lockdown mode on, SSH off, no daily logins as the SSO administrator.
