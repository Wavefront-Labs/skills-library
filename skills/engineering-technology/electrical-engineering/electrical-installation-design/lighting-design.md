---
id: engineering-technology.electrical-engineering.electrical-installation-design.lighting-design
name: lighting-design
category: engineering-technology
field: electrical-engineering
product: electrical-installation-design
tags: [electrical-engineering, electrical-installation-design, emergency-lighting, en-12464-1, illuminance, lighting-controls, lighting-design, lumen-method, utilisation-factor]
level: practitioner
status: draft
description: "Design interior lighting with the lumen method, illuminance targets, uniformity and emergency lighting."
sources:
  - "https://www.iec.ch/"
  - "https://www.ies.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Lighting design

1. **Targets:** maintained illuminance by task from EN 12464-1 (Europe) or IES recommendations (North America), plus uniformity (Uo >= 0.4 to 0.6 typical for tasks) and glare ratings (UGR).
2. **Lumen method:** `N = E A / (Phi UF MF)` with E lux, A area, Phi lamp lumens, UF utilisation factor (room index and reflectances) and MF maintenance factor (lamp lumen maintenance x luminaire cleanliness x room surface factor; for LED around 0.8 over life).
3. **Example:** 10 m x 8 m office at 500 lux, luminaire 4000 lm, UF 0.6, MF 0.8: `N = 500 x 80 / (4000 x 0.6 x 0.8) = 20.8`, so 21 luminaires.
4. **Layout:** check spacing-to-height ratio from the manufacturer's data; verify with a photometric simulation tool.
5. **Emergency lighting:** escape route and anti-panic lighting levels and duration (often 1 lux minimum along the route and 3 hours or 1 hour per local rule), tested monthly/annually; check the adopted code.
6. **Controls:** daylight linking, occupancy sensors, scheduling; energy codes set a lighting power density (W/m^2) limit (for example ASHRAE 90.1 or national codes).

**Verify:** measure illuminance on a grid at commissioning and compare to the design.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
