---
id: computing-software.systems-network-administration.virtualisation.esxi-hardening-security-configuration-guide
name: esxi-hardening-security-configuration-guide
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-hardening, security-configuration-guide, vsphere-security, esxi-firewall, secure-boot, execinstalledonly, account-lockout, disa-stig, vmware, esxi, vsphere]
level: advanced
status: docs-checked
description: "Harden ESXi with the vSphere Security Configuration Guide: shell/SSH off, firewall allow-lists, lockout, execInstalledOnly, Secure Boot/TPM, syslog, scripted checks."
sources:
  - https://github.com/vmware/vcf-security-and-compliance-guidelines
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security/securing-esxi-hosts.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security/securing-esxi-hosts/using-the-esxi-shell.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESXi hardening with the Security Configuration Guide

**Goal:** hosts configured to the vendor baseline (SCG, or DISA STIG where required),
verified by script, with documented exceptions.

## High-value controls
| Control | Setting / command |
|---|---|
| Shell and SSH stopped, policy off | ESXi Shell and SSH are deactivated by default; activate for troubleshooting only, and set availability/idle timeouts so a forgotten enable closes itself |
| Lockdown mode | Normal, with a documented exception user list |
| Firewall allow-lists | `esxcli network firewall ruleset set -r sshServer -a false` then `allowedip add -r sshServer -i <mgmt-net>` (same for NTP, syslog, CIM as needed) |
| Account lockout and password policy | advanced settings per the Security Configuration Guide |
| Only signed code | keep the execInstalledOnly runtime option on (on by default; the security guide documents deactivating it as an exception) |
| Secure Boot + TPM 2.0 | UEFI Secure Boot on; host attestation shows in vCenter |
| Remote logging | `esxcli system syslog config set --loghost <siem>` to central SIEM, persistent log dir |
| NTP/PTP | Two or more sources, time drift alarms |
| MOB disabled | per the Security Configuration Guide |
| TLS | TLS profiles via `esxcli system tls server set` (COMPATIBLE default, NIST_2024 available) |
| BPDU filter / no forged transmits | advanced settings per the Security Configuration Guide; vSwitch security Reject |

## Automate checks
Broadcom publishes SCG spreadsheets plus PowerCLI audit and remediation scripts in the
`vcf-security-and-compliance-guidelines` repo. Pattern:
```powershell
Get-VMHost | Get-AdvancedSetting -Name <scg-setting> | Select Entity, Name, Value
```
Put the desired values into the host profile so remediation and new hosts inherit them.

## Gotchas
- execInstalledOnly blocks unsigned third-party tools (old agents); test before enforcing.
- Strict lockdown + lost vCenter = no management path; keep normal lockdown with
  exception users unless policy demands strict and you have a tested recovery.
- Firewall allow-lists that omit the vCenter or backup proxy IPs break integrations.

## Verify
The audit script reports compliant for every control (or a signed-off exception);
vCenter shows host TPM attestation "Passed"; a test SSH from outside the allowed range fails.

## Checked
2026-10-31: Confirmed the ESXi Shell/SSH default-off and troubleshooting-only guidance, the
availability/idle timeout settings, UEFI Secure Boot, TPM, execInstalledOnly and Envoy on
port 443 against the vSphere 8.0 "Securing ESXi Hosts" and "Using the ESXi Shell" pages;
the esxcli firewall ruleset and syslog/tls server commands against the ESXCLI reference;
the SCG repository (baselines, audit and remediation scripts) against the official Broadcom
github.com/vmware/vcf-security-and-compliance-guidelines page. Replaced exact SCG setting
names and values (spreadsheet content, not fetchable) with pointers to the guide.
Method: documentation only; no commands were run.
