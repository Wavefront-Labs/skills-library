---
id: computing-software.networking-hardware-and-wireless.strongswan.vti-devices-and-marks
name: vti-devices-and-marks
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, vti, mark-in, mark-out, route-based-vpn, install-routes]
level: advanced
status: docs-checked
description: "Use Linux VTI devices with strongSwan: creating them with ip tunnel, matching marks with mark_in and mark_out, disabling charon route installation and the disable_policy sysctl."
sources:
  - https://docs.strongswan.org/docs/latest/features/routeBasedVpn.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vti devices and marks
VTI devices wrap existing IPsec policies: packets must be routed to the device and still match established policies. Negotiating `0.0.0.0/0` selectors on both ends tunnels anything routed through the device. Marks keep other packets from matching those broad policies: only packets carrying the mark match. XFRM interfaces are the better option on kernels 4.19 and newer.

```
ip tunnel add vti0 local 192.168.0.1 remote 192.168.0.2 mode vti key 42
sysctl -w net.ipv4.conf.vti0.disable_policy=1
ip link set vti0 up
ip route add 10.1.0.0/16 dev vti0
```

The `key` must match the connection mark; `ikey` and `okey` set different marks for in- and outbound traffic. Setting `disable_policy` avoids duplicate policy lookups. Names starting with `vti` are treated specially by `ip` (statistics are not shown by name). Remove with `ip tunnel del <name>`. IPv6 works too.

**Configuration:**
1. Disable route installation in strongswan.conf: `charon.install_routes = 0`.
2. Configure a regular site-to-site connection with `local_ts = 0.0.0.0/0` and `remote_ts = 0.0.0.0/0`, or specific subnets. Other packets routed to the device are rejected with an ICMP error.
3. Set `mark_in` and `mark_out` in swanctl.conf. After applying the optional mask (default `0xffffffff`) to the device mark, the value must match the configured mark.

## Checked
2026-11-04. Confirmed against the VTI Devices section of the Route-based VPN page. Removed the mark_in_sa and %unique remarks, which are not on that page.

Method: documentation only; no commands were run.
