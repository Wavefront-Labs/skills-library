---
id: computing-software.systems-network-administration.headscale.supported-clients
name: supported-clients
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, clients, platforms, linux, freebsd]
level: intro
status: docs-checked
description: "Which client platforms work with Headscale, how many Tailscale releases are targeted, and where per-platform instructions live."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/about/clients.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/about/features.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/about/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Supported clients

Listed as supported with Headscale: Linux, OpenBSD, FreeBSD, Windows, Android, macOS, iOS and tvOS.

The project targets the last 10 Tailscale client releases. Some platforms need extra configuration to connect to Headscale.

## Where to look

| Platform | Guide |
|---|---|
| Windows | client-windows, or `/windows` on your Headscale server |
| macOS, iOS, tvOS | client-apple, or `/apple` on your server |
| Android | client-android |
| Linux, BSD | no extra notes; use `tailscale up --login-server <YOUR_HEADSCALE_URL>` |

## Gotchas

- Not every Tailscale SaaS feature is supported: the features page marks Funnel and network flow logs as unsupported (feature-support skill).
- Running Headscale on a machine that is also in the tailnet can cause problems with subnet routers, traffic relay nodes and MagicDNS; the FAQ says it might work but is not supported.

## Checked

2026-11-04. Confirmed against the Headscale clients page (OS table, last 10 releases, /windows and /apple pages), the features page and the FAQ. Removed an unsourced advice line about old clients.
Method: documentation only; no commands were run.
