---
id: computing-software.ar-vr-development.mobile-and-spatial-ar.arkit-world-map-persistence
name: arkit-world-map-persistence
category: computing-software
field: ar-vr-development
product: mobile-and-spatial-ar
tags: [mobile-and-spatial-ar, arkit-world-map-persistence]
level: advanced
status: draft
description: "Save and reload an ARWorldMap."
sources: ['https://developers.google.com/ar', 'https://developer.apple.com/documentation/arkit']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Persist world maps
**Goal:** Save and reload an ARWorldMap.

- `session.getCurrentWorldMap` then archive with `NSKeyedArchiver`; reload via `config.initialWorldMap`.
- Wait for a good mapping status before saving.
- Maps can share across devices through data transfer.

## Gotchas
- Relocalisation fails in changed environments.

## Self-check
Anchors reappear in the same place after relaunch.
