---
id: engineering-technology.aerospace-engineering.matlab-simulink.isa-atmosphere-blocks
name: isa-atmosphere-blocks
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [matlab, simulink, aerospace-blockset, standard-atmosphere, isa, coesa, atmosphere-model, geopotential-altitude]
level: practitioner
status: verified
description: "Use Aerospace Blockset ISA and COESA atmosphere blocks and the matching functions correctly, including altitude definition, non-standard days and units."
sources:
  - "MathWorks Aerospace Blockset documentation (environment blocks)"
  - "ICAO Doc 7488 standard atmosphere"
  - "US Standard Atmosphere 1976"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# ISA and COESA atmosphere blocks

**Goal:** correct density, temperature, pressure and speed of sound for a flight simulation.

## Blocks and functions
- Aerospace Blockset has an **ISA Atmosphere Model** block and a **COESA Atmosphere Model** block (US Standard Atmosphere 1976), plus blocks for temperature offsets (non-standard day). The Aerospace Toolbox function `atmosisa(h)` returns `[T, a, P, rho, nu, mu]` (temperature, speed of sound, pressure, density, kinematic and dynamic viscosity) in SI units for the ISA model; the input is geopotential altitude, valid from -5000 m to the mesopause (84,852 m) with the extended option (before R2023a only sea level to the tropopause). `atmoscoesa` is the COESA function.
- `atmosisa` takes geopotential altitude in metres (MathWorks page). ISA tables are in geopotential altitude; geometric 10,000 m is 9,984 m geopotential (0.16% lower, computed with r = 6,356,766 m). Check each block's own documentation for which altitude it expects.
- Sea level standard: 288.15 K, 101325 Pa, 1.225 kg/m3.

## Practice
1. Convert geometric altitude to geopotential where the function or block expects it.
2. Use temperature offset (delta ISA, for example +15 K hot day) for performance cases.
3. Compute Mach and dynamic pressure from the block's speed of sound and density.
4. Use `convvel`/`convlength` for unit conversion rather than hand-typed factors.

## Gotchas
- Each atmosphere block has a documented altitude range; check it for rockets and high-altitude vehicles.
- Mixing feet and metres is the most common error.

## Verify
- [ ] `atmosisa(0)` returns 288.15 K, 101325 Pa and 1.225 kg/m3 (recomputed from the ISA lapse equations); `atmosisa(11000)` returns 216.65 K and about 22,632 Pa.
