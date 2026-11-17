---
id: computing-software.systems-network-administration.pi-hole.upstream-dns-provider-choices
name: upstream-dns-provider-choices
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [upstream-providers, quad9, opendns]
level: intro
status: docs-checked
description: "Choose an upstream DNS provider for Pi-hole from the installer presets and know what each offers."
sources: ["https://docs.pi-hole.net/guides/dns/upstream-dns-providers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Choosing upstream DNS providers

The installer offers preset upstream providers (the page lists Google, OpenDNS, Level3, Comodo, Quad9, Quad9 unfiltered, Quad9 ECS, Cloudflare DNS, and Custom). Google is the default.

**Provider addresses from the guide**

| Provider | IPv4 addresses |
| --- | --- |
| Google (default) | `8.8.8.8`, `8.8.4.4` |
| OpenDNS Home (Cisco) | `208.67.222.222`, `208.67.220.220`, `208.67.222.220`, `208.67.220.222` |

OpenDNS Home includes a phishing filter. OpenDNS also offers FamilyShield, a free option that blocks pornographic content plus proxies and anonymizers.

**Choosing**

- The Pi-hole Unbound guide describes running your own recursive resolver to avoid having to trust an upstream provider.
- The dnscrypt-proxy guide covers DoH or other encrypted DNS between Pi-hole and upstream servers.
- For a custom provider, the page suggests looking at the OpenNIC DNS Project if you care about Internet independence and privacy.

**Setting it**

```bash
sudo pihole-FTL --config dns.upstreams '["8.8.8.8", "8.8.4.4"]'
```

`dns.upstreams` accepts IP addresses or hostnames with an optional `#port`; if it is empty, Pi-hole resolves no non-local queries.

## Checked

2026-11-03. Read the Upstream DNS Providers page (the nine installer options, Google default and addresses, OpenDNS Home addresses and phishing filter, FamilyShield description), the FTL configuration reference (`dns.upstreams` format and empty behaviour), and the opening of the Unbound and dnscrypt-proxy guides. Removed the generic checklist (privacy policy, two addresses, dashboard check).

Method: documentation only; no commands were run.
