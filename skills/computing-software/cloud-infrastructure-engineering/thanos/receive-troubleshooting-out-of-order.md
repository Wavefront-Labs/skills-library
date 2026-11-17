---
id: computing-software.cloud-infrastructure-engineering.thanos.receive-troubleshooting-out-of-order
name: receive-troubleshooting-out-of-order
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-receive, out-of-order, out-of-bound, troubleshooting]
level: advanced
status: docs-checked
description: "Diagnose the out-of-bound and out-of-order sample errors logged by Thanos Receive."
sources: ["https://thanos.io/tip/operating/troubleshooting.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Receive: out-of-bound and out-of-order errors

**Out-of-bound** (`Error on ingesting samples that are too old or are too far into the future`): the sample timestamp is below the TSDB head's minimum acceptable time. Causes:
1. Receive was stopped and resumed, and remote Prometheus resends from its oldest sample.
2. Receive lacks compute, so ingestion falls behind scraping.

Check the pod history for case 1. For case 2, in kube-prometheus-stack look at the "Prometheus / Remote Write" dashboard; a rate above 0 for a long period means adding replicas or resources to Receive.

**Out-of-order** (`Error on ingesting out-of-order samples`): TSDB expects chronological order per series, so any sample older than one already accepted with an identical label set is rejected. Causes include:
- Prometheus HA with an unset or empty replica external label name.
- Federation with `honor_labels` and `honor_timestamps` both true and the same replica label name at all layers.
- Several remote Prometheus deployments with identical external labels (for example all empty) and metrics with no unique label, such as aggregated cluster CPU usage.

Fixes from the docs: give each remote Prometheus deployment distinct external labels; use a different replica external label name for each federation layer; use static-endpoint federation if the lesser Prometheus is in HA.

Enable debug logging on Receive to see the label set of the rejected sample. The Receive flag `--tsdb.out-of-order.time-window` (experimental, default 0s) allows out-of-order ingestion within a window; if you use it with the compactor, enable `--compact.enable-vertical-compaction` or risk a compactor halt. `--tsdb.too-far-in-future.time-window` (default 0s) rejects samples beyond Receive's local NTP time plus the window.

## Checked

2026-11-03. Confirmed against the Thanos Receive page (components/receive.md) and the Thanos troubleshooting page (operating/troubleshooting.md): hashrings and ketama, shuffle sharding, tenancy and decommissioning, quorum formula, Cap'n Proto, limits and gates, defaults, out-of-bound and out-of-order causes. Added the documented fixes and the out-of-order window flag warnings. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
