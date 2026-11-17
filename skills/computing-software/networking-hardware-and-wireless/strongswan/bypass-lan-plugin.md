---
id: computing-software.networking-hardware-and-wireless.strongswan.bypass-lan-plugin
name: bypass-lan-plugin
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, bypass-lan, local-network, passthrough, split-tunnel]
level: practitioner
status: docs-checked
description: "Reach local printers and NAS while a strongSwan full tunnel is up: the bypass-lan plugin installs passthrough policies for local subnets; interfaces_use and interfaces_ignore."
sources:
  - https://docs.strongswan.org/docs/latest/plugins/bypass-lan.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bypass lan plugin
For mobile hosts that join different networks while connected to a VPN covering everything (remote traffic selector 0.0.0.0/0), the bypass-lan plugin automatically installs passthrough (bypass) policies for locally attached subnets, so local devices such as printers or a NAS stay reachable.

It is disabled by default; build with `--enable-bypass-lan`.

**Behaviour.** At start it enumerates enabled interfaces and installs bypass policies for the subnets attached directly to them. Whenever interfaces, addresses or routes change, it enumerates again and adds or removes policies as needed.

**Route-based VPNs.** The default behaviour is incompatible with route-based VPNs, so disable the plugin or restrict the interfaces.

**Options** in `charon.plugins.bypass-lan` (all interfaces are considered by default):
- `interfaces_use`: comma-separated interfaces whose connected subnets are considered; all others are ignored.
- `interfaces_ignore`: comma-separated interfaces whose subnets are ignored. Has no effect if `interfaces_use` is set.

## Checked
2026-11-04. Confirmed against the strongSwan bypass-lan plugin page: purpose, disabled by default, --enable-bypass-lan, behaviour, route-based VPN incompatibility, interfaces_use and interfaces_ignore. Nothing removed.

Method: documentation only; no commands were run.
