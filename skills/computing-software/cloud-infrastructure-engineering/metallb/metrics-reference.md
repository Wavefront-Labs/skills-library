---
id: computing-software.cloud-infrastructure-engineering.metallb.metrics-reference
name: metrics-reference
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, metrics-reference, allocator, k8s-client, frrk8s-metrics, bgp-session-up, bfd-session-up]
level: practitioner
status: docs-checked
description: "MetalLB Prometheus metric names: allocator, k8s client, native/FRR bgp and FRR-K8s bgp/bfd metrics, the metallb_ vs frrk8s_ prefix and peer label format."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/prometheus-metrics/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metrics reference

Allocator (per pool): `metallb_allocator_addresses_in_use_total`, `metallb_allocator_addresses_total` (usable addresses).

K8s client: `metallb_k8s_client_updates_total`, `metallb_k8s_client_update_errors_total`, `metallb_k8s_client_config_loaded_bool` (1 if config loaded at least once), `metallb_k8s_client_config_stale_bool` (1 if running a stale config because the latest failed to load).

BGP with `metallb_bgp_` prefix (native BGP, and deprecated FRR mode via the FRR metrics sidecar): `metallb_bgp_session_up` (1 up, 0 down), `metallb_bgp_updates_total`, `metallb_bgp_announced_prefixes_total`.

Default FRR-K8s mode uses `frrk8s_` and the `peer` label holds only the IP (no port); with a VRF an extra `vrf` label appears.
- BGP: `frrk8s_bgp_session_up`, `_announced_prefixes_total`, `_received_prefixes_total`, `_opens_sent`, `_opens_received`, `_notifications_sent`, `_updates_total`, `_updates_total_received`, `_keepalives_sent`, `_keepalives_received`, `_route_refresh_sent`, `_total_sent`, `_total_received`.
- BFD: `frrk8s_bfd_session_up`, `_control_packet_input`, `_control_packet_output`, `_echo_packet_input`, `_echo_packet_output`, `_session_up_events`, `_session_down_events`, `_zebra_notifications`.

Gotcha: older FRR-based setups used `metallb_` names and `peer="172.23.0.5:179"`; migrating dashboards need relabeling (`computing-software.cloud-infrastructure-engineering.metallb.metrics-relabeling`).

Scrape setup: `computing-software.cloud-infrastructure-engineering.metallb.prometheus-scraping`. Alerts: `computing-software.cloud-infrastructure-engineering.metallb.alert-rules`.

## Checked

2026-11-04. Every metric name, the metallb_ vs frrk8s_ prefix rule, peer label format, VRF label and the relabeling note were compared with the MetalLB Prometheus Metrics page and match. Nothing removed.

Method: documentation only; no commands were run.
