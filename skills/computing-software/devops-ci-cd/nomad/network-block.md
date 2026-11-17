---
id: computing-software.devops-ci-cd.nomad.network-block
name: network-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, network-block, network, ports, dynamic-ports, static-ports, bridge-mode, port-mapping, nomad-port, dns, ignore-collision, hcl]
level: practitioner
status: docs-checked
description: "Allocate ports and network modes for a Nomad group with the network block covering dynamic and static ports, to mapping, NOMAD_PORT env vars, bridge mode, firewalld and DNS."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/network.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad network block

`network` (group level, **only one per group**) declares the group's network mode and ports. Only services that *listen* need ports; batch jobs and outbound-only services do not.

```hcl
network {
  mode = "bridge"
  port "http" {}
  port "lb"   { static = 8889 }
  port "app"  { to = 8080 }
}
```

## Modes (`mode`, default `"host"`, Linux only; other OSes use host)
- `host` - tasks join the host network namespace.
- `bridge` - shared isolated namespace for the group bridged to the host; prerequisite for Consul service mesh (apps can bind to localhost and use the proxy). Needs the reference CNI plugins at the client's `cni_path`. Bridge works with the `docker`, `exec`, `raw_exec` and `java` drivers. To avoid external access, bind workloads to loopback only.
- `none` - isolated namespace with no interfaces.
- `cni/<name>` - namespace configured by a CNI network (`computing-software.devops-ci-cd.nomad.cni-and-host-networks`).

## Port parameters
- Label - identifies the port in service discovery and in env var names. Task gets `NOMAD_IP_<label>`, `NOMAD_PORT_<label>` and `NOMAD_ADDR_<label>`.
- Dynamic (empty block) - allocated from `20000` to `32000`. Preferred for nearly everything; the app reads the env var to know where to bind.
- `static` - fixed host port; the group lands only on a node where it is free. Not recommended except for system jobs or specialised ones such as load balancers.
- `to` - mapped port inside the namespace (bridge, or drivers like Docker and QEMU). Omitted or `-1` means equal to the allocated port. `NOMAD_PORT_<label>` contains the `to` value and `NOMAD_HOST_PORT_<label>` the host port. For group network ports only these two (`NOMAD_PORT_` and `NOMAD_HOST_PORT_`) are set.
- `ignore_collision` (`false`) - allow placement where the port is already reserved, for programs using `SO_REUSEPORT`. Only with host mode and `static` ports; Docker may also need `network_mode = "host"`.

## Other parameters
- `hostname` - Docker driver and bridge mode only, supports interpolation.
- `dns { servers, searches, options }` - Linux only; with `cni/*` modes these override DNS from the CNI plugins.
- `mbits` is deprecated.

## Gotcha: firewalld
Bridge mode may break outbound requests on RHEL-family hosts running firewalld. Mark the `nomad` bridge interface trusted: `sudo firewall-cmd --zone=trusted --add-interface=nomad` (plus `--permanent`), then restart affected jobs.

## Checked

2026-11-03. Confirmed against the network job-specification page (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: nothing; no unsupported claim found.

Method: documentation only; no commands were run.
