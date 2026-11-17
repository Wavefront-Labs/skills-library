---
id: computing-software.cloud-infrastructure-engineering.garage.bootstrap-peers-list
name: bootstrap-peers-list
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [bootstrap-peers, garage-node-id, peer-discovery, connect-nodes]
level: practitioner
status: docs-checked
description: "List known peers in bootstrap_peers using the key@host:port form produced by garage node id."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`bootstrap_peers` is a list of peer identifiers a node contacts to find the rest of the cluster. Each identifier has the form:

`<node public key>@<node public IP or hostname>:<port>`

When `rpc_public_addr` is set properly on the target node, running `garage node id` there prints the full identifier, address and port included, which you can paste into the `bootstrap_peers` of other nodes. Otherwise the command prints only the public key and you must add the IP and port yourself.

Example shape from the configuration page:

`bootstrap_peers = [ "563e1ac8...bc95d@[fc00:1::1]:3901", "86f0f26a...f332@[fc00:1::2]:3901" ]`

Bootstrap peers are one discovery method. Alternatives are the `[consul_discovery]` and `[kubernetes_discovery]` sections, covered in their own pages. The `rpc_secret` is shared between all nodes of the cluster.

## Checked

2026-11-04. Read the Configuration file format page in full. Confirmed the identifier syntax, the `garage node id` behaviour with and without `rpc_public_addr`, the example shape and the consul and kubernetes sections. Removed the troubleshooting checklist and the reachable-port claim, which the page does not state.
Method: documentation only; no commands were run.
