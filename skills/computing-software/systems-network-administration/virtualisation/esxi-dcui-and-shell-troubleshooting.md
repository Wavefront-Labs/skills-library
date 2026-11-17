---
id: computing-software.systems-network-administration.virtualisation.esxi-dcui-and-shell-troubleshooting
name: esxi-dcui-and-shell-troubleshooting
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [dcui, esxi-shell, esxi-host-setup, management-network, restart-management-agents, ssh, vmware, esxi, vsphere, troubleshooting]
level: practitioner
status: draft
description: "Use the ESXi DCUI and shell: fix the management network, test it, restart management agents, network restore options, and safe shell/SSH timeouts."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esxi-installation-and-setup-8-0.html
  - https://knowledge.broadcom.com/external/article?legacyId=1003490
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ESXi DCUI and shell for host setup and recovery

**Goal:** get a host's management network right from the console, and recover a host
that vCenter has lost without rebooting its VMs.

## DCUI tasks (F2 at the console, iLO/iDRAC remote console)
- **Configure Management Network:** pick the vmnic(s) for vmk0, VLAN ID, IPv4/IPv6,
  DNS and hostname. Choose at least two uplinks on different physical switches.
- **Test Management Network:** pings gateway, DNS servers and resolves the hostname.
  A failure on name resolution here is the usual reason vCenter add-host fails.
- **Restart Management Network:** renews vmk0 without a reboot.
- **Network Restore Options:** *Restore Standard Switch* recreates vSwitch0/vmk0 when a
  vDS change cut the host off (the commonest self-inflicted outage). *Restore Network
  Settings* resets everything to defaults.
- **Restart Management Agents:** restarts hostd/vpxa. VMs keep running. Use when the
  host shows "not responding" but VMs are fine.
- **Troubleshooting Options:** enable ESXi Shell/SSH and set their timeouts.

## Shell equivalents
```sh
esxcli network ip interface ipv4 get
esxcli network ip interface ipv4 set -i vmk0 -t static -I <IP> -N <MASK> -g <GW>
esxcli network vswitch standard portgroup set -p "Management Network" -v <VLAN>
vmkping -I vmk0 <gateway>
/etc/init.d/hostd restart ; /etc/init.d/vpxa restart     # or: services.sh restart (heavier)
esxcli system settings advanced set -o /UserVars/ESXiShellInteractiveTimeOut -i 900
esxcli system settings advanced set -o /UserVars/ESXiShellTimeOut -i 3600
```
`services.sh restart` also restarts other agents (and can briefly drop HA/vSAN agents);
prefer restarting hostd and vpxa individually.

## Gotchas
- Lockdown mode (normal) disables DCUI login except for exception users; strict mode
  stops the DCUI service entirely, so keep a documented recovery path.
- The DCUI root password is the local root password, not an SSO account.
- Leaving SSH on raises a host warning and is a hardening finding; turn it off after use
  (`vim-cmd hostsvc/disable_ssh`).

## Verify
Test Management Network shows all OK; `vmkping` to the vCenter IP succeeds; the host
reconnects in vCenter and `/var/log/vpxa.log` shows no new errors.
