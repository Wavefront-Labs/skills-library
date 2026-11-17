---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.low-voltage-supply-and-dc-dc-converter-sizing
name: low-voltage-supply-and-dc-dc-converter-sizing
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [dcdc-converter, dc-dc, 12v-supply, low-voltage-battery, lv-battery, power-net, alternator, 12v-battery-sizing, supply-redundancy, power-distribution, load-profile]
level: practitioner
status: gated
description: "Size the 12 V supply: electrical load profile, HV-to-12 V DC-DC converter rating, LV battery role and redundancy, setpoint control, and efficiency and EMC checks."
sources:
  - "ISO 16750-2:2023 (https://www.iso.org/standard/76119.html)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# 12 V supply and DC-DC converter sizing

## 1. Load profile
List each 12 V load with peak, continuous and duty (electric power steering, brake and stability pumps, HVAC blower, lamps, seat and window heating, infotainment, compute for ADAS, cooling pumps and fans, door and body modules). Build time-based scenarios (city night with rain and heater, highway, towing, fast charging, parked with climate control) and sum with diversity (not every load peaks together). ADAS and central compute raise baseline load substantially.

## 2. Source options
- **ICE or mild hybrid:** alternator (and in 48 V mild hybrids a 48 V to 12 V converter); battery buffers peaks and cranking.
- **EV and plug-in hybrid:** HV-to-12 V DC-DC converter (isolated buck; power rating sized to load profile plus margin, a few kilowatts being typical (gated: unconfirmed, source is paywalled or blocked)). Must work in all HV states relevant to 12 V supply and produce a controlled voltage setpoint (often about 13.5-14.5 V, temperature compensated for the LV battery (gated: unconfirmed, source is paywalled or blocked)).
- **12 V battery:** AGM, lead-acid, or lithium (often LFP) packs; provides start of vehicle systems before the HV contactors close, backup supply when the DC-DC fails, and power for safety systems during crash or fault.

## 3. Sizing
- **Converter:** continuous rating = maximum sustained load + battery charging margin (typically some amps for recharge) with derating at maximum coolant temperature; peak rating for brief spikes, or share with the battery.
- **Battery:** capacity set by backup need: safety-critical loads (steering, braking, lighting) for the safe-stop time with the DC-DC failed; plus parked drain over the required standby period (see quiescent current); plus cold start or key-on capability.
- **Redundancy:** for automated driving or steer/brake-by-wire, dual supply paths: second battery or supercapacitor, redundant converters, supply monitoring and isolation (diode or smart switch) between circuits.

## 4. Control and interaction
Converter set-point from the battery management or power manager (state of charge, temperature, load shedding); communication of load demand; soft start; load-dump and reverse-polarity protection of consumers (ISO 16750-2 electrical-load tests); noise (switching ripple and EMC) on the 12 V rail and radiated emissions; efficiency at partial load, affecting range.

## 5. Verification
Load-profile simulation (Simulink or SPICE-level for transients), bench tests of DC-DC at corner temperatures, vehicle tests with all loads on, fault tests (converter off, battery disconnected), life cycle of the battery under real load profile.

## Verify
- [ ] Load scenarios and diversity documented.
- [ ] Converter and battery sized for safe-stop with converter failed.
- [ ] Supply redundancy matches the safety concept.
- [ ] Ripple, EMC and efficiency measured.
