---
id: computing-software.ar-vr-development.mobile-and-spatial-ar.arcore-cloud-geospatial
name: arcore-cloud-geospatial
category: computing-software
field: ar-vr-development
product: mobile-and-spatial-ar
tags: [mobile-and-spatial-ar, arcore-cloud-geospatial]
level: advanced
status: draft
description: "Share anchors across devices and anchor to the world."
sources: ['https://developers.google.com/ar', 'https://developer.apple.com/documentation/arkit']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud Anchors and Geospatial API
**Goal:** Share anchors across devices and anchor to the world.

- Cloud Anchors host and resolve with a TTL; authentication via keyless or API key set up in Google Cloud (confirm current limits in docs).
- Geospatial API uses VPS and Street View coverage; check `earth.earthState` and localisation accuracy.
- Disclose camera and location use in privacy notices.

## Gotchas
- Coverage is limited to certain areas.

## Self-check
Anchor hosted on one device appears on another.
