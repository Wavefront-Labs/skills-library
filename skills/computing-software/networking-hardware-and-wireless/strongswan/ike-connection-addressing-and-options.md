---
id: computing-software.networking-hardware-and-wireless.strongswan.ike-connection-addressing-and-options
name: ike-connection-addressing-and-options
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, ike-connection, remote-addrs, fragmentation, send-certreq, encap]
level: practitioner
status: docs-checked
description: "Connection-level swanctl.conf options for strongSwan: IKE version, local and remote addresses and ports, fragmentation, certreq and cert sending, encap, keyingtries, uniqueness."
sources:
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlConf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ike connection addressing and options
- `version`: default `2`; `1` is deprecated IKEv1; `0` accepts both as responder and initiates with IKEv2.
- `local_addrs` / `remote_addrs`: default `%any`. Accept addresses, DNS names, CIDR subnets or ranges, comma-separated. As initiator the first non-range, non-subnet is used; to initiate, at least one specific address or DNS name is needed in `remote_addrs`. FQDNs are resolved on each config lookup.
- `local_port` / `remote_port`: default 500; with 500, IKE floats to 4500 for NAT. A non-default local port needs the socket-dynamic plugin.
- `encap = yes` forces UDP encapsulation of ESP by manipulating NAT detection payloads, to get past firewalls that block ESP.
- `mobike`: default yes; IKEv2 then always floats to port 4500 from the second exchange; disable for implementations that dislike it.
- `fragmentation`: `yes` (default), `accept`, `force` (IKEv1 only) or `no`. Peer fragments are always processed.
- `childless`: `allow` (default), `prefer`, `force`, `never` (RFC 6023).
- `send_certreq` (default yes): disable if too many trusted roots enlarge the initial packets. `send_cert`: `ifasked` (default), `never`, `always`.
- `keyingtries` (default 1): `0` retries until success or a permanent error.
- `unique`: `no`, `never`, `keep`, `replace`; compared by remote IKE identity, or EAP or XAuth identity when used.
- `aggressive` (IKEv1): less secure; exposes IDs and allows dictionary attacks on a PSK.

## Checked
2026-11-04. Confirmed every option and default above against the connections section of the swanctl.conf page.

Method: documentation only; no commands were run.
