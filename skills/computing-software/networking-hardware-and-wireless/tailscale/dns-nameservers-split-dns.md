---
id: computing-software.networking-hardware-and-wireless.tailscale.dns-nameservers-split-dns
name: dns-nameservers-split-dns
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [split-dns, global-nameserver, override-dns]
level: practitioner
status: docs-checked
description: "Choose restricted versus global nameservers and the Override DNS servers setting."
sources: ["https://tailscale.com/kb/1054"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tailnet nameservers and split DNS

Goal: control which DNS servers tailnet clients use.

**Two nameserver types**

- Restricted nameserver: applies only to queries matching a search domain (split DNS). Example: set `1.1.1.1` as the nameserver for `example.com` and only `*.example.com` lookups use it.
- Global nameserver: handles queries for any domain.

**Details**

- Public global nameservers such as Cloudflare, Google or Quad9 get DNS-over-HTTPS automatically. Examples listed: Quad9 `9.9.9.9`, Google `8.8.8.8`, Cloudflare `1.1.1.1`.
- Tailscale treats a provider's address list as one entity: adding one Google address includes all of Google's.
- NextDNS or Control D can be used as personalized global nameservers.
- By default devices use local DNS settings for all queries. Enable the Override DNS servers toggle to force clients to always use your nameservers.
- Unless nameservers are public or use Tailscale IPs, configure subnet routing so devices can reach private DNS servers.
- Clients must be set to use Tailscale DNS settings for any of this to apply.
- Arbitrary records cannot be added to MagicDNS.
- The `tailscale dns` command also manages DNS.

**Checklist**

1. Pick restricted or global per domain.
2. Use more than one global nameserver for redundancy.
3. Route to private resolvers.
4. Decide on Override DNS servers.

## Checked

2026-11-03. Read DNS in Tailscale (kb/1054) and confirmed restricted versus global nameservers, DoH for public providers and the Override DNS servers toggle. Nothing else was removed.

Method: documentation only; no commands were run.
