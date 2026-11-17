---
id: agriculture-environment.irrigation-water-management.surface-irrigation.furrow-and-border-irrigation-management
name: furrow-and-border-irrigation-management
category: agriculture-environment
field: irrigation-water-management
product: surface-irrigation
tags: [surface-irrigation, flood-irrigation, gravity-irrigation, furrow-irrigation, border-check, bay-irrigation, basin-irrigation, siphons, gated-pipe, bankless-channel, advance-time, cutoff, recession, opportunity-time, tailwater, tailwater-recovery, reuse-system, deep-percolation, surge-irrigation, laser-levelling, inflow-rate, irrigation-efficiency]
level: practitioner
status: gated
description: "Run furrow and border-check irrigation well: set siphons and inflow, time advance and cutoff, measure applied depth, and recover tailwater."
sources: ["https://www.nrcs.usda.gov/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Furrow and border-check irrigation management

**Goal:** get water to the bottom of the field fast enough that the top end doesn't
drown, then cut it off at the right moment so the root zone is refilled without
huge deep drainage or runoff losses.

## The core idea: opportunity time
Every point in the field soaks for the time between water arriving (**advance**) and
water leaving the surface (**recession**). The top end always soaks longer than the
bottom. Good management makes those times as equal as possible:
- **Fast advance** (high inflow, short runs, smooth graded surface) → more even soak.
- **Rule of thumb:** water should reach the end of the run in roughly **¼ to ½ of the
  total required soak time** (the "quarter-time rule"). If it takes most of the set just
  to get to the bottom, the top end has been over-watered.

## 1. Setting inflow
**Furrows (siphons, gated pipe, pipes-through-bank):**
- Siphon flow depends on pipe diameter and *head* (water level difference between the
  supply channel and the furrow outlet, or channel level and pipe outlet if free-flowing).
  Manufacturers' and extension tables give L/s per siphon size at each head — keep a
  copy in the ute. Keep supply level steady or flow changes all set.
- Start with the maximum **non-erosive** flow. Classic guidance (Criddle) is
  `Q_max (L/s) ≈ 0.6 / S` (gated: unconfirmed, source is paywalled or blocked) with S = slope in % — e.g. 0.2% slope → ~3 L/s per furrow.
  Treat this as a ceiling, then watch for scouring.
- Once water reaches the end, you can **cut back** (halve the siphons per furrow or
  lower gated outlets) to reduce runoff for the remainder of the set.

**Border-check / bays:** inflow per metre of bay width is the setting. Bays on heavy
soils commonly run 2–5 L/s per metre width (gated: unconfirmed, source is paywalled or blocked) (local guide values vary widely — check your
district). Cut off inflow **before** the front reaches the end (often when it's 60–80% (gated: unconfirmed, source is paywalled or blocked)
of the way down) so the water stored on the surface finishes the job without ponding
at the bottom.

## 2. Measuring what happens
1. Peg stations at 0, ¼, ½, ¾ and the end of 3 representative furrows or bays.
2. Record the clock time water front passes each peg (advance) and when the surface
   drains at each (recession).
3. Measure inflow (bucket and stopwatch on a siphon outlet, or a flume) and outflow
   (flume or weir at the tail drain).
4. **Applied depth** = (inflow volume) ÷ (area). **Infiltrated** ≈ inflow − runoff.
   Compare with the depth the schedule asked for (see
   agriculture-environment.irrigation-water-management.irrigation-scheduling.soil-water-balance-scheduling).
5. Probe or dig at the top and bottom 24–48 h later: has the bottom end wetted the full
   root zone? Is the top end soaked well below it?

Adjust one thing at a time: inflow rate, set time, cutback time, or run length.

## 3. Surge irrigation (furrows)
A surge valve alternates flow between two sets in on/off cycles. Wetted soil seals
partially, so later surges advance faster over it, giving more even soak on light or
cracking-prone soils. Typical setup: cycle times starting ~30–60 min during advance (gated: unconfirmed, source is paywalled or blocked),
then shorter "cutback" cycles. Expect it to help most on long runs with slow advance.

## 4. Tailwater recovery
Runoff isn't lost if you catch it. A sump at the tail drain and a pump returning water
to the head channel (or a downstream field) can lift whole-farm efficiency a lot.
Size the sump for at least one set's expected runoff; many regions require tailwater
not to leave the property (nutrient and pesticide loss).

## 5. Field shape matters
- **Laser-level** to a uniform grade (or dead-level for basins). Low spots pond and
  scald the crop; high spots stay dry. Re-check levels every few years.
- Furrow slopes about 0.05–0.5% are usual (gated: unconfirmed, source is paywalled or blocked); run lengths on light soils are kept short
  (a few hundred metres) and on heavy clays can be much longer.
- Wheel-track furrows infiltrate slower than non-wheel ones — compare them separately.

## Gotchas
- Cracking clays take a big first "crack fill" then nearly seal — the first irrigation
  after a dry spell needs far longer than later ones.
- Late-night set changes get missed; an over-run set can waterlog the bottom end and
  kill a crop (cotton and wheat are sensitive). Use alarms or automation where possible.
- Numbers above are textbook/extension ranges, **not validated for any district** — use
  your local irrigation guide's figures for soil type.

## Verify
- [ ] Advance and recession times recorded at 5 stations; quarter-time rule roughly met.
- [ ] Inflow and runoff measured; infiltrated depth matches the schedule within ~20%.
- [ ] No erosion in furrow heads at the chosen flow.
- [ ] Bottom-end root zone wetted, top end not obviously waterlogged 48 h later.
- [ ] Tailwater captured, not leaving the farm.

## Checked

- Date: 2026-10-25. Jurisdiction: no regulation involved; local guide values vary.
- Confirmed against: nothing numeric could be confirmed from a free primary page in this batch.
- Not confirmed: the non-erosive flow formula, border flow range, cut-off point, surge cycle times and slope range (NRCS NEH 623 Ch. 4 was not fetched).

Method: documentation only; no commands were run.
