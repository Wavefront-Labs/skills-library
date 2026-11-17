---
id: computing-software.networking-hardware-and-wireless.caddy.on-demand-tls
name: on-demand-tls
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [on-demand-tls, ask-endpoint, sni, saas, certificate-on-handshake, abuse-prevention, automatic-https]
level: advanced
status: docs-checked
description: "Caddy on-demand TLS: when it fits, enabling it in site blocks, the required ask endpoint restriction and the first-handshake delay."
sources:
  - https://caddyserver.com/docs/automatic-https
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve domains you do not know ahead of time, such as customer domains.

On-demand TLS obtains a certificate during the first TLS handshake that needs it instead of at config load, so domain names need not be listed. It suits cases where you do not know all names at start or reload, DNS may not be ready yet, or customers control the names. The handshake for an unknown SNI is held while Caddy obtains a certificate; the delay is usually a few seconds and only for that first client. Later handshakes use the cached certificate and renewals happen in the background.

It must be both enabled and restricted. Enable it in a Caddyfile site block with the `tls` directive (or in JSON TLS automation policies). Restrict it in the `on_demand_tls` global option (JSON: the `automation` object). Restrictions are global, not per site or domain. The main one is an "ask" endpoint: Caddy sends an HTTP request asking whether it may obtain and manage a certificate for the domain in the handshake. Your backend answers, for example by checking an accounts table.

Be mindful of how fast your CA issues; slow issuance hurts the first visitor. Because of the deferred nature and extra configuration needed to prevent abuse, the page recommends it only for the use cases above.

## Checked

2026-11-08. Read the Automatic HTTPS page in full (On-Demand TLS section). Confirmed: the three use cases, the held handshake and few-second first-client delay, caching and background renewal, enabling via the `tls` directive or TLS automation policies, restrictions via the `on_demand_tls` global option or the JSON `automation` object, the ask endpoint, and the recommendation to use it only for those cases. Removed the unconfirmed `on_demand` JSON key name.

Method: documentation only; no commands were run.

