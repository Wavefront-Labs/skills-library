---
id: manufacturing-production.printing-production.offset-press-operation.makeready-ink-water-balance-and-running-to-the-ok-sheet
name: makeready-ink-water-balance-and-running-to-the-ok-sheet
category: manufacturing-production
field: printing-production
product: offset-press-operation
tags: [offset-press-operation, offset-printing, lithography, sheetfed, web-offset, heidelberg, komori, manroland, koenig-bauer, makeready, ink-water-balance, fountain-solution, dampening, scumming, toning, emulsification, ink-keys, ink-zones, register, fan-out, blanket, plate, packing, density, solid-ink-density, dot-gain, tone-value-increase, ok-sheet, colour-ok, press-check, cip3, ppf, waste-sheets]
level: practitioner
status: draft
description: "Make ready a sheetfed offset press and run it to the OK sheet: plates and blankets, ink presetting, achieving ink-water balance, register and density targets, then holding colour at speed."
sources: ["ISO 12647-2 offset process control (general reference)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Offset: makeready, ink-water balance and running to the OK sheet

**Goal:** go from last job off to saleable sheets with the minimum waste, then keep
every sheet matching the OK sheet for the whole run.

## 1. Makeready sequence (sheetfed)
1. **Job data in:** load the CIP3/CIP4 (PPF/JDF) ink-key presets from prepress, sheet
   size, stock thickness. Presets get you to ~80–90% of final ink; without them you
   are guessing zone by zone.
2. **Wash-up** blankets and impression cylinders (automatic wash), and rollers if
   changing to a lighter colour or special.
3. **Plates:** check each plate against the job ticket (job, colour, version) before
   hanging. Automatic plate changers save minutes; still check for plate damage and
   that plates are fully clamped and square.
4. **Feeder and delivery:** set pile height, suckers, air blast, side lay, sheet
   size and delivery joggers for the stock. Most early waste is feeding trouble.
5. **Pressures:** set for stock thickness (on modern presses, entered numerically;
   check blanket packing on older ones — over-packed blankets cause slur and dot gain).
6. **Ink up and dampen,** then pull sheets to bring up colour and register.

## 2. Ink-water balance
Offset works because image areas take ink and non-image areas take water. The target
is the **minimum water that keeps the plate clean**.
- **Too little water:** scumming/toning — ink in non-image areas, filling in shadows,
  dirty margins. Raise dampening a little.
- **Too much water:** washed-out, mottled solids, snowflaking, ink emulsifying (ink
  looks short and pale), water marks, curl and register trouble on paper.
- Find it by running down the dampening until the plate just starts to tone, then
  back up a few points. Re-check after the press warms up — roller temperature changes it.
- **Fountain solution** is controlled chemistry: check conductivity and pH (commonly
  around pH 4.8–5.5 for conventional systems — follow the supplier) and alcohol/IPA
  substitute level, and temperature (chillers ~10–15 °C typical). Drift in any of these
  shifts the balance.

## 3. Register
- Check register marks with a loupe (or camera system). Correct circumferential and
  lateral first, then diagonal (cocking) if the press allows.
- **Fan-out:** paper stretches as it absorbs water through units; later colours
  misregister towards the tail and sides. Less water helps; some presses have
  fan-out compensation.
- Doubling/slur (shadow images) is not register — look at blankets, packing and
  pressures.

## 4. Bringing colour to OK
1. Measure solids in the colour bar with a densitometer or spectro (scanning on the
   console where available). Aim for the job's **target densities or Lab values**
   (per ISO 12647-2 or the G7/proof aim the job is printed to).
2. Adjust ink keys **zone by zone**, small moves, and wait several sheets (10–20+) for
   the ink train to respond before judging. Over-correction drives oscillation.
3. Check **dot gain/TVI** on 50% patches and **grey balance** — if solids are on target
   but greys are wrong, the problem is plate curve or press condition, not ink feed.
4. Compare the sheet to the **proof** under the viewing booth (D50, ISO 3664 light).
5. Customer or supervisor signs the **OK sheet**: date, time, signature, comments.
   Keep it at the console.

## 5. Holding it during the run
- Pull a sheet every few hundred (or per site interval), measure, compare to the OK
  sheet and the targets. Closed-loop colour systems automate this; still look.
- Watch for **hickeys** (spots from dried ink/paper debris) — clean the blanket or
  plate; for **ghosting** and **set-off** in delivery, adjust spray powder, pile height
  or ink film.
- Fountain solution and ink top-ups keep levels steady; low ink in a duct changes feed.

## Gotchas
- Chasing a colour by adding ink when the real issue is too much water (emulsified ink).
- Judging colour on wet sheets: density drops as ink dries ("dry-back"); learn your
  stock's dry-back.
- Changing many keys at once makes it impossible to see what worked.

## Verify
- [ ] Plates checked against the ticket before hanging.
- [ ] Dampening set to the toning point plus a small margin; fountain solution in range.
- [ ] Solids and TVI measured to job targets; grey balance checked.
- [ ] OK sheet signed and at the console.
- [ ] Periodic pulls measured against OK throughout the run.

*Draft note:* pH, temperature and interval values are common ranges; follow press and
consumable manufacturer specifications.
