---
id: computing-software.systems-network-administration.virtualisation.esxi-ssh-and-shell-timeouts
name: esxi-ssh-and-shell-timeouts
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-ssh, shell-timeout, esxi-hardening, vsphere-security, esxi-shell, powercli, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Control ESXi SSH and ESXi Shell: enable only on demand, ESXiShellTimeOut and ESXiShellInteractiveTimeOut, suppress warnings properly, and audit across hosts."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security/securing-esxi-hosts/using-the-esxi-shell.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESXi SSH and Shell services

Baseline (vSphere Security Configuration Guide): **SSH and ESXi Shell stopped, startup
policy "Start and stop manually"**, timeouts set so a forgotten enable closes itself.

## Timeouts
Two timeouts exist for the ESXi Shell and SSH, both set from the vSphere Client host
settings or the DCUI: an **availability timeout** (the service stops itself after that
many minutes) and an **idle timeout** (idle sessions are logged out). Set both so a
forgotten enable closes itself. Keep the "SSH enabled" warning visible rather than
suppressing it.

## PowerCLI: enable for a job, then close
```powershell
$h = Get-VMHost esx01*
Get-VMHostService -VMHost $h | ? Key -eq TSM-SSH | Start-VMHostService
# ... work ...
Get-VMHostService -VMHost $h | ? Key -eq TSM-SSH | Stop-VMHostService -Confirm:$false

# audit for running SSH/shell services
Get-VMHost | Get-VMHostService | ? { $_.Key -in 'TSM-SSH','TSM' -and $_.Running } | Select VMHost, Key, Policy
```
Enable or disable SSH from the Host Client or the DCUI.

## Hardening extras
- Restrict who can SSH with the ESXi firewall allow-list
  (`esxcli network firewall ruleset set -r <ssh-ruleset> --allowed-all false` then
  `esxcli network firewall ruleset allowedip add -r <ssh-ruleset> -i <mgmt-net>`).
- Key-based auth is disabled in lockdown mode.
- 8.0: `esxcli system ssh server config set` exposes sshd options (ciphers, MACs).
- Lockdown mode strict stops SSH regardless (exception users still need the service on).

## Gotchas
- Monitoring tools that SSH to hosts every few minutes defeat the timeout; use API/CIM.
- Host profiles can re-enable SSH; check the profile's Security → Service config.

## Verify
Audit shows no running TSM-SSH outside change windows; banner warning absent only
because SSH is off.

## Checked
2026-10-31: Confirmed the ESXi Shell/SSH services (off by default, troubleshooting only,
independent of lockdown mode) and the documented availability/idle timeout settings
(vSphere Client and DCUI pages) against "Using the ESXi Shell"; `esxcli network firewall
ruleset set --allowed-all/--ruleset-id/--enabled` and `allowedip add` against the ESXCLI
network reference; `esxcli system ssh server config set/list` against the ESXCLI system
reference. Replaced the UserVars setting names and typical values with the documented
timeout names, and removed the vim-cmd hostsvc commands and the authorized_keys path.
Method: documentation only; no commands were run.
