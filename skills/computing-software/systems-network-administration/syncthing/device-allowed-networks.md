---
id: computing-software.systems-network-administration.syncthing.device-allowed-networks
name: device-allowed-networks
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, allowednetworks, cidr, connection-restrictions]
level: advanced
status: docs-checked
description: "Restrict which remote networks a Syncthing device may connect from or to using allowedNetworks CIDR lists."
sources: ["https://docs.syncthing.net/advanced/device-allowednetworks.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# allowedNetworks

## What it does
An advanced device setting affecting connection handling. Empty (default) means no restriction. Otherwise it is a comma-separated list of networks, and it refers to the address of the remote device, not the network the local device is presently on.

```
192.168.0.0/16, 172.16.0.0/12, 2001:db8::/32
```

With this value Syncthing will:
- allow connections from the device from addresses in those networks
- reject connections from the device from addresses outside them
- attempt connections to addresses in those networks (manually configured or discovered)
- not attempt connections to addresses outside them, whether manually configured or discovered

## Format rules
Only numeric IPv4 and IPv6 prefixes in CIDR notation work. Hostnames and dotted netmasks are not supported.

## Pitfalls
A non-empty value is enforced for all connections, so mentioning only an IPv4 prefix denies all IPv6 connections and vice versa. Use `0.0.0.0/0` (IPv4) or `::/0` (IPv6) to allow all connections on that address family.

## Checked
2026-11-04. Read the allowedNetworks page: default empty, comma-separated list, remote-address meaning, the four behaviours, numeric CIDR only (no hostnames or octet netmasks), enforcement for all connections, and the `0.0.0.0/0` and `::/0` family values. Removed the invented "Typical use" paragraph.
Method: documentation only; no commands were run.
