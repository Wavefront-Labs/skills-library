---
id: computing-software.game-programming.multiplayer-networking.production-network-telemetry
name: production-network-telemetry
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, network-telemetry, observability, live-ops, game-programming]
level: practitioner
status: draft
description: "Instrument live multiplayer networking: per-connection RTT, loss, jitter and bandwidth metrics, server tick health, aggregation by region and alerting."
sources: ["https://opentelemetry.io/docs/", "https://partner.steamgames.com/doc/api/steamnetworkingtypes"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Production network telemetry

**Goal:** know how the netcode performs for real players, by region, platform and ISP, before
reviews tell you.

## Client/connection metrics
Sample per connection every few seconds:
- RTT (min/avg/p95), jitter, inbound/outbound loss %, out-of-order %, bandwidth in/out.
- Prediction corrections per minute and correction magnitude; interpolation buffer underruns
  (extrapolation time).
- GameNetworkingSockets exposes this via `GetConnectionRealTimeStatus` (`m_nPing`,
  `m_flConnectionQualityLocal/Remote`, `m_flOutBytesPerSec`).

## Server metrics
- Tick duration p50/p99 vs budget, ticks missed, players per server, CPU/memory, outgoing packets per
  tick, snapshot size.

## Pipeline
- Aggregate on the server per match and send summaries (histograms, not every sample) to your
  telemetry backend; OpenTelemetry metrics or a game analytics pipeline.
- Tag with region, data centre, platform, client build, connection type, coarse ISP/ASN.
- Correlate with gameplay telemetry (quits, rage quits shortly after high-loss periods).

## Dashboards and alerts
- Heatmap of RTT by region/data centre; alert on p95 RTT or loss jumps per data centre (often a
  routing or DDoS issue).
- Tick overrun alerts per build (server performance regressions).
- Per-patch comparison of correction rates.

## Privacy
IP addresses are personal data; derive region/ASN at ingest and drop raw IPs.

## Verify
- Inject loss with a link emulator for a test account; the dashboard shows the spike within minutes.
