---
id: computing-software.systems-network-administration.virtualisation.vcsa-vami-network-time-syslog
name: vcsa-vami-network-time-syslog
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vami-network-settings, vcsa-appliance-config, vcsa, vami, vcenter-server-appliance, vmware, vcenter]
level: practitioner
status: docs-checked
description: "Configure the vCenter appliance through the VAMI on port 5480: hostname and network, NTP or host time sync, syslog forwarding, access settings and their CLI equivalents."
sources:
  - https://knowledge.broadcom.com/external/article/313094
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# VCSA appliance management (VAMI) settings

**Goal:** a vCenter appliance with correct DNS, time and log forwarding, set the supported way.

## Access
`https://<vcsa-fqdn>:5480`, log in as `root` (not SSO). Summary shows health of CPU, memory, database, storage, swap and services.

## Networking
- Networking -> Edit: DNS servers, IPv4/IPv6, gateway. Changing the IP is allowed; changing the **FQDN/PNID** is disruptive (certificate regeneration, re-registration of ELM/plugins). Plan it.
- Proxy settings are also here (needed for online depots).

## Time
Time -> Time synchronization: *NTP* (list servers) or *Host* (sync with the ESXi host it runs on). Choose NTP and keep hosts on the same NTP sources; SSO tokens fail with significant clock skew.

## Syslog
Syslog -> Configure: remote syslog targets, protocol TLS/TCP/UDP, port. Use TLS 6514 or TCP 514 to a SIEM.

## Access
Access -> SSH login, DCLI, console CLI, BASH shell (timed). Keep SSH disabled except during troubleshooting.

## CLI equivalents (appliance shell)
The appliance REST API (and the `appliance_ntp` module of the `vmware.vmware_rest`
Ansible collection) can manage NTP and other appliance settings; see the vSphere
Automation API documentation. When the UI is down, appliance network changes can be made
from the console shell (see the vCenter Appliance documentation).

## Gotchas
- VAMI not loading: check the `applmgmt` service status with `service-control` and restart it.
- Root password expired: VAMI login fails; reset from the console (see root password recovery).

## Verify
`timedatectl` and `chronyc sources` show sync, `nslookup` of the FQDN resolves forward and reverse, test events arrive in the SIEM.

## Checked
2026-10-31: VAMI port 5480 confirmed in the vSphere Automation API overview; NTP/time-sync settings and the `appliance_ntp` module confirmed via the vmware.vmware_rest collection index and the vCenter Configuration guide's SNMP/settings TOC; `service-control` confirmed as a VCSA command in KB 377237. Removed unconfirmed specifics: the appliance-shell command names, the vami_config_net path, the 5-minute skew figure, the three-target syslog limit and the 6.7U3+ PNID-change version claim.
Method: documentation only; no commands were run.
