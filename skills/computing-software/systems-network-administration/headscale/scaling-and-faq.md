---
id: computing-software.systems-network-administration.headscale.scaling-and-faq
name: scaling-and-faq
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, scaling, faq, same-machine, device-visibility, support]
level: practitioner
status: docs-checked
description: "Headscale FAQ essentials: scaling limits, supported deployment methods, reverse proxy support, running with Tailscale on one machine, update path."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/about/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scaling and FAQ gotchas

## Scale

It depends. Headscale targets homelabs and self-hosters; performance is not a design priority. The main bottleneck is recomputing the network map whenever something changes.

- Scenario 1, 1000 servers that rarely move: computing the world map is very demanding, then usage returns to low until the next event.
- Scenario 2, 80 laptops or phones that move often: computing the map is less demanding, but constant changes lead to constant resource usage.
- Headscale struggles when the two overlap (many nodes with frequent changes); it can likely handle 100s of devices (maybe more) when little to no change happens.

## Support boundaries

- Officially supported: binaries and DEB packages. Container images are built, but Docker is not officially supported.
- The maintainers do not use reverse proxies and cannot diagnose them; community docs and the Discord reverse-proxy-issues channel exist.
- Headscale and Tailscale on the same machine is not supported; it can break subnet routers, relay nodes and MagicDNS.
- Update one minor version at a time (upgrade-procedure).

## Visibility

Nodes can see each other in `tailscale status` even if the policy allows only one direction; policy still filters traffic, and `tailscale ping` is always allowed both ways.

## Project model

Contributions are discussed with maintainers before a pull request; plans live in GitHub Milestones.

## Checked

2026-11-04. Confirmed against the Headscale FAQ (scaling scenarios, supported deployment methods, Docker, reverse proxies, same-machine caveat, update path, device visibility, contribution model).

Method: documentation only; no commands were run.
