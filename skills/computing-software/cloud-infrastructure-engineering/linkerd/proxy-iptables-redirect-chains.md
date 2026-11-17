---
id: computing-software.cloud-infrastructure-engineering.linkerd.proxy-iptables-redirect-chains
name: proxy-iptables-redirect-chains
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, iptables, init-container, proxy, networking]
level: sme
status: docs-checked
description: "Understand the PROXY_INIT_REDIRECT and PROXY_INIT_OUTPUT chains, the inbound port 4143 and outbound port 4140 redirects."
sources:
  - https://linkerd.io/2.19/reference/iptables/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`linkerd-init` creates two chains in the `nat` table: `PROXY_INIT_REDIRECT` for inbound and `PROXY_INIT_OUTPUT` for outbound packets.

Inbound: the `PREROUTING` chain sends packets to the redirect chain through the rule `install-proxy-init-prerouting`. That chain has two more rules:

1. `ignore-port`: packets whose destination ports are in the `skip-inbound-ports` install option bypass the proxy and go straight to the application.
2. `proxy-init-redirect-all`: `iptables -t nat -A PROXY_INIT_REDIRECT -p tcp -j REDIRECT --to-port 4143` redirects all other TCP packets to the proxy's inbound port 4143.

The proxy recovers the original destination with the `SO_ORIGINAL_DST` socket option, processes the request and sends a new packet through `OUTPUT` to the application.

Outbound: packets leaving the pod traverse `OUTPUT`, where a rule jumps to `PROXY_INIT_OUTPUT`. Its `redirect-all-outgoing` rule, `iptables -t nat -A PROXY_INIT_OUTPUT -p tcp -j REDIRECT --to-port 4140`, sends outgoing TCP to the proxy's outbound port 4140.
To debug, inspect the rules a pod got with `kubectl -n NAMESPACE logs POD linkerd-init`.

## Checked

2026-11-08. Read in full against the Linkerd 2.19 docs source (markdown in linkerd/website) of https://linkerd.io/2.19/reference/iptables/. Confirmed the chains, rule names and ports 4143 and 4140. Removed an unsourced note on mTLS and CAP_NET_ADMIN and replaced it with the documented linkerd-init log command.

Method: documentation only; no commands were run.
