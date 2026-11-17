---
id: computing-software.general-digital-literacy.basic-troubleshooting.running-a-speed-test
name: running-a-speed-test
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, wifi, connectivity, speed-test, slow-internet, download-speed, upload-speed, latency, ping, bufferbloat, mbps]
level: intro
status: docs-checked
description: "Measure internet speed properly (download, upload, latency), compare wired vs Wi-Fi, read Mbps against streaming needs, and gather evidence for your provider."
sources:
  - https://help.netflix.com/en/node/306
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running and reading a speed test

**Goal:** know whether "the internet is slow" is your Wi-Fi, your device or your provider.

## Run it
Use fast.com (Netflix), speedtest.net or your provider's test. Close downloads/streams and
pause cloud sync first.

## Read it
| Measure | What it means |
|---|---|
| **Download** (Mbps) | receiving data; compare with your streaming service's recommended speed |
| **Upload** (Mbps) | sending data (calls, big uploads) |
| **Latency/ping** (ms) | delay; high values hurt calls and games |
| Jitter / loaded latency | stability under load; high values = choppy calls ("bufferbloat") |
Mbps (megabits) divided by 8 = MB/s (megabytes): 80 Mbps is about 10 MB per second.

Netflix publishes recommended speeds per quality: HD (720p) 3 Mbps or higher, Full HD (1080p) 5 Mbps or higher, 4K 15 Mbps or higher. Other services publish their own figures.

## Find where the slowness is
1. Test next to the router, then where you usually sit. Big drop = **Wi-Fi coverage** problem
   (move the router higher/central, add a mesh system).
2. Test with an **Ethernet cable**. Wired fast but Wi-Fi slow = Wi-Fi. Wired slow too = line or provider.
3. Test on another device. Only one device slow = that device (updates, VPN, old Wi-Fi card).
4. Test at different times of day.

## Evidence for the provider
Screenshot several wired tests at different times and compare them with the speed promised in your
contract. If a test is slower than expected, Netflix's own advice is to contact your internet provider.

## Checked
2026-11-01. Confirmed on Netflix "Netflix-recommended internet speeds": 3, 5 and 15 Mbps tiers, Fast.com as a check, contact the provider if slower than expected. Removed: per-call and upload figures, the 50 ms threshold, 5 GHz advice, the evening-congestion and Ofcom contract-exit claims (no page read).

Method: documentation only; no commands were run.

## Verify
- [ ] You know your wired vs Wi-Fi download speed and which is the bottleneck.
