---
id: computing-software.cloud-infrastructure-engineering.kubespray.nodelocaldns-cache-and-ha
name: nodelocaldns-cache-and-ha
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [nodelocaldns, dns, cache, daemonset, external-zones, ha]
level: advanced
status: docs-checked
description: "Run Kubespray's node-local DNS cache, add external zones, and enable the secondary pod (enable_nodelocaldns_secondary) to survive upgrades."
sources:
  - https://kubespray.io/docs/advanced/dns-stack.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`enable_nodelocaldns: true` makes pods use a DNS caching agent on the same node, avoiding iptables DNAT and connection tracking. It queries CoreDNS for cache misses on cluster names. Per the page, since the 2.10 release it is enabled by default.

**External zones** extend its configuration with the same shape as CoreDNS external zones:

```yaml
nodelocaldns_external_zones:
- zones:
  - example.com
  - example.io:1053
  nameservers:
  - 1.1.1.1
  - 2.2.2.2
  cache: 5
```

`dns_etchosts` and `nodelocaldns_additional_configs` also apply to it.

**HA.** A single nodelocaldns pod may not be replaced quickly enough during a cluster or nodelocaldns upgrade, causing short DNS timeouts. Enable a redundant pod per node:

```yaml
enable_nodelocaldns_secondary: true
nodelocaldns_secondary_skew_seconds: 5
```

The skew is the time in seconds the secondary may survive when both DaemonSets update at once; tune it by testing. Caveat: with the secondary enabled, the primary no longer tears down its iptables rules, so if both have failing pods on the same node there can be a DNS blackout with traffic no longer forwarded to the central CoreDNS. Account for this if you disable the cache.

**Limits** from the page: `searchdomains` allows 6 names and 256 characters, but the default cluster domains reduce that to 4 names and 239 characters (back to 6 with `remove_default_searchdomains: true`), and `nameservers` takes at most 3 with only 2 custom because one slot is reserved. Note `ndots` high values hurt performance.

## Checked

2026-11-08. Cited pages re-read in full. Settings, caveats and limits were confirmed on the Nodelocal DNS cache and Limitations sections of the DNS stack page.

Method: documentation only; no commands were run.
