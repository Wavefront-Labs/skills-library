---
id: computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-bgp-session
name: troubleshoot-bgp-session
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, bgp-session, vtysh, frr, frr-k8s, reload-error, troubleshooting, tcpdump]
level: advanced
status: docs-checked
description: "Check MetalLB BGP sessions and advertisements: session metrics, native speaker logs, FRR vtysh commands, FRR reload errors and what to check when a session will not establish."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/troubleshooting/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting BGP

Prerequisite: a `BGPAdvertisement` exists. Pick one speaker that should advertise the IP and check the session is up and the IP advertised.

Session state metric: `metallb_bgp_session_up`, or `frrk8s_bgp_session_up` in FRR-K8s mode.

Native mode: speaker logs show `BGP session established` or `BGP session down`, and `failed to send BGP update` on advertisement failure.

FRR container (FRR mode):
- `vtysh show running-conf`: current FRR configuration
- `vtysh show bgp neigh <neigh-ip>`: `Established` means healthy
- `vtysh show ipv4` / `ipv6`: advertisements

FRR-K8s mode: check the FRR-K8s pod logs and the `FRRNodeState` resources.

Deprecated FRR mode: an invalid generated config yields a `reload error` log in the speaker container; the `reloader` logs may show the invalid file.

Session will not establish but config looks fine:
- Parameters: ASNs, passwords.
- FRR container logs.
- tcpdump on the nodes, using the right port if you overrode `peerPort`.

If the configuration and the logs look fine on MetalLB's side, check the routing table on the routers corresponding to the `BGPPeer`s.

Related: `computing-software.cloud-infrastructure-engineering.metallb.bgp-peer-and-advertisement`, `computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-rp-filter`.

## Checked
2026-11-04. Confirmed against the MetalLB Troubleshooting page, "Checking if the BGP advertisement works": session metrics, native log lines, the three vtysh commands, FRR-K8s note, reload error, session checklist, router routing table. Removed a BGPSessionState mention (not on this page) and a claim about routers filtering routes.
Method: documentation only; no commands were run.
