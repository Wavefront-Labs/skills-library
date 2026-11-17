---
id: computing-software.networking-hardware-and-wireless.strongswan.child-sa-traffic-selectors-and-modes
name: child-sa-traffic-selectors-and-modes
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, child-sa, traffic-selectors, ipsec-mode, local-ts]
level: practitioner
status: docs-checked
description: "Define strongSwan CHILD_SA traffic selectors with protocol and port syntax, choose tunnel, transport, beet or shunt modes, and set updown, policies, reqid and priority."
sources:
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlConf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# child sa traffic selectors and modes
`local_ts` and `remote_ts` are comma-separated CIDR subnets, each with an optional `[proto/port]` selector. The default is `dynamic`, replaced by the tunnel outer address or the negotiated virtual IP. Inside the brackets give a numeric or getservent(3) protocol name, then optionally `/port` (numeric, service name or `opaque`); ranges work, but kernel-netlink only handles ranges mappable to a bit mask. For `icmp` and `ipv6-icmp` a port below 256 is the type, otherwise type is the high 8 bits and code the low 8 bits.

IKEv1 interprets only the first selector (unless the unity plugin is used); define several children for several pairs, and use identical selectors on both sides to avoid narrowing problems.

`mode` (default `tunnel`): `transport`, `transport_proxy`, `beet`, `iptfs`, or `pass` and `drop` to install shunt policies. Transport, iptfs and beet are negotiated; tunnel is used if the preferred mode is unavailable.

Other options: `esp_proposals` / `ah_proposals` (ESP proposed when no AH is given, `default` adds safe algorithms, `esn`/`noesn`), `updown` script, `hostaccess`, `policies` (set no to skip installing IPsec policies), `policies_fwd_out`, `ipcomp`, `inactivity` timeout, fixed `reqid`, fixed `priority` for policies (useful for high-priority drop policies), `interface` to restrict outbound policies.

## Checked
2026-11-04. Confirmed against the strongSwan swanctl.conf reference (children: local_ts, remote_ts, mode, policies, policies_fwd_out, inactivity, reqid, priority, interface, updown, hostaccess, esp_proposals, ah_proposals, ipcomp). Nothing removed.

Method: documentation only; no commands were run.
