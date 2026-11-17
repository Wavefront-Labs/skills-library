---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-antenna-patterns-and-polarisation
name: wifi-antenna-patterns-and-polarisation
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-antennas, antenna-gain-dbi, polarisation-mismatch]
level: practitioner
status: draft
description: "Pick internal and external antennas for ceiling, wall, high-density and outdoor APs and read azimuth and elevation patterns."
sources:
  - https://www.cwnp.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Antenna choice

- Gain (dBi) reshapes the pattern; it adds no power. Higher-gain omnis flatten the elevation lobe and create a blind zone directly beneath.
- Ceiling APs are designed to be mounted flat on a ceiling. Mounting a ceiling model on a wall changes its pattern; use wall-mount models or the vendor's mounting guidance.
- Patch or directional antennas suit high-ceiling warehouses, stadiums and outdoor links; use the manufacturer pattern plots and aim by survey.
- Polarisation mismatch costs signal; client orientation is mixed, so dual-polarised antennas are common.
- External antennas must be on the AP model's certified list; uncertified combinations can breach EIRP approval.

## Verify
- [ ] A post-install survey confirms the intended coverage footprint, not just the datasheet.
