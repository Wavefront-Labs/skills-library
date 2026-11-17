---
id: computing-software.systems-network-administration.virtualisation.esxi-firewall-rulesets
name: esxi-firewall-rulesets
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-firewall-ruleset, esxi-firewall, esxcli, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Manage the ESXi host firewall: enable or disable rulesets, restrict services to allowed IP ranges, and avoid locking out vCenter or management access."
sources:
  - https://developer.broadcom.com/xapis/esxcli-command-reference/latest/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ESXi firewall rulesets

**Goal:** expose only required services on each host, from known networks only.

## Inspect
```bash
esxcli network firewall get                       # enabled, default action
esxcli network firewall ruleset list              # name, enabled
esxcli network firewall ruleset rule list -r sshServer
esxcli network firewall ruleset allowedip list
```

## Enable/disable and restrict
```bash
esxcli network firewall ruleset set -r sshServer -e true
esxcli network firewall ruleset set -r sshServer --allowed-all false
esxcli network firewall ruleset allowedip add -r sshServer -i 10.10.50.0/24
esxcli network firewall refresh
```
PowerCLI across a cluster:
```powershell
Get-Cluster CL1 | Get-VMHost | Get-VMHostFirewallException -Name 'SSH Server' | Set-VMHostFirewallException -Enabled:$false
```
IP restrictions per ruleset are set via `Get-EsxCli -V2` (`network.firewall.ruleset.allowedip.add.Invoke(@{rulesetid='sshServer';ipaddress='10.10.50.0/24'})`).

## Rules that must stay reachable from vCenter
the vSphere Client, HA heartbeat, vMotion, vSphere Replication, provisioning/NFC and CIM monitoring rulesets. Restricting these without including vCenter and backup proxies disconnects the host or breaks backups.

## Custom rules
Files under `/etc/vmware/firewall/` are not persistent and ESXi 8 blocks ad-hoc edits; ship custom rulesets in a signed VIB from the vendor, or use built-in rulesets.

## Gotchas
- Service running but ruleset closed (or vice versa) is common after hardening scripts; check both `vim-cmd hostsvc/...` service state and the ruleset.
- Default action is DROP; leaving the firewall disabled for troubleshooting is a finding in audits.
- Host profiles can enforce rulesets; manual changes drift and get remediated back.

## Verify
`nc -zv <host> 22` succeeds from the allowed subnet and fails from elsewhere; vCenter still shows the host connected.

## Checked
2026-10-31: Confirmed `esxcli network firewall get/ruleset list/rule list/allowedip list`,
`ruleset set` (--ruleset-id, --enabled, --allowed-all) and `allowedip add`, plus the
`network firewall refresh` command, against the ESXCLI network reference page. Replaced
the named management rulesets and port numbers with service descriptions (names/ports
not on the fetched pages).
Method: documentation only; no commands were run.
