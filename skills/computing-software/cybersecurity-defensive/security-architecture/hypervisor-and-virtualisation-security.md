---
id: computing-software.cybersecurity-defensive.security-architecture.hypervisor-and-virtualisation-security
name: hypervisor-and-virtualisation-security
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [security-architecture, hypervisor-security, esxi-hardening, vcenter, hyper-v, vm-escape, management-plane, ransomware-esxi]
level: advanced
status: draft
description: "Secure the virtualisation layer: isolated ESXi/vCenter management, AD join risks, lockdown mode, execInstalledOnly, patching, and why ransomware targets hypervisors."
sources: ["https://core.vmware.com/vsphere-security-configuration-guide", "https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/plan-hyper-v-security-in-windows-server", "https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-061a"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hypervisor and virtualisation security

Compromising the hypervisor or its management plane compromises every VM: ransomware groups
encrypt datastores directly from ESXi shells, bypassing guest EDR.

## Management plane isolation
- ESXi management (vmk0), vCenter, iDRAC/iLO, and vMotion/storage networks on dedicated VLANs reachable
  only from admin jump hosts/PAWs; never from user or server networks.
- vCenter is Tier 0: whoever controls it controls DCs running on it.

## Identity
- Avoid joining ESXi hosts to the production AD domain: the "ESX Admins" group default (CVE-2024-37085)
  let any domain user who can create that group get full admin. If joined, change
  `Config.HostAgent.plugins.hostsvc.esxAdminsGroup` and patch.
- vCenter SSO: separate admin accounts, MFA via identity federation, least-privilege roles.
- Local root passwords unique per host, vaulted.

## ESXi hardening (vSphere Security Configuration Guide)
- **Lockdown mode** (normal or strict) so hosts are managed only via vCenter; exception users minimal.
- Disable SSH and ESXi Shell except during maintenance (with timeouts `UserVars.ESXiShellTimeOut`).
- `VMkernel.Boot.execInstalledOnly = TRUE` and UEFI Secure Boot + TPM: only signed VIBs run, blocking
  dropped ransomware binaries; enforcement with `esxcli system settings encryption set --require-exec-installed-only=T`.
- Acceptance level VMwareAccepted/PartnerSupported (no CommunitySupported VIBs).
- Firewall rules restricting management services to admin IPs.
- Syslog to the SIEM (`Syslog.global.logHost`), persistent scratch, NTP.

## Hyper-V
- Hosts as Server Core, in a separate management forest or at least Tier 0 treatment.
- Shielded VMs and Host Guardian Service for sensitive workloads; VBS on hosts.
- Restrict Hyper-V Administrators group.

## Patching
Hypervisor vulnerabilities (OpenSLP, VMX escapes, vCenter RCEs) are actively exploited; disable
unused services (`/etc/init.d/slpd stop` + chkconfig off) and patch on a short cycle.

## Backups
Backup infrastructure must not depend on vCenter credentials that ransomware will have; immutable copies.

## Gotchas
- Monitoring coverage: guest EDR sees nothing of hypervisor activity; collect ESXi logs (shell
  commands in `shell.log`, `hostd.log`) and alert on SSH enablement.
- Snapshot-based backups expose full disk images to backup operators.

## Verify
Quarterly: lockdown mode on, SSH disabled, execInstalledOnly enforced on all hosts (PowerCLI report),
management VLAN unreachable from a user subnet, ESXi logs arriving in the SIEM.
