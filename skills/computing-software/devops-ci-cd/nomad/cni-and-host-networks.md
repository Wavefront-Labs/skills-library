---
id: computing-software.devops-ci-cd.nomad.cni-and-host-networks
name: cni-and-host-networks
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, cni-and-host-networks, cni, host-network, cni-args, network-mode, portmap, slaac, ipv6, hcl]
level: advanced
status: docs-checked
description: "Use CNI networks and named host networks in Nomad with mode cni/name, portmap capabilities, cni args, host_network per port, and the SLAAC address-change limitation."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/network.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad CNI networks and host networks

## CNI
Nomad fingerprints CNI network configurations on each node by their `name` field; select one in the group network block with `mode = "cni/<name>"`. Given a node CNI config named `mynet` (a `ptp` plugin with `host-local` IPAM plus a `portmap` plugin with `"capabilities": {"portMappings": true}`):

```hcl
network {
  mode = "cni/mynet"
  port "http" {
    to = 8080
  }
  cni {
    args = {
      "nomad.region" : "${node.region}"
    }
  }
}
```
- The client builds the right capability arguments for `portmap` from the `port` blocks.
- `cni { args }` become `CNI_ARGS` per the CNI spec and support interpolation.
- `dns` settings in the block override DNS returned by CNI plugins.

### SLAAC limitation
CNI and Nomad service discovery assume addresses never change during an allocation. If the kernel uses IPv6 SLAAC, use a CNI plugin chain that waits for the prefix (the docs cite `arodd/cni-slaacwait`, chaining `macvlan` and `dhcp`). If the prefix changes after the task starts, networking fails; the docs recommend `connect` plus Consul DNS instead.

## Host networks
A port with `host_network = "<name>"` is only allocated on that named host network, and Nomad schedules the group only onto nodes that define it. Without it the `"default"` host network is used (commonly the address with the default route). Port mapping rules then use that host address as destination.

```hcl
network {
  mode = "bridge"
  port "https" {
    static       = 443
    to           = 8080
    host_network = "public"
  }
  port "admin" {
    to           = 9000
    host_network = "private"
  }
}
```
Use it to expose public traffic on one interface while keeping admin ports private. Basics of ports and modes are in `computing-software.devops-ci-cd.nomad.network-block`.

## Checked

2026-11-03. Confirmed against the network job-specification page (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: nothing; no unsupported claim found.

Method: documentation only; no commands were run.
