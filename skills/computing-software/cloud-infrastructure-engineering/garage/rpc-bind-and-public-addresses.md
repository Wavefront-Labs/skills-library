---
id: computing-software.cloud-infrastructure-engineering.garage.rpc-bind-and-public-addresses
name: rpc-bind-and-public-addresses
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [rpc-bind-addr, rpc-public-addr, rpc-public-addr-subnet, rpc-bind-outgoing]
level: practitioner
status: docs-checked
description: "Configure the RPC listen address, the public address peers use, and subnet filtering behind NAT."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`rpc_bind_addr` is the address and port for inter-cluster RPC, typically `"[::]:3901"`. The port must be the same one other nodes use to reach this node, even through NAT. So the NAT must forward the external port to the same internal port, and several nodes behind one NAT need different RPC ports.

`rpc_public_addr` is the address and port that other nodes should use to contact this node. It is optional but recommended, and helps when a NAT maps the RPC port to a different public port.

`rpc_public_addr_subnet` applies when `rpc_public_addr` is not set but autodiscovery is used. It filters the discovered IP addresses down to a subnet, for example `"2001:0db8:f00:b00:/64"`, so a node picks its address from a given range without hardcoding a dynamic IP, and configs can be shared between nodes.

`rpc_bind_outgoing` (since v0.9.2, disabled by default) pre-binds outgoing sockets to the same IP as `rpc_bind_addr` before connecting to remote nodes. It is needed when a host has several IP addresses and only one can reach the others because of firewall or routing rules.

Run `garage node id` to print a node's identifier; with `rpc_public_addr` set correctly it includes the address.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Configuration file format. Confirmed on the configuration page: `rpc_bind_addr`, NAT port rule, `rpc_public_addr`, `rpc_public_addr_subnet` with its example, `rpc_bind_outgoing` (since v0.9.2, disabled by default), and `garage node id`. No changes needed.

Method: documentation only; no commands were run.
