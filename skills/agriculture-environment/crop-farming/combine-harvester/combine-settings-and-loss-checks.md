---
id: agriculture-environment.crop-farming.combine-harvester.combine-settings-and-loss-checks
name: combine-settings-and-loss-checks
category: agriculture-environment
field: crop-farming
product: combine-harvester
tags: [combine-harvester, combine, header, harvester, draper-front, reel-speed, reel-position, cutting-height, threshing, rotor-speed, drum-speed, concave-clearance, separation, cleaning-shoe, fan-speed, chaffer, sieve, returns, tailings, grain-sample, cracked-grain, unthreshed-heads, header-loss, rotor-loss, sieve-loss, drop-pan, loss-monitor, chaff-spreader, john-deere, case-ih, claas, new-holland]
level: practitioner
status: gated
description: "Set a combine for crop and conditions: header and reel first, then threshing, separation and cleaning, adjusting one thing at a time and using drop-pan loss checks and the grain sample to steer."
sources: ["https://www.nsw.gov.au/regional-and-primary-industries/agriculture/soil/groundcover"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Combine settings and loss checks

**Goal:** a clean, uncracked sample in the tank with total losses you've *measured* —
not just believed — at a forward speed that keeps the machine full. Start from the
manufacturer's crop chart (or the in-cab automation preset), then fine-tune from
evidence. Settings differ greatly between rotary and conventional machines and between
brands; treat the numbers here as illustrations.

## 1. Order of adjustment (front to back)
1. **Header:** losses at the front can't be recovered by threshing settings.
2. **Threshing:** rotor/drum speed, concave clearance.
3. **Separation:** rotor vanes/straw walkers — mostly a load question (speed).
4. **Cleaning:** fan speed, chaffer and sieve openings.
**Change one setting at a time**, run ~100–200 m at steady speed, then check sample and
losses. Write each change down.

## 2. Header
- Cutting height: as high as gets all the heads/pods (less straw = more capacity),
  low for lodged crops and low-podding pulses (flex/draper fronts, pick-up reels).
- **Reel speed** slightly faster than ground speed (index ~1.1–1.25 commonly cited) (gated: unconfirmed, source is paywalled or blocked);
  too fast shatters heads, too slow lets crop fall forward.
- Reel position: tines just ahead of the knife, height so bats hit just below the heads.
- Feed must be even and "heads first" into the feeder; bunching causes slugging and
  rotor losses.
- Knife sections and guards sharp and tight; dull knives mean ragged cut and losses
  in tough straw.

## 3. Threshing
- Increase **rotor/drum speed** or **close the concave** to thresh more; do the reverse
  if grain is cracked or straw is broken up badly (overloading the sieves).
- Prefer adjusting rotor speed first for cracking issues and concave for unthreshed
  heads, but check your manual's logic.
- Typical tendencies: wheat/barley thresh fairly easily at moderate speeds; canola and
  pulses need lower speeds and wider concaves to avoid splitting; maize/corn needs low
  rotor speed and wide concave with special concave sections.
- Damp, green or tough straw (early morning, evening) threshes worse — settings that
  worked at 2 pm may fail at 8 pm.

## 4. Cleaning
- **Fan speed:** as high as possible without blowing grain over the back (light seeds
  like canola need low fan; heavy maize higher). Too low = trash in the sample and
  overloaded sieves.
- **Chaffer** (upper sieve) open enough to let grain through over its front two-thirds;
  **sieve** (lower) sets sample cleanliness.
- Watch the **returns/tailings** volume: heavy returns of threshed grain = sieve too
  closed or fan too low; returns full of unthreshed heads = threshing too gentle.

## 5. Measuring losses
- **Before harvest:** count pre-harvest losses on the ground in the standing crop
  (natural shedding) — subtract them later.
- **Drop pan / tray test:** a pan of known area (e.g. 0.1 m² or wider covering the full
  sieve width) dropped under the combine while running to catch rotor/sieve losses;
  count grains. Header losses: stop, back up, count grains on the ground in the cut area
  in front of where the machine was.
- Convert: `loss (kg/ha) = grains per m² × TSW (g) ÷ 100`. Example: 30 grains/m² of
  wheat at TSW 40 g = 12 kg/ha. Rule of thumb in North American units: about **15-20 wheat
  kernels per square foot ≈ 1 bushel/acre** lost (computed from TSW 30-40 g and 60 lb/bushel; kernel size changes it).
- Compare against a target (often ~1–2% of yield total) (gated: unconfirmed, source is paywalled or blocked) and split by source: header,
  threshing (unthreshed heads in the residue), separation, cleaning.
- **Calibrate the in-cab loss monitor** against these counts: the monitor shows
  relative change, not absolute loss.

## 6. Sample checks
Every tank, at first: cracked grain, unthreshed heads, white caps, chaff, weed seed,
dirt/stones (cutting too low). Feed it back into the order above.

## Gotchas
- Pushing forward speed beyond capacity raises rotor/walker losses sharply; a full but
  not overloaded machine is optimal.
- Uneven spreading of chaff and straw hurts next year's sowing — set the spreader to
  full cut width; for harvest weed seed control, set the chaff system accordingly.
- Fire risk in dry crops: blow down daily, check bearings and belts for heat.
- Settings drift as moisture changes through the day.

## Verify
- [ ] Started from the manufacturer chart/preset for the crop.
- [ ] Changes made one at a time and logged.
- [ ] Losses counted with a drop pan and ground counts, split by source, pre-harvest losses subtracted.
- [ ] Loss monitor calibrated to the counts.
- [ ] Sample checked for cracking, trash and unthreshed heads.

## Checked

- Date: 2026-10-25. Jurisdiction: no regulation involved; metric with North American conversions.
- Confirmed against: the loss formula (grains/m2 x TSW g / 100 = kg/ha, 1 g/m2 = 10 kg/ha) and worked example (30 x 40 / 100 = 12 kg/ha) were recomputed; the bushel rule of thumb was recomputed from TSW 30-40 g and 60 lb/bushel (about 15-20 kernels per square foot).
- Not confirmed: the reel index and the 1-2% loss target (no free primary source stating them was found, manufacturer manuals are not public).

Method: documentation only; no commands were run.
