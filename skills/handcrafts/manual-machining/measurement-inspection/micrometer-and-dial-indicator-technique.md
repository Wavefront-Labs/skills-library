---
id: handcrafts.manual-machining.measurement-inspection.micrometer-and-dial-indicator-technique
name: micrometer-and-dial-indicator-technique
category: handcrafts
field: manual-machining
product: measurement-inspection
tags: [measurement-inspection, metrology, micrometer, outside-micrometer, vernier-micrometer, ratchet-stop, friction-thimble, zeroing, setting-standard, gauge-blocks, slip-gauges, jo-blocks, wringing, dial-indicator, dial-test-indicator, dti, plunger-indicator, cosine-error, runout, tir, surface-plate, height-gauge, calipers, tenths, thermal-expansion, 20-degrees, inspection, drawing-tolerance, machinist]
level: practitioner
status: draft
description: "Read and use an outside micrometer and dial indicators correctly: zero against standards, consistent feel, temperature, cosine error, runout and checking a part against its drawing tolerance."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Micrometer and dial indicator technique

**Goal:** measure a turned or milled part repeatably to 0.01 mm (and to 0.002 mm
with a vernier micrometer and care), and decide honestly whether it meets the
drawing.

## 1. The rule of ten
Your instrument's resolution should be about one tenth of the tolerance you are
checking. A ±0.02 mm tolerance needs a 0.001–0.002 mm instrument; calipers
(0.02 mm resolution, worse in practice) are for roughing only.

## 2. Outside micrometer
**Zero first:**
1. Clean the anvil and spindle faces with a slip of paper drawn between them.
2. For 0–25 mm, close them with the ratchet and check the zero line. For larger
   frames, use the **setting standard** supplied. Adjust the sleeve with the
   C-spanner if it is off.

**Reading (metric 0.01 mm):** sleeve shows whole mm above the line and 0.5 mm
below; thimble 0–49 adds hundredths. E.g. sleeve 12 + 0.5 visible, thimble 23 →
12.73 mm. A vernier scale on the sleeve adds the third decimal: the line that
aligns gives thousandths.

**Feel:**
- Use the **ratchet or friction thimble** for the final closing, 2–3 clicks, every
  time. Consistent force is the whole game.
- On a round part, rock the micrometer gently across the diameter — the minimum
  reading is the true diameter — and along the axis for square.
- Hold the frame by the insulated pad, or in a stand; hand heat grows a 100 mm
  steel frame by roughly 1 µm per °C.
- Measure at least three positions (and 90° apart) to find taper and ovality.

## 3. Temperature
Steel grows about **11.5 µm per metre per °C**. A 50 mm part measured 10 °C warm
from machining reads ~0.006 mm big. Let parts cool to room temperature; the
reference temperature for gauges is **20 °C**.

## 4. Gauge blocks
- Check a micrometer at intermediate points (e.g. 2.5, 5.1, 7.7, 10.3, 12.9…) with
  gauge blocks to catch screw error.
- **Wring** blocks by sliding faces together with a twist; clean before and after,
  oil lightly when storing. Don't leave them wrung for days.

## 5. Dial indicators
Two kinds:
- **Plunger (dial) indicator:** reads along its axis. Plunger must be **in line**
  with the movement being measured.
- **Dial test indicator (DTI, lever type):** for runout and alignment. Set the
  stylus nearly **parallel** to the surface (within ~15°). At larger angles a
  **cosine error** makes it under-read: at 30°, multiply the reading by about 0.87.

**Runout check (lathe or on centres):**
1. Mount the indicator rigidly on a magnetic base, short arms, joints tight.
2. Preload a quarter to half a revolution; zero.
3. Rotate the part slowly by hand. **Total indicator reading (TIR)** = max − min.
4. Check near the chuck and at the far end to separate offset from bend/taper.

**Height comparison on a surface plate:** set the indicator to zero on a gauge-block
stack equal to the nominal height, then sweep the part; the reading is the
deviation from nominal.

## 6. Inspecting against the drawing
- Read the tolerance — e.g. Ø20 h7 is +0 / −0.021 mm. Use the fits table rather than
  memory.
- Measure each feature at least twice; record the readings.
- In tolerance only counts if the reading plus a margin for your measurement
  uncertainty is inside the limits — a part reading exactly on a limit is doubtful.

## Faults
- Inconsistent readings: varying force, dirt, part still warm.
- Indicator "sticks": dirty or bent plunger; tap the base lightly before reading.
- Micrometer won't zero: worn or damaged faces — send for calibration.

## Verify
- [ ] Micrometer zeroed with a clean standard before use.
- [ ] Ratchet used for every reading; three positions measured.
- [ ] Parts and instruments at room temperature.
- [ ] DTI stylus near-parallel; cosine error accounted for.
- [ ] Readings recorded and compared with the drawing limits, with margin.
