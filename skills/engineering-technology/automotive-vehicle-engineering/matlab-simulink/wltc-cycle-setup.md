---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.wltc-cycle-setup
name: wltc-cycle-setup
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [wltc-cycle, wltc, wltp, drive-cycle, speed-tolerance, cycle-class]
level: practitioner
status: verified
description: "Load a WLTC class cycle into Simulink, apply the regulation speed tolerance check, and keep phase boundaries for reporting."
sources:
  - "UN GTR 15 (WLTP) overview; confirm the current text and any regional adoption"
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
  - "https://dieselnet.com/standards/cycles/wltp.php"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Set up the WLTC cycle and tolerances

1. Cycle class depends on power-to-mass ratio; class 3 vehicles (power-to-mass ratio above 34 W/kg; 3a if maximum speed is below 120 km/h, 3b at 120 km/h or more) run a 1800 s cycle in four phases (Low, Medium, High, Extra High; 589/433/455/323 s, per DieselNet's tabulation of the GTR 15 cycle). Confirm class limits and the text edition in the regulation you are certifying to; regional adoptions differ.
2. Get the speed-vs-time table from the regulation annex (do not retype from memory); store as `timeseries` or a From Workspace block with 1 Hz samples and linear interpolation.
3. Report phase results: keep phase start/end indices so distance, energy and fuel are reported per phase and combined.
4. Tolerance: the regulation allows a band around the trace (speed tolerance in km/h and a time window). Implement as a checker: flag any sample where actual speed leaves the band for longer than permitted. Confirm the numbers in the current regulation.
5. Simulate at fixed 10 ms to 100 ms step for repeatability; interpolate the cycle at the model rate.

**Gotchas:** a model that violates the trace is not a valid consumption result; fix the driver or powertrain limits before quoting numbers.

## Verify
- [ ] Total cycle distance matches the regulation value to within rounding.
- [ ] Trace-violation flag is zero for a sufficiently powerful model.
