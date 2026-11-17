---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-airtime-and-legacy-protection
name: wifi-airtime-and-legacy-protection
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-airtime, legacy-protection, basic-rates]
level: practitioner
status: draft
description: "Explain why Wi-Fi capacity is airtime, not bandwidth, and how beacons, legacy clients and low basic rates reduce cell throughput."
sources:
  - https://www.ieee802.org/11/
  - https://www.cwnp.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Airtime is the real capacity

- All stations on a channel share one half-duplex medium. A slow client sending the same bytes holds the channel far longer than a fast one.
- Beacons go out at the lowest basic rate. Many SSIDs on one radio can consume a large share of airtime; cap SSIDs per radio (3-4 is a common guideline) and raise the minimum basic rate.
- Protection (RTS/CTS or CTS-to-self) engages when legacy 802.11b/g devices are heard, adding overhead for everyone.
- Neighbouring APs on the same channel defer to each other (CSMA/CA) even with no clients: co-channel contention.

## Actions
- Disable data rates below what your weakest supported client needs.
- Enable airtime fairness or band steering where the platform offers them, and test the effect.
- Measure per-radio channel utilisation at peak before adding APs.

## Verify
- [ ] Channel utilisation at peak leaves headroom (vendor guidance is often under roughly 50 percent; confirm for your platform).
