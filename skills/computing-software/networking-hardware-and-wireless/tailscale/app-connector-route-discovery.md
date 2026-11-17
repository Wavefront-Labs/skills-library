---
id: computing-software.networking-hardware-and-wireless.tailscale.app-connector-route-discovery
name: app-connector-route-discovery
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [route-discovery, app-connector-domains, cname-records]
level: advanced
status: docs-checked
description: "Use FQDNs, CNAME handling and port 53 access so app connectors learn routes."
sources: ["https://tailscale.com/kb/1332"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# App connector route discovery

Goal: make app connectors discover and advertise the right routes.

**Domains.** Configure a list of valid fully qualified domain names. A and AAAA records are routed through the connector. Adding a domain triggers automatic route discovery; without pre-configured routes the connector enters a learning period during which it proxies DNS requests for the configured domains. With auto approval enabled, new routes are approved and advertised immediately; the learning period ends once all routes are discovered.

**How lookups work.** The connector acts as the authoritative nameserver for the configured domains, for example `*.example.com`, via an invisible split DNS entry.

**Port access.** Clients need access to the app connector tag for discovery, which uses the PeerAPI and needs the connector visible as a peer. Grant minimal access such as `tcp:53` or `udp:53`. Without it, DNS lookups never reach the connector and no routes are discovered.

**CNAME records.** The connector resolves CNAME chains and advertises routes for the final target. Verify with `dig`; in the docs example `app.acme.com` is a CNAME to `acme.backend.com`, and the target `acme.backend.com` is what gets advertised.

**Multiple connectors.** If several advertise a route, the tailnet's route selection option picks one per client.

**Checklist**

1. List FQDNs.
2. Allow port 53 to the connector tag.
3. Check CNAME targets with `dig`.

## Checked

2026-11-09. Confirmed against the Tailscale app connector best practices page: FQDN domains, learning period, auto approval, authoritative nameserver behaviour, port 53 access, CNAME chains and the dig example, and route selection. Nothing removed.

Method: docs-checked 2026-11-09 against tailscale.com/kb/1332 (Best practices for using app connectors), read in full.
