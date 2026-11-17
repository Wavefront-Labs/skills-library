---
id: computing-software.networking-hardware-and-wireless.strongswan.attr-plugin-ike-attributes
name: attr-plugin-ike-attributes
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, attr-plugin, dns, config-payload, modeconfig]
level: practitioner
status: docs-checked
description: "Push DNS, WINS, subnet and other IKE configuration attributes to peers from strongswan.conf with the attr plugin, including IPv4 and IPv6 attribute keys."
sources:
  - https://docs.strongswan.org/docs/latest/plugins/attr.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# attr plugin ike attributes
The attr plugin is enabled by default (`--disable-attr` removes it). It serves attributes set in `charon.plugins.attr` in strongswan.conf through IKEv2 CP configuration payloads or IKEv1 Mode Config. They are only assigned to peers that request a virtual IP address. Multiple values go in a comma-separated list; the IPv4 or IPv6 attribute type follows the address family of the value.

IPv4 keys with attribute type and code:

| Key | Type | Code |
|---|---|---|
| address | INTERNAL_IP4_ADDRESS | 1 |
| netmask | INTERNAL_IP4_NETMASK | 2 |
| dns | INTERNAL_IP4_DNS | 3 |
| nbns | INTERNAL_IP4_NBNS | 4 |
| dhcp | INTERNAL_IP4_DHCP | 6 |
| subnet | INTERNAL_IP4_SUBNET | 13 |
| p-cscf | P_CSCF_IP4_ADDRESS | 20 (IKEv2 only) |

IPv6 keys: address (INTERNAL_IP6_ADDRESS, 8), netmask (9, IKEv1 only), dns (10), nbns (11, IKEv1 only), dhcp (12), and subnet.

`subnet` carries protected sub-networks in CIDR notation. It is usually ignored in favour of `local_ts`, but macOS clients use it for routes. `netmask` is similar to subnet but bound to the internal address.

The page points to the IANA website for the complete list of IKEv2 configuration payload attributes.

## Checked
2026-11-04. Confirmed against the attr plugin page: `--disable-attr`, behaviour, the IPv4 and IPv6 attribute tables with codes and IKE-version notes, and the subnet and netmask descriptions. Removed the closing pointer to pool and RADIUS attributes (not on the page).

Method: documentation only; no commands were run.
