---
id: computing-software.systems-network-administration.virtualisation.esxi-ntp-ptp-time-configuration
name: esxi-ntp-ptp-time-configuration
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-ntp, esxi-ptp, esxi-host-setup, time-sync, esxcli, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Set ESXi host time with NTP or PTP, DNS and hostname after install via esxcli or PowerCLI, and verify sync before joining vCenter, vSAN or AD."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-and-host-management-8-0.html
  - https://developer.broadcom.com/xapis/esxcli-command-reference/latest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESXi time (NTP/PTP), DNS and hostname

Bad time breaks AD join (Kerberos clock-skew tolerance), SSO token validation, vSAN, HA logs
correlation and certificate validity. Do this before adding the host to vCenter.

## DNS and hostname
```sh
esxcli system hostname set --host=esx01 --domain=corp.example
esxcli network ip dns server add --server=10.0.0.10
esxcli network ip dns search add --domain=corp.example
```
Forward **and reverse** records must exist before adding to vCenter (vCenter uses FQDN in
certificates).

## NTP (esxcli)
```sh
esxcli system ntp set --server=ntp1.corp.example --server=ntp2.corp.example --enabled=true
esxcli system ntp get
esxcli system ntp test          # queries the servers and reports offset
esxcli network firewall ruleset set -r ntpClient -e true
```
PowerCLI fleet-wide:
```powershell
Get-VMHost | Add-VMHostNtpServer -NtpServer ntp1.corp.example,ntp2.corp.example
Get-VMHost | Get-VMHostService | ? Key -eq ntpd | Set-VMHostService -Policy On | Start-VMHostService
```
Use at least 3 sources (or 2 reliable internal ones); ESXi does not step large offsets
smoothly, so fix the hardware clock in BIOS first if it is hours out.

## PTP
For sub-millisecond requirements (finance, telco). Requires a PTP-capable network and a
VMkernel adapter or PCI-passthrough NIC: `esxcli system ptp set` (or Host → Configure →
Time Configuration). PTP can fall back to NTP on failure (non-revertive).

## Gotchas
- Guest time: VMware Tools periodic sync is off by default; guests should use NTP/AD. Tools
  still syncs on vMotion/snapshot resume.
- Host profiles can overwrite NTP settings; fix the profile, not just the host.
- vCenter appliance time is separate (VAMI → Time); keep both on the same sources.

## Verify
`esxcli system ntp get` shows Enabled true and servers; `esxcli hardware clock get` vs
`date -u` agree; vSAN Skyline "Time is synchronized across hosts and VC" check is green.

## Checked
2026-10-31: Confirmed `esxcli system hostname set`, `esxcli network ip dns server add`,
`esxcli network ip dns search add`, `esxcli system ntp set/get/test` and the PTP commands
(`esxcli system ptp get/set/test/stats get`, vmknic or pcipassthru device types, NTP
fallback flag) against the ESXCLI system reference page. Removed the 7.0U1+/7.0U3+/8.0
version notes and the Kerberos 5-minute figure.
Method: documentation only; no commands were run.
