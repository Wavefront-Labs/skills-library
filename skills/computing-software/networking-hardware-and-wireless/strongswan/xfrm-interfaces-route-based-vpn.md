---
id: computing-software.networking-hardware-and-wireless.strongswan.xfrm-interfaces-route-based-vpn
name: xfrm-interfaces-route-based-vpn
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, route-based-vpn, xfrm-interface, if-id, interface-id]
level: advanced
status: docs-checked
description: "Build route-based VPNs on Linux with strongSwan XFRM interfaces: creating them with ip link or xfrmi, if_id_in and if_id_out, %unique ids, routes, sharing, VRFs and namespaces."
sources:
  - https://docs.strongswan.org/docs/latest/features/routeBasedVpn.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# xfrm interfaces route based vpn
Route-based VPNs let routing decide what is tunneled, with easy plaintext capture and a settable MTU. XFRM interfaces need Linux 4.19 and iproute2 5.1.0 or newer (older kernels can use VTI devices). They need no endpoint addresses, support IPv4 and IPv6 on one interface, non-tunnel modes, and a shared interface for several peers. An XFRM interface ID in the policy selector links policies and SAs to the interface, so duplicate 0.0.0.0/0 selectors work when the IDs differ.

```
ip link add ipsec0 type xfrm if_id 42
# or if iproute2 cannot: /usr/local/libexec/ipsec/xfrmi --name ipsec0 --id 42
ip link set ipsec0 up
ip route add 10.1.0.0/16 dev ipsec0
```


**swanctl.conf.** Configure the connection normally, optionally with `0.0.0.0/0` and `::/0` selectors. Set `if_id_in` and `if_id_out` (same value for one interface; `%unique` for a unique ID per CHILD_SA; distinct values or `%unique-dir` for separate in/out interfaces; set only one for one direction). On the connection level, children inherit them; unique values are then per IKE_SA.

With `charon.plugins.kernel-netlink.install_routes_xfrmi` enabled, routes are installed via the interface identified by `if_id_out` if it exists. Avoid routing IKE/ESP into the interface: mark IKE with `charon.plugins.socket-default.fwmark`, mark ESP with `<child>.set_mark_out`, exclude with `charon.plugins.kernel-netlink.fwmark=!<mark>`, or add a throw route in table 220.

For Netfilter, match the interface name instead of the IPsec policy match.

## Checked
2026-11-04. Confirmed against the Route-based VPN page: kernel and iproute2 requirements, the ip link and xfrmi commands, if_id_in and if_id_out semantics, install_routes_xfrmi, the routing loop options, and the Netfilter note.

Method: documentation only; no commands were run.
