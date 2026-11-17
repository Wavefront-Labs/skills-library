---
id: computing-software.qa-testing-engineering.exploratory-testing.mobile-network-condition-testing
name: mobile-network-condition-testing
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [network-throttling, offline-testing, mobile-testing, flaky-network, offline-first]
level: practitioner
status: docs-checked
description: "Test apps on poor and changing networks: offline, high latency, low bandwidth and packet loss using the Android emulator console and Chrome DevTools profiles."
sources:
  - https://developer.android.com/studio/run/emulator-console
  - https://developer.chrome.com/docs/devtools/settings/throttling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network condition testing (offline, throttled)

**Goal:** the app degrades gracefully on bad networks and recovers when connectivity returns.

## Conditions to cover
Offline from start; going offline mid-request; slow links; high latency; packet loss; Wi-Fi to cellular handover; DNS failure; very slow server responses.

## Tools
- **Android emulator console** (network characteristics are one of the things the console controls):
  - `network status` shows the current delay and speed characteristics.
  - `network delay <latency>` sets emulated latency, as a named profile (for example `gprs`) or a range in milliseconds (`network delay 40 100`). At startup use `emulator -netdelay gprs`.
  - `network speed <speed>` sets the transfer rate, as a named profile or kilobits per second (`network speed 14.4 80`). Profiles include gsm (14.4 up, 14.4 down), gprs (40.0 up, 80.0 down), edge (118.4 up, 236.8 down), umts (128.0 up, 1920 down), hsdpa, lte and full. At startup use `emulator -netspeed gsm @Pixel_API_26`.
  - `gsm data <state>` and `gsm voice <state>` set the connection state: unregistered (no network available), home, roaming, searching.
  - `network capture start <file>` and `network capture stop` record packets; the file is a bare filename saved under the AVD `console_out/` folder. From emulator 36.5 Wi-Fi traffic is handled by netsim and this command captures only legacy cellular/WAN traffic.
  - The network commands apply to Ethernet and cellular only.
- **Chrome DevTools** (Settings > Throttling): add a custom network throttling profile with a name, download and upload speeds in Kbps, latency in ms, packet loss in percent, packet queue length and a packet reordering flag. The page states the packet parameters let you throttle WebRTC applications without third-party software. The profile then appears in the Network panel throttling list. CPU throttling presets can be calibrated to approximate low- and mid-tier mobile devices.

## What to check
- Clear offline indicators; no infinite spinners (timeouts set).
- Retries do not duplicate writes.
- Offline-first apps: queued changes sync when back online; conflict handling.
- Cached content shown when offline where appropriate.
- Large downloads and uploads resume, not restart.
- Error messages are actionable.

## Gotchas
- Emulated links on a fast office network hide real-world issues; field test tier 1 apps.
- Throttling only downlink misses slow uploads; set upload speed too.

## Verify
Each key journey tested under offline, slow and switching conditions, with screenshots of the user-facing state.

## Checked
2026-11-09: checked against the Android emulator console page (network status, delay, speed, capture, gsm state; read for the network and telephony sections only, not the full 44k-character page) and the Chrome DevTools Throttling page (read in full). Removed because not confirmed this batch: the Apple Network Link Conditioner source and iOS bullets (download page is a stub), Charles, Proxyman and mitmproxy throttling, Playwright `setOffline`, the specific 3G figures and 5-10 percent loss values, and the idempotency-key advice. Tag `network-link-conditioner` trimmed.

Method: documentation only; no commands were run.
