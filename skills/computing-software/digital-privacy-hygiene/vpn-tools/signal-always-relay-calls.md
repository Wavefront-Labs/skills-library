---
id: computing-software.digital-privacy-hygiene.vpn-tools.signal-always-relay-calls
name: signal-always-relay-calls
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, signal-call-relay, signal, ip-address-privacy, calls]
level: practitioner
status: docs-checked
description: "Use Signal's setting that relays all calls through Signal's servers to hide your IP address from call contacts, and know its latency trade-off."
sources:
  - "https://signal.org/blog/signal-video-calls/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Signal call relay setting

**Goal:** prevent a call recipient from learning your IP address (and rough location).

## Background
Signal originally always relayed call media through the Signal service. Newer versions can attempt a direct
peer-to-peer connection, which reduces call latency but can expose your IP address to the remote peer. Because an
IP address can often reveal a rough location such as a metro area, Signal relays a call through its servers when
you receive it from someone who is not in your address book.

## Turn it on
Signal has a setting that relays all calls through the Signal service. Look for the relay option in the app's
privacy or calls settings (exact menu names vary by platform and version; check your app).

## Trade-off
Relaying adds latency compared with a direct peer-to-peer call, which is the reason peer-to-peer exists.

## When it matters
- Calling someone who could be hostile or whose identity you cannot verify.
- Anyone whose home IP address would locate them.

## Checked
Method: docs-checked 2026-11-09 against the Signal blog post "Signal video calls" (full page read). Dropped as unconfirmed: exact menu paths, the claim that quality is only slightly lower, the VPN alternative, per-device behaviour and group-call routing. The support.signal.org source was removed because the site could not be read.
