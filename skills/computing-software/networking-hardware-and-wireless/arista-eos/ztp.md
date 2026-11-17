---
id: computing-software.networking-hardware-and-wireless.arista-eos.ztp
name: ztp
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, ztp, zero-touch-provisioning, dhcp-option-67, bootstrap]
level: practitioner
status: draft
description: "Bootstrap new EOS switches with ZTP using DHCP options for bootstrap script or startup-config."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Zero Touch Provisioning
Goal: bring up a factory-default switch with no console config.

```
# dhcpd.conf excerpt (ISC DHCP)
subnet 198.51.100.0 netmask 255.255.255.0 {
  range 198.51.100.50 198.51.100.99;
  option bootfile-name "http://192.0.2.70/ztp/bootstrap";
}
```

```
# bootstrap script (served over http)
#!/usr/bin/env python
# fetches config for this serial number and saves startup-config
```

```
switch# zerotouch cancel
switch# zerotouch disable
switch# show zerotouch
```

- A switch in ZTP mode DHCPs on Management1, downloads the bootstrap (option 67), and runs it.
- The bootstrap can point the device at CloudVision (TerminAttr) or an AVD-generated config.
- `write erase` + `reload` puts a device back in ZTP.

Gotcha: ZTP only runs when there is no startup-config. A cached partial config prevents re-run; use `zerotouch cancel` or `write erase` as required.

Operational tip: serve the bootstrap over HTTPS where supported, verify the config against the serial number, and keep the ZTP DHCP scope on an isolated management VLAN so rogue servers cannot hijack provisioning.

## Verify
- `show zerotouch` shows the mode and result; the device appears in CloudVision inventory.
