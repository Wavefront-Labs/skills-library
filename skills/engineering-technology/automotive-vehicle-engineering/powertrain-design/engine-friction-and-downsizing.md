---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.engine-friction-and-downsizing
name: engine-friction-and-downsizing
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [engine-friction, fmep, downsizing, pumping-loss, friction-mean-effective-pressure, downspeeding]
level: practitioner
status: gated
description: "Quantify engine friction with FMEP, understand pumping loss, and assess downsizing and downspeeding for fuel economy and drivability trade-offs."
sources:
  - "Heywood, Internal Combustion Engine Fundamentals"
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Engine friction and downsizing

- FMEP: `bmep = imep_gross - pmep - fmep`; typical FMEP for modern gasoline engines is roughly 0.5-1.5 bar rising with speed (gated: unconfirmed, source is paywalled or blocked) (check measured data). Break it into piston/rings, bearings, valvetrain, pumps.
- Friction share is large at light load because brake output is small while FMEP is constant.
- Pumping loss: throttled gasoline engines pay at part load; reduce via Atkinson/Miller cycles, variable valve timing, cylinder deactivation, downsizing.
- Downsizing: smaller turbocharged engine runs at higher BMEP for the same power, reducing pumping and friction fraction, improving economy at light/mid load; cost/limits: low-end torque, knock, transient response, high-load enrichment, particulate and catalyst temperatures.
- Downspeeding: taller gearing lowers speed and raises load; needs adequate low-speed torque and NVH.
- Evaluate using BSFC maps in the cycle simulation to quantify gains, not rules of thumb.

**Gotchas:** real-world driving at high load reduces the downsizing benefit.

## Verify
- [ ] FMEP vs speed curve from motoring or Willans-line measurement documented.
- [ ] Cycle fuel simulation shows benefit using both baseline and downsized maps.
