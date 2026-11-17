---
id: computing-software.game-programming.game-engine-architecture.gameplay-telemetry-pipelines
name: gameplay-telemetry-pipelines
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, gameplay-telemetry, analytics, live-ops, game-programming]
level: practitioner
status: draft
description: "Instrument gameplay telemetry: event schemas, batching and offline buffering, sampling, privacy and consent, and heatmap and funnel analysis."
sources: ["https://learn.microsoft.com/en-us/gaming/playfab/features/analytics/", "https://opentelemetry.io/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gameplay telemetry

**Goal:** know where players die, quit or get stuck, with data you can trust and are allowed to collect.

## Event design
```json
{ "event": "player_death", "v": 2, "ts": 1760781234.5, "session": "...", "build": "1.4.2",
  "level": "forest_02", "pos": [123.4, 5.0, -88.2], "cause": "fall", "playtime_s": 5310 }
```
- Versioned schemas; every event carries session id, build, platform, timestamp.
- Prefer few, well-defined events (session_start/end, level_start/complete/fail, death, purchase,
  settings_changed) over logging everything.
- Positions enable heatmaps; include level/region id.

## Client pipeline
- Queue events in memory, batch every N seconds or N events, compress, send over HTTPS.
- Persist unsent batches to disk for offline play; cap size and drop oldest.
- Never block the game thread; never retry in tight loops.
- Sampling for high-frequency events (position every 10 s, not every frame).

## Privacy and consent
- GDPR/CCPA: lawful basis, consent where needed, opt-out, data deletion requests, child players
  (COPPA). Pseudonymous ids; avoid raw IPs and free text.
- Platform rules (console TRCs, App Store tracking transparency) apply.

## Analysis
- Funnels (tutorial step completion), retention cohorts (D1/D7), death and quit heatmaps over level
  maps, difficulty spikes (fail rate by checkpoint).
- Join with build/patch to measure changes.

## Verify
- Dev build validation mode: schema-check every event locally and show it in a debug overlay.
- Count events received vs sent in a test session (no loss, no duplicates beyond idempotent retry).
