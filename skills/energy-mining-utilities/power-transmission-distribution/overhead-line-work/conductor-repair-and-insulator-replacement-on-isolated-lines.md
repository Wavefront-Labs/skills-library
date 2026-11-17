---
id: energy-mining-utilities.power-transmission-distribution.overhead-line-work.conductor-repair-and-insulator-replacement-on-isolated-lines
name: conductor-repair-and-insulator-replacement-on-isolated-lines
category: energy-mining-utilities
field: power-transmission-distribution
product: overhead-line-work
tags: [overhead-line-work, overhead-lines, linework, lineworker, lineman, linesman, pole-top, pole-climbing, pole-inspection, pole-top-rescue, fall-arrest, conductor-repair, compression-splice, full-tension-splice, repair-sleeve, acsr, aaac, insulator-replacement, pin-insulator, strain-insulator, hoist, come-along, wire-grip, portable-earths, working-earths, storm-restoration, downed-wires, backfeed, distribution-lines]
level: practitioner
status: draft
description: "Repair damaged conductor and swap insulators on an isolated, earthed overhead line: pole checks before climbing, splice vs repair sleeve, taking load off hardware, storm-day traps."
sources:
  - "General utility overhead-line practice as described in distribution-line construction manuals and connector manufacturers' installation instructions; paraphrased, no single source"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Conductor repair and insulator replacement on isolated overhead lines

**Goal:** restore a damaged span or failed insulator so it holds mechanically and
electrically for decades, without anyone being hurt by stored load, backfeed or a
bad pole. This covers de-energised work only; live methods are in
`energy-mining-utilities.power-transmission-distribution.live-line-work.rubber-glove-and-hot-stick-work-within-approach-limits`.
Your employer's line-work rules, switching instructions and connector datasheets
override anything here.

## 1. Before anyone leaves the ground
- **Access permit in hand** for the exact section, and you have personally seen it is
  isolated: test for dead with an approved detector (prove the detector on a known live
  source or prover before *and* after), then apply **working earths on every side of the
  worksite** — between you and every possible source, including LV backfeed from
  customer generators and paralleled circuits.
- **Check the pole before climbing:** look for ground-line rot (sound with a hammer —
  a dull, hollow note is a warning), cracks, burn damage, leaning, missing or slack guys,
  and woodpecker or termite damage. A pole that is about to lose a conductor's tension
  can snap when the line is cut. If in doubt, support it (guy, pole-mounted support, or
  crane/EWP) before releasing any tension.
- Rescue readiness: a named second person on the ground who can perform a pole-top or
  EWP-basket rescue, rescue kit at the base, and a plan for how to lower a casualty.

## 2. Conductor repair: sleeve or splice?
Decide after inspecting the damage closely (bring it to you in a wire grip if needed):

| Damage | Usual repair |
|---|---|
| A few outer strands broken, steel core intact | **Repair sleeve** / armour rods over the damage |
| Many strands broken, core damaged, burn-down, or conductor parted | Cut out the damage and fit a **full-tension compression (or automatic) splice** |
| Damage within a clamp or at a support | Move the repair: splices and sleeves are generally kept out of clamps and away from supports |

Thresholds vary by manufacturer and utility (a common rule is that a repair sleeve is
only for limited outer-layer damage, roughly up to about a third to a half of the outer
strands, with no core damage). **Treat those numbers as unconfirmed; use your standard.**

Compression splice routine:
1. Take the tension with wire grips and a hoist/come-along rated for the conductor's
   tension, with a safety strap so a slipping grip cannot whip.
2. Cut square; wire-brush aluminium until bright (the oxide film is what makes joints
   run hot), apply the inhibitor compound the connector specifies.
3. Mark insertion depth on the conductor so you can see it didn't creep during crimping.
4. Use **the die stamped for that connector**, crimp in the sequence the datasheet gives
   (usually from the centre outward), overlapping bites as specified. Check every crimp
   with the go/no-go gauge.
5. Many utilities limit to one splice per conductor per span and keep it clear of the
   middle of a road crossing; follow your rule.

## 3. Replacing an insulator
- **Take the load off before undoing anything.** For a suspension or strain string,
  rig a hoist or strain carrier to carry the conductor; for a pin/post insulator, lift
  the conductor slightly with a lifting arm or rope.
- Inspect what you're bolting back onto: pins, crossarm bolts, clevises and cotter
  pins wear too. Never reuse a bent pin or a corroded cotter.
- Fit the replacement, transfer the load back slowly, and watch the hardware settle.
- Polymer insulators: don't grab or stand on the sheds, and check for tracking or
  shed tears before reusing any.

## 4. Storm restoration traps
- **Every downed wire is live** until you have isolated, tested and earthed it.
  Communication and fence wires can be energised by contact with power lines.
- Backfeed from portable generators is real; earths protect you, assumption doesn't.
- Trees still under tension against a line can spring when cut; get them de-tensioned
  first. Fatigue is the main hazard on long storm shifts — enforce rest limits.

## Verify
- [ ] Permit, test-for-dead (with prover before and after) and earths on every side are done.
- [ ] Pole and guys checked; tension released only once the pole can take it.
- [ ] Repair type chosen from the damage, not habit; die matches the connector.
- [ ] Every crimp gauged; conductor cleaned and inhibited; insertion marks unmoved.
- [ ] Insulator hardware inspected and load transferred back smoothly.
- [ ] Earths removed and permit cancelled in the right order before re-energising.
