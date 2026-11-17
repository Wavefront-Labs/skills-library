---
id: computing-software.cloud-infrastructure-engineering.kubespray.coredns-configuration-variables
name: coredns-configuration-variables
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [coredns, dns, external-zones, cache, rewrite, dns-etchosts, old-dns-domains]
level: advanced
status: docs-checked
description: "Customise CoreDNS from the Kubespray inventory: external zones, dns_etchosts, cache block, old_dns_domains and the systemd-resolved fix."
sources:
  - https://kubespray.io/docs/advanced/dns-stack.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Variables that shape the CoreDNS Corefile:

- `dns_upstream_forward_extra_opts`: dictionary of options for the forward block in CoreDNS and nodelocaldns configs.
- `coredns_kubernetes_extra_opts` and `coredns_kubernetes_extra_domains`: extra options and domains for the kubernetes plugin.
- `coredns_additional_configs` and `coredns_rewrite_block` (the rewrite plugin).
- `enable_coredns_reverse_dns_lookups` defaults to `true`.

**External zones** forward well-known or internal-only zones (such as a VPN domain), injected before the default kubernetes zone:

```yaml
coredns_external_zones:
- zones:
  - example.com
  - example.io:1053
  nameservers:
  - 1.1.1.1
  - 2.2.2.2
  cache: 5
```

Entries can also carry a `rewrite` list, and the variable can be passed as an INI JSON string.

**Static hosts**, also used by nodelocaldns:

```yaml
dns_etchosts: |
  192.168.0.100 api.example.com
  192.168.0.200 ingress.example.com
```

**Cache tuning** on the default zone:

```yaml
coredns_default_zone_cache_block: |
  cache 3600 {
    success 3000
    denial 0
    prefetch 10 1m
  }
```

**Old domains.** After changing `dns_domain`, `old_dns_domains: [example1.com, example2.com]` makes names under the old domains answer the same as under `cluster.local`.

If CoreDNS fails with `address already in use`, set `systemd_resolved_disable_stub_listener` to `true` (it defaults to `true` only on Flatcar).

## Checked

2026-11-08. Cited pages re-read in full. Each variable and snippet was confirmed on the DNS stack page, DNS variables section.

Method: documentation only; no commands were run.
