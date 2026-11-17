---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.tyre-size-selection
name: tyre-size-selection
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [tyre-size, tire-size, wheel-package, tyre-selection, etrto, load-index, speed-rating, rolling-radius, aspect-ratio, tyre-label]
level: practitioner
status: gated
description: "Select a tyre size: read the designation, compute overall diameter, check load index and speed symbol against axle loads, and trade grip, noise and rolling resistance."
sources:
  - "Reimpell, Stoll and Betzler, The Automotive Chassis (chapter list)"
  - "Pacejka, Tire and Vehicle Dynamics (chapter list); ETRTO standards manual (https://www.etrto.org); confirm current editions"
  - "https://lexaris.de/library/tableofcontents/2050125"
  - "https://lexaris.de/library/tableofcontents/2050141"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Tyre size selection

## 1. Read the designation
Example 225/45 R17 94W: 225 = section width (mm), 45 = aspect ratio (sidewall height as a percentage of width), R = radial, 17 = rim diameter (inches), 94 = load index, W = speed symbol. Load index and speed symbol are table-looked-up in the ETRTO/tyre standards (tables not checked (gated: unconfirmed, source is paywalled or blocked)); the index is not the load in kg but maps to it.

## 2. Overall diameter and rolling radius
Overall diameter D = rim diameter (25.4 mm per inch) + 2 x width x aspect ratio. Example: 17 in = 431.8 mm; sidewall = 225 x 0.45 = 101.25 mm; D = 431.8 + 202.5 = 634.3 mm (computed). Loaded and dynamic rolling radius is smaller than half of D (deflection and speed growth); use the tyre supplier's measured rolling circumference for speed and distance calibration. Keep overall diameter within a small tolerance of the original when changing sizes (speedometer, ABS, final drive).

## 3. Load and speed capability
Required load index must cover the heaviest axle load at the vehicle's maximum permissible mass, with extra capacity for dynamic loads and the standard's rules for each application (extra-load/reinforced tyres, commercial tyres, speed derating of load capacity at high speed). Speed symbol must be at least the vehicle's top speed (or the regulatory limit if the vehicle is limited). Confirm against the tyre fitment regulation of the market (for example UN Regulation No. 30, pneumatic tyres for motor vehicles and their trailers, and No. 54, pneumatic tyres for commercial vehicles and their trailers, in regions adopting the UN regulations).

## 4. Trade-offs
- **Wider:** more lateral grip and braking in dry, but more rolling resistance and aerodynamic drag, wider noise footprint, more hydroplaning risk, heavier.
- **Taller sidewall:** better ride and rim protection, softer steering response.
- **Lower profile and larger rim:** sharper steering, less sidewall damping, more road noise from stiffer tyres, heavier wheel and unsprung mass.
- **EV-specific:** low rolling resistance tyres for range and tyre noise tuning, higher load capacity for heavy packs, reinforced sidewalls.
- **Tyre label:** in the EU, tyre labelling regulation covers rolling resistance, wet grip and noise classes; confirm the current regulation for the market and target classes.

## 5. Package check
Check clearance to arches, struts, arms and brakes at full bump, rebound and steer (see wheel offset and clearance), snow-chain clearance if required, spare wheel. Check the effect on kerb height, ride height, effective gear ratio and brake size.

## Verify
- [ ] Overall diameter and rolling circumference computed and compared to baseline.
- [ ] Load index covers axle loads with the applicable margin; speed symbol covers top speed.
- [ ] Label class and approval markings confirmed for market.
- [ ] Package clearance and steering lock checked.
