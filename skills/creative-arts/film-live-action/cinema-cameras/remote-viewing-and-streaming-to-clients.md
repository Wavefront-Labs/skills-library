---
id: creative-arts.film-live-action.cinema-cameras.remote-viewing-and-streaming-to-clients
name: remote-viewing-and-streaming-to-clients
category: creative-arts
field: film-live-action
product: cinema-cameras
tags: [cinema-cameras, film-live-action, remote-viewing, stream-to-client, remote-village, qtake-cloud, frame-io-c2c, low-latency-streaming, secure-streaming, remote-producers]
level: practitioner
status: draft
description: "Stream the camera feed to remote producers and clients: video assist and encoders, secure low-latency platforms, colour-accurate viewing, multi-camera feeds and comms."
sources:
  - "https://www.qtake-hd.com (QTAKE - video assist and QTAKE Cloud streaming)"
  - "https://frame.io/c2c (Frame.io Camera to Cloud)"
  - "https://www.teradek.com (Teradek - Cube/Prism encoders and Core streaming)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Remote viewing and streaming to clients

**Goal:** people off set (producers, agency, studio, VFX supervisors) watch the shoot
live with good image quality, low delay and proper security - and can talk to set.

## 1. Signal chain
Camera SDI -> **video assist** (QTAKE, Playback Pro, or the DIT) with LUT applied ->
**encoder** (Teradek Cube/Prism, hardware encoder or software in QTAKE) -> internet
(bonded cellular, site fibre, Starlink) -> **platform** -> viewers' browsers/apps.

## 2. Platforms
- **QTAKE Cloud / QTAKE Monitor**: live streams plus recorded takes with metadata for
  review; native to video assist operators.
- **Teradek Core / TV**, **Evercast**, **Sohonet ClearView Flex** (low-latency, secure,
  often used for post sessions too), **Frame.io Camera to Cloud** (proxies uploaded
  in near-real time for editorial and review, not a live stream).
Choose by latency need (directing remotely needs <1 s; reviewing can tolerate seconds),
security requirements (studio-approved, encrypted, watermarked, access-controlled),
and number of viewers.

## 3. Image quality
- Stream with the **show LUT** applied; tell viewers their screen isn't calibrated
  (laptops/phones differ). For colour-critical remote approvals use calibrated iPads/
  monitors (some platforms support HDR/colour-managed apps).
- Bitrate: 5-10 Mbps for HD drama review; more for multi-feed.
- Multiple cameras: quad split or switchable feeds; label cameras.

## 4. Communication
A talkback channel (platform chat/voice or a separate call) to a designated person
on set (producer or video assist operator) - **not** the director's headset by default.
Remote notes go through that person.

## 5. Security and policy
Watermark streams with viewer name; password-protected, time-limited links; NDA list.
Some productions forbid streaming certain scenes (nudity, spoilers) - closed-set rules
apply to streams too.

## 6. Test
Test the full chain at the location before day one (bandwidth at the actual spot,
cellular coverage). Have a fallback (lower bitrate, single camera).

## Gotchas
- Remote viewers giving notes straight into the director's ear.
- Unsecured links forwarded beyond the approved list.
- Judging colour on a phone.
- No bandwidth test; stream fails on day one.

## Verify
- [ ] Chain and platform chosen for latency and security.
- [ ] LUT applied; viewers warned about uncalibrated displays.
- [ ] Notes routed through one on-set contact.
- [ ] Bandwidth tested at location; fallback ready.
