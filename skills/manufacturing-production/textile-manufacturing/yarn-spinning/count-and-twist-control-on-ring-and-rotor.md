---
id: manufacturing-production.textile-manufacturing.yarn-spinning.count-and-twist-control-on-ring-and-rotor
name: count-and-twist-control-on-ring-and-rotor
category: manufacturing-production
field: textile-manufacturing
product: yarn-spinning
tags: [yarn-spinning, spinning-mill, ring-spinning, ring-frame, rotor-spinning, open-end-spinning, oe-spinning, drawframe, sliver, roving, simplex, carding, yarn-count, ne, tex, nm, twist, tpi, tpm, twist-multiplier, alpha-e, cv-percent, uster, evenness, imperfections, thin-places, thick-places, neps, wrap-reel, lea, ends-down, piecing, doffing, traveller, spindle, autoconer, yarn-clearing, rieter, toyota, saurer]
level: practitioner
status: draft
description: "Hold yarn count and twist on ring and rotor frames: draft and twist gear logic, wrap-reel count tests, twist checks, Uster evenness reading, ends-down control and good piecing and doffing practice."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Count and twist control on ring and rotor

**Goal:** yarn of the ordered **count** and **twist** with low variation and few
imperfections, at a low ends-down rate. Count and twist errors are costly because they
show up downstream — as barré stripes in knitting or weak spots in weaving — after
whole lots are made.

## 1. Units you'll meet
- **Count**: English cotton count **Ne** (hanks of 840 yd per lb — higher = finer),
  **tex** (g per 1000 m — higher = coarser), **Nm** (metric). Know which your mill uses
  and convert carefully (Ne ≈ 590.5 / tex).
- **Twist**: turns per inch (TPI) or per metre (TPM). **Twist multiplier**
  (e.g. αe = TPI/√Ne) lets you compare twist level across counts: weaving warp yarns
  usually higher, knitting yarns lower (softer).

## 2. Where count and twist come from
- **Count = feed count × total draft.** On the ring frame the draft (change wheels or
  servo setting) turns roving into yarn; on the drawframe/simplex the drafts set sliver
  and roving hank. A wrong change wheel or roving hank shifts count for the whole frame.
- **Twist = spindle speed ÷ front-roller delivery speed** (ring). On rotor spinning,
  twist = rotor speed ÷ take-off speed.
- Upstream evenness (card and drawframe sliver CV, autoleveller performance) sets
  the floor for yarn evenness — you can't fix a bad sliver at the ring frame.

## 3. Routine tests
- **Count**: wrap reel a set length (e.g. a 120-yd lea or 100 m skein), weigh on a
  calibrated balance, calculate count and **CV % between samples**. Test per frame/side
  per shift as the quality plan says.
- **Twist**: twist tester (untwist–retwist method for singles) — check samples from
  different spindles; one bad spindle (slipping tape) gives low-twist yarn.
- **Evenness** (Uster Tester or equivalent): CVm %, thin places (−50 %), thick places
  (+50 %), neps (+200 % / +140 % for ring) per km. Benchmark against Uster Statistics
  percentiles for the count.
- **Strength/elongation** (single-yarn tester) for weaving yarns.
- Winding with **electronic yarn clearers** removes objectionable faults; clearer
  cuts per 100 km is a quality indicator too.

## 4. Ends-down and piecing (ring)
- Track **ends-down per 1000 spindle-hours**. Rising ends-down → traveller wear (change
  travellers on schedule), ring condition, humidity too low, poor roving, spindle
  vibration.
- **Piecing**: join the broken end correctly so the piecing isn't a thick spot; clear
  the waste (pneumafil) — loose fibre fly on adjacent ends creates slubs.
- **Doffing**: full bobbins doffed together (auto-doffers on modern frames), no mixing
  of counts or lots in bobbin boxes/creels; colour-coded tubes per count.

## 5. Rotor specifics
Rotor speed, opening roller speed, navel type and rotor groove shape all affect yarn.
Rotor deposits (trash/dust) cause periodic faults (moiré) — clean rotors on schedule.
Robot piecers must be calibrated; bad robot piecings are a frequent fault source.

## 6. Environment
Humidity and temperature in spinning halls strongly affect ends-down and static.
Keep RH in the mill's target band for the fibre (cotton rooms are humidified).

## Gotchas
- **Mixed lots**: bobbins from different count or cotton mixing in the same lot cause
  barré in fabric. Keep lot identity through to packing.
- Periodic faults in the Uster spectrogram point to a specific roller or gear by
  wavelength — use it to find the faulty part.

## Verify
- [ ] Count mean on target and between-sample CV within the plan limit.
- [ ] Twist within tolerance on sampled spindles; low-twist spindles fixed.
- [ ] Uster CVm/IPI within the mill's target percentile.
- [ ] Ends-down rate trended; travellers changed on schedule.

*Draft: test lengths and percentiles depend on the mill quality plan and the current
Uster Statistics edition — not verified against a specific mill.*
