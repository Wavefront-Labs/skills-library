---
id: computing-software.systems-network-administration.headscale.dns-nameservers-split
name: dns-nameservers-split
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, nameservers, split-dns, search-domains, dns-config]
level: practitioner
status: docs-checked
description: "Push global nameservers, split-DNS domains and search domains to Headscale clients through the dns section of the config."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/config-example.yaml
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/about/features.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/policy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nameservers and split DNS

Global and restricted nameservers (split DNS) and search domains are supported.

```yaml
dns:
  nameservers:
    global:
      - 1.1.1.1
      - 1.0.0.1
    split: {}
  search_domains: []
```

- `nameservers.global`: DNS servers exposed to all clients (the example config lists 1.1.1.1, 1.0.0.1 and two IPv6 addresses).
- `nameservers.split`: a map of domains and which DNS server to use for each.
- `search_domains`: custom search domains.
- `override_local_dns: true` (default) makes these win over the node's local resolver settings.

## Related

- If NextDNS is the global resolver, the `nextdns:<profile>` node attributes can be used (policy-node-attributes).

## Gotchas

- `dns.base_domain` must be different from the `server_url` domain.
- For DNS configuration to have any effect, clients must have `--accept-dns=true` (the Tailscale client default). Setting any DNS config with it integrates with the client's DNS manager or overwrites `/etc/resolv.conf`.
- To stop Headscale managing DNS, set all fields under `dns` to empty values.

## Checked

2026-11-04. Confirmed against config-example.yaml (`dns.nameservers.global` and `split`, `search_domains`, `override_local_dns`, accept-dns note, base_domain) and the features page. Removed the restart-and-verify section with `tailscale dns status --all`, which the pages do not give.

Method: documentation only; no commands were run.
