---
id: computing-software.networking-hardware-and-wireless.strongswan.virtual-ip-requests-and-assignment
name: virtual-ip-requests-and-assignment
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, virtual-ip, vips, config-payloads, external-pools, install-virtual-ip]
level: practitioner
status: docs-checked
description: "Request and hand out strongSwan virtual IPs: vips on the initiator, pools on the responder, dynamic selectors, dual-stack requests, DNS via the resolve plugin and source routes."
sources:
  - https://docs.strongswan.org/docs/latest/features/vip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# virtual ip requests and assignment
The initiator asks the responder for an inner tunnel address. IKEv1 uses ModeConfig; IKEv2 uses CP configuration payloads. strongSwan implements the case where the initiator requests and the responder assigns one or several IPv4 and/or IPv6 addresses from pools.

**Initiator.** `connections.<conn>.vips = 0.0.0.0` (or `::`) requests any address; a specific one can be named, but the responder may return a different one or none. List both for dual stack: `vips = 0.0.0.0, ::`. For a static virtual IP without payloads, add it to any local interface (even `lo`) and reference it in `local_ts`; putting it in `vips` would not install it. Leave `local_ts` at `dynamic` so it is replaced by the assigned address.

**Responder.** Leave `remote_ts` at `dynamic` (otherwise every client gets the same selector, causing conflicting policies). Define pools and reference them with `pools = <name>`: a single address (`addrs = 10.3.0.5`), a CIDR pool (`10.3.0.0/24`) or a range (`10.3.0.1-10.3.0.100`), and the same for IPv6. A name not found in `pools` queries plugins for an external pool, such as the dhcp or eap-radius plugins.

**DNS.** Clients cannot request DNS servers in swanctl.conf; servers received in CP or ModeConfig payloads are handled by the resolve plugin (via resolvconf(8) or writing resolv.conf).

**Linux behaviour.** Virtual IPs go on the outbound interface unless `charon.install_virtual_ip_on` is set. Source routes in `charon.routing_table` (or `--with-routing-table`) force use of the virtual IP toward the remote selectors.

## Checked
2026-11-04. Confirmed against the strongSwan Virtual IP Addresses page: vips on the initiator, dynamic selectors, static virtual IP on lo, dual stack, responder pools, external pools, resolve plugin, install_virtual_ip_on and routing_table. Nothing removed.

Method: documentation only; no commands were run.
