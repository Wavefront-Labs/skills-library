---
id: natural-sciences.biology.microbiology-methods.serial-dilution-plate-counts
name: serial-dilution-plate-counts
category: natural-sciences
field: biology
product: microbiology-methods
tags: [microbiology-methods, microbiology, cfu, colony-forming-units, plate-count, viable-count, serial-dilution, ten-fold-dilution, spread-plate, pour-plate, drop-plate, miles-misra, countable-range, 30-300, tntc, dilution-factor, enumeration, bacterial-counts, agar-plates, aseptic-technique, iso-4833, iso-7218]
level: practitioner
status: gated
description: "Count viable bacteria as CFU/mL: ten-fold serial dilutions, spread/pour/drop plating, the 30-300 countable range, weighted calculation across dilutions, and common errors."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serial dilution and plate counts (CFU/mL)

**Goal:** turn a sample with an unknown, usually huge, number of bacteria into a
defensible colony-forming-unit (CFU) count per mL or per g, with replicate plates
in the countable range.

## 1. Plan the dilution range
You need at least one dilution that gives a countable plate. If you have no idea of the
load, plate a wide range (e.g. 10⁻¹ to 10⁻⁸). Rough guides: an overnight *E. coli* broth
culture is often ~10⁹ CFU/mL; a turbid culture at OD600 ≈ 1 is very roughly 10⁸–10⁹
(strain- and instrument-dependent — calibrate your own OD-to-CFU curve).

## 2. Ten-fold series
1. Label tubes before you start. Fill each with 900 µL sterile diluent (saline, PBS or
   peptone water — plain distilled water can lyse some cells).
2. Vortex the sample; transfer 100 µL into tube 1 → 10⁻¹. Vortex well (~5 s).
3. **Fresh tip every transfer.** Carry-over from one tip shifts counts by a lot.
4. Repeat down the series. Work quickly: cells can die or multiply in diluent if left
   for long (guideline in standard methods is within about 15–30 min).

## 3. Plating methods
| Method | Volume | Notes |
|---|---|---|
| Spread plate | 100 µL on surface, spread with sterile spreader/beads until absorbed | Colonies on surface; easy to pick; dried plates absorb better |
| Pour plate | 1 mL into empty dish + ~15–20 mL molten agar cooled to ~45–50 °C, swirl | Larger volume = better sensitivity; heat can stress cells; embedded colonies smaller |
| Drop plate (Miles–Misra) | 10 µL spots, several per plate | Saves plates; countable range per spot ~3–30 colonies |

Plate each chosen dilution in at least duplicate. Include an uninoculated diluent plate as
a sterility control. Incubate inverted (lid down) so condensation does not drip.

## 4. Counting
- Countable range for a standard 90 mm plate is commonly **30–300 colonies** (some
  standards use 25–250, or upper limits around 150 for spreading organisms). Below
  ~30 statistical error is large; above ~300 colonies merge and compete.
- Plates over the limit are **TNTC** (too numerous to count). Record them as such.
- Count with a colony counter or marked-backed lid; mark each colony as counted.

## 5. Calculation
Simple case, one countable dilution:

CFU/mL = mean colonies ÷ (volume plated in mL × dilution)

Example: 10⁻⁶ tube, 0.1 mL spread, plates 152 and 168 → mean 160 →
160 ÷ (0.1 × 10⁻⁶) = **1.6 × 10⁹ CFU/mL**.

When two consecutive dilutions are both countable, many standards (ISO 7218/ISO 4833-style) use a
weighted mean: N = ΣC ÷ (V × (n₁ + 0.1·n₂) × d), where ΣC is the colonies on all retained plates from both
dilutions, V the volume plated, n₁ and n₂ the numbers of plates at the first and second retained dilution,
and d the first (less diluted) dilution factor. With the same number n of plates at both dilutions this is
ΣC ÷ (1.1 × n × V × d); for duplicates the denominator is 2.2·V·d (an earlier version of this skill
wrote V × 1.1 × d, which overstates N by a factor of n; checked: plates 150, 150 at 10⁻⁵ and 15, 15 at 10⁻⁶ give
330 ÷ (2.2 × 0.1 × 10⁻⁵) = 1.5 × 10⁸ CFU/mL, matching 150 ÷ (0.1 × 10⁻⁵)). Confirm the exact wording and countable ranges in the applicable standard (gated: unconfirmed, source is paywalled or blocked).

Report to two significant figures in scientific notation. Counts below the countable range
are reported as estimates (e.g. "est. < 3.0 × 10² CFU/mL").

## Sanity checks
- Consecutive dilutions should differ by roughly ten-fold. If 10⁻⁵ gives 200 and 10⁻⁶ gives
  90, something is wrong: carry-over, poor mixing or clumping.
- Duplicates should agree within Poisson expectations (for ~100 colonies, the standard
  deviation is about √100 = 10).

## Gotchas
- **CFU ≠ cells.** Chains and clumps (staphylococci, streptococci) each make one colony.
  Vortex or sonicate gently if the method allows.
- Spreading organisms (*Proteus*, *Bacillus*) swarm and make plates uncountable; use
  drier plates or higher agar percentage.
- Wet plates make spread inocula run together — pre-dry plates.
- Pour-plate agar too hot kills heat-sensitive organisms.

## Verify
- [ ] Sterility control plate blank.
- [ ] At least one dilution with duplicate plates in the countable range.
- [ ] Ten-fold step between adjacent dilutions roughly holds.
- [ ] Calculation shows volume plated and dilution factor explicitly; result in CFU/mL or CFU/g with 2 s.f.
