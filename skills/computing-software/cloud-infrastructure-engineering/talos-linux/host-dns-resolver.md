---
id: computing-software.cloud-infrastructure-engineering.talos-linux.host-dns-resolver
name: host-dns-resolver
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [host-dns, resolverconfig, coredns, kube-dns, caching, networking]
level: practitioner
status: docs-checked
description: "Talos host DNS caching resolver: ResolverConfig hostDNS, 127.0.0.53, forwardKubeDNSToHost with 169.254.116.108, member-name resolution and the inspection commands."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/networking/host-dns.mdx
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/networking/configuration/resolvers.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since Talos 1.7 a caching DNS resolver runs on the host for host workloads and host-networking pods. Configure it in the `hostDNS` section of `ResolverConfig`:

```yaml
apiVersion: v1alpha1
kind: ResolverConfig
hostDNS:
  enabled: true
```

The old `.machine.features.hostDNS` field is deprecated in 1.14 and mutually exclusive with the document.

Operation: the server listens on `127.0.0.53:53` (TCP and UDP) and `/etc/resolv.conf` points at it. Upstreams come from DHCP, platform sources, kernel args or the machine config. Inspect with:

```shell
talosctl get resolvers
talosctl logs dns-resolve-cache
talosctl get dnsupstream
```

`forwardKubeDNSToHost` (default for new clusters from 1.8) makes CoreDNS use the host resolver at `169.254.116.108`, sharing the cache. Disabling host DNS requires `forwardKubeDNSToHost: false`, otherwise validation fails. To turn only forwarding off:

```yaml
apiVersion: v1alpha1
kind: ResolverConfig
hostDNS:
  enabled: true
  forwardKubeDNSToHost: false
```

Apply to all nodes and restart `coredns` pods if changed after creation.

`resolveMemberNames: true` resolves cluster member names from discovery data, so `talosctl -n talos-default-worker-1 version` works; with forwarding on, kube-dns resolves them too. Default upstreams are `8.8.8.8` and `1.1.1.1`; custom nameservers and `searchDomains` go in the same `ResolverConfig`.

## Checked

2026-11-04. hostDNS enablement, listen address, forwardKubeDNSToHost, resolveMemberNames and inspection commands confirmed on the Host DNS page; default resolvers and search domains on the Resolvers page.

Method: documentation only; no commands were run.
