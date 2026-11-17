---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-predictive-vs-onsite-survey
name: wifi-predictive-vs-onsite-survey
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-site-survey, predictive-survey, validation-survey, wifi-site-survey]
level: practitioner
status: draft
description: "Pick predictive, AP-on-a-stick and validation surveys, and capture requirements before placing a single AP."
sources:
  - https://www.cwnp.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Survey types

- Requirements first: device types and capabilities, application SLA (voice, scanners, video), user density, coverage zones, security, roaming, and building construction.
- Predictive survey: model from floor plans with correctly calibrated wall attenuation. Good for budgeting; verify with a real measurement.
- Pre-deployment (AP-on-a-stick): temporary AP at planned positions to measure real RSSI/SNR/interference.
- Post-deployment validation: walk the site with the installed AP set and the actual client type, record RSSI, SNR, channel utilisation, retries, roaming points.
- Always survey with a representative client adapter; different adapters read different RSSI.

## Verify
- [ ] Deliverable includes heatmaps for RSSI, SNR and channel overlap, with AP placement, channels and power tables.
