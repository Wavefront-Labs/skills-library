---
id: computing-software.systems-network-administration.cisco-networking.zero-touch-provisioning-and-pnp
name: zero-touch-provisioning-and-pnp
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, zero-touch-provisioning, ztp, cisco-pnp, plug-and-play, dhcp-option-67, guestshell, day-0]
level: practitioner
status: draft
description: "Day-0 provision IOS XE devices without console: ZTP via DHCP option 67 Python script, Cisco PnP discovery (option 43, DNS, cloud redirect), and debugging failed runs."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/1712/b_1712_programmability_cg/m_1712_prog_ztp.html
  - https://www.cisco.com/c/en/us/td/docs/cloud-systems-management/network-automation-and-management/dna-center/tech_notes/b_dnac_sda_pnp_deployment.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zero-touch provisioning and PnP on IOS XE

An unconfigured IOS XE device (no startup-config) tries, in order: PnP and ZTP via DHCP on its
management/uplink ports. Which one runs depends on what the DHCP server hands back.

## ZTP: DHCP option 67 points at a Python script
ISC/Kea style (option 67 bootfile, option 150 or a URL):
```
"option-data": [ { "name": "boot-file-name", "data": "http://10.0.0.30/ztp.py" } ]
```
IOS DHCP server:
```
ip dhcp pool ZTP
 network 10.99.0.0 255.255.255.0
 default-router 10.99.0.1
 option 67 ascii http://10.99.0.30/ztp.py
```
The script runs inside Guest Shell with the `cli` module:
```python
from cli import configure, cli
configure(["hostname SW-NEW", "username admin privilege 15 secret 9 <hash>",
           "ip ssh version 2", "line vty 0 4", "transport input ssh", "login local"])
cli("write memory")
```
Typical script jobs: read serial (`cli("show version")`), fetch a per-serial config from HTTP,
upgrade the image, apply config, save.

## PnP: device finds a PnP server (Catalyst Center or other)
Discovery order: DHCP option 43 string, then DNS `pnpserver.<domain>`, then Cisco cloud
(devicehelper.cisco.com, which redirects per Smart Account).
```
ip dhcp pool PNP
 option 43 ascii "5A1N;B2;K4;I10.0.0.50;J80"
```
`5A1N` = PnP, active, IPv4, no debug; `B2` IPv4 address follows; `K4` HTTP (`K5` HTTPS); `I` server;
`J` port.

## Watching and debugging
On the device console during first boot you see `--- System Configuration Dialog ---` being
skipped and `Guestshell enabled successfully` then script output. Afterwards:
```
show pnp status
show pnp tech-support
dir flash:guest-share/        ! ztp script logs on some releases
show log | include ZTP|PNP
```

## Gotchas
- Any startup-config disables both. Run `write erase` then reload (do not save at the prompt).
- Option 43 for PnP conflicts with option 43 for AP WLC discovery on the same scope; use a separate
  provisioning VLAN/pool.
- The device needs DNS and routing to reach the script URL; option 6 and 3 matter.
- Guest Shell requires IOx; small platforms or old releases may lack it, and ZTP scripts fail
  silently if a CLI command errors. Wrap calls in try/except and log to flash.
- Mark the end of provisioning in the script (e.g. a banner) so you can tell success from a
  half-run.

## Verify
- [ ] A factory-reset device boots to the expected hostname and is reachable by SSH.
- [ ] Script log on flash shows each step completed.
