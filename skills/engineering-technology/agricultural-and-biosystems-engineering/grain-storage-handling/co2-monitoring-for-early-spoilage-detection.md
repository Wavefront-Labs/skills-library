---
id: engineering-technology.agricultural-and-biosystems-engineering.grain-storage-handling.co2-monitoring-for-early-spoilage-detection
name: co2-monitoring-for-early-spoilage-detection
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: grain-storage-handling
tags: [agricultural-and-biosystems-engineering, grain-storage-handling, co2-monitoring, aeration-control, storage-monitoring, carbon-dioxide, early-warning, spoilage-detection, grain-respiration]
level: practitioner
status: verified
description: "Use CO2 sensors in stored grain to detect early biological activity, set baselines, alarm levels and sampling points, and combine with temperature cables."
sources:
  - "Navarro & Noyes, The Mechanics and Physics of Modern Grain Aeration Management"
  - "Sinha & Muir, Grain Storage: Part of a System"
  - "NOAA Global Monitoring Laboratory, Trends in atmospheric CO2 (https://gml.noaa.gov/ccgg/trends/)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CO2 monitoring for early spoilage detection

**Goal:** catch respiration of moulds, insects and grain before temperature cables show a problem.

## Principle
Grain, insects and fungi respire, producing CO2. Warm moist grain produces more. A CO2 reading above the baseline in the headspace or exhaust air indicates activity.

## Setup
1. Sensor type: infrared (NDIR) CO2 sensors, inside the bin headspace or in the exhaust duct, sampled during or after fan operation; follow the vendor for calibration.
2. Baseline: clean outdoor air is about 425 ppm (NOAA Mauna Loa monthly mean 426 ppm for September 2026; air near plants and towns is higher); record the bin's baseline when grain is known to be sound and at the same operating condition (fan on or off).
3. Alarm levels: set from baseline and the vendor's guidance (sustained readings well above baseline; any ppm alarm figure is bin- and vendor-specific (gated: unconfirmed, source is paywalled or blocked)).

## Interpretation
- Spikes after fan start can be flushing of stored CO2; compare with the same operating state.
- Rising trend over days or high compared with other bins suggests spoilage even at normal temperatures.
- Insects increase CO2 production at low moisture where moulds are inactive; follow up with sampling.

## Action
Inspect the grain, probe samples and moisture, run aeration to cool, and consider unloading or treatment if confirmed.

## Gotchas
- Carbon dioxide is also a hazard: bins and headspaces can be oxygen-deficient; follow confined-space rules and do not rely on sensors alone for entry safety.

## Verify
- [ ] Alarm test with a calibration gas and documented response procedures.
