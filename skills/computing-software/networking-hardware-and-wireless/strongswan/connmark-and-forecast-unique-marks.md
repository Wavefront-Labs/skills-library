---
id: computing-software.networking-hardware-and-wireless.strongswan.connmark-and-forecast-unique-marks
name: connmark-and-forecast-unique-marks
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, connmark, forecast, unique-mark, multicast, transport-mode]
level: advanced
status: docs-checked
description: "Use mark_in and mark_out = %unique with the strongSwan connmark plugin for transport-mode clients behind NAT and the forecast plugin for multicast and broadcast forwarding."
sources:
  - https://docs.strongswan.org/docs/latest/plugins/connmark.html
  - https://docs.strongswan.org/docs/latest/plugins/forecast.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# connmark and forecast unique marks
Both plugins are disabled by default, need iptables development headers to build, and apply to SAs that use a unique Netfilter mark: `mark_in = %unique` and `mark_out = %unique` on the child, so each negotiated SA is distinguishable. They configure the needed Netfilter rules themselves.

**connmark** (`--enable-connmark`). Transport-mode only. Two transport-mode clients behind one NAT have identical IPsec policies, so replies need extra binding to reach the right SA; the main use is separating multiple L2TP sessions, though any client-initiated protocol supported by conntrack works. Child: `mode = transport` with the two unique-mark options. Rules in the mangle table: PREROUTING applies the SA mark (ESP matching without NAT, UDP encapsulation ports with NAT), INPUT copies the IPsec policy mark into the conntrack entry with CONNMARK, and OUTPUT restores it so the correct SA is selected.

**forecast** (`--enable-forecast`). Allows identical IPsec policies with multicast or broadcast selectors and forwards such traffic over all matching SAs by listen-and-forward, between clients and between clients and the gateway LAN. Example child: `local_ts = 10.1.0.0/16,224.0.0.0/4` (local network plus multicast, or 0.0.0.0/0) and `remote_ts = dynamic,224.0.0.0/4,10.1.255.255`. Keep `dynamic` when a virtual IP is assigned, and list the required broadcast addresses.

## Checked
2026-11-04. Confirmed against the strongSwan connmark and forecast plugin pages: configure options, iptables header requirement, mark_in and mark_out = %unique, mangle-table rule flow, example selectors. Nothing removed.

Method: documentation only; no commands were run.
