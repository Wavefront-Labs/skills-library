---
id: manufacturing-production.pharmaceutical-manufacturing.solid-dose-production.tablet-compression-setup-and-troubleshooting
name: tablet-compression-setup-and-troubleshooting
category: manufacturing-production
field: pharmaceutical-manufacturing
product: solid-dose-production
tags: [solid-dose-production, oral-solid-dose, osd, tablet-press, tablet-compression, rotary-press, fette, korsch, natoli, tooling, punches-and-dies, precompression, main-compression, fill-depth, ejection-force, in-process-controls, ipc, tablet-weight, hardness, breaking-force, friability, thickness, disintegration, capping, lamination, sticking, picking, weight-variation, granulation, blending, coating, encapsulation, pharmaceutical-manufacturing]
level: practitioner
status: draft
description: "Set up a rotary tablet press, dial in weight, hardness and thickness, run in-process controls, and diagnose capping, sticking, picking and weight variation at production scale."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tablet compression: setup and troubleshooting

**Goal:** bring a rotary press (Fette, Korsch, IMA, Natoli and similar) from line clearance
to stable production with tablets inside weight, hardness, thickness and friability
limits, and know what to change when they drift. Granulation/blending upstream sets most
of what's possible here — a press can't fix a bad blend.

## 1. Setup
1. **Line clearance** signed; previous product's tooling and granules gone.
2. **Tooling inspection:** punches and dies from the tooling store, IDs matching the batch
   record; check tips for wear, chips and embossing damage; log usage. Damaged tips are
   the commonest cause of picking and cosmetic defects.
3. **Install** dies flush (dial gauge per SOP), upper and lower punches lubricated per
   the tooling SOP — sparingly; excess oil gives black specks.
4. **Hopper and feeder:** forced feeder paddle speed set per recipe; check no bridging in
   the hopper.
5. **Hand-turn** the turret a full revolution before power to catch binding.

## 2. Dialling in (start at low speed)
Adjust in this order — each mostly controls one property:
| Adjust | Mainly controls |
|---|---|
| **Fill depth** (dosing) | Tablet **weight** |
| **Main compression** (punch gap / force) | **Hardness** and **thickness** |
| **Pre-compression** | De-aeration → reduces **capping**; small effect on hardness |
| **Turret speed** | Dwell time — faster = less time under force, often softer tablets and more capping |

Set weight first, then hardness, then confirm thickness. Bring speed up in steps and
re-check after each step. Many modern presses run automatic weight control off
compression force — it still needs a correct manual set-point to start from.

## 3. In-process controls (IPC)
Frequency and sample size are set in the batch record:
- **Individual and average weight**
- **Hardness/breaking force**, **thickness**, **diameter**
- **Friability** (limit and method as in the batch record and pharmacopoeia) — less frequent
- **Disintegration** where required
- **Appearance** — embossing, edges, specks
Record every result at the time; an out-of-limit IPC triggers the reaction in the batch
record (adjust and re-test, segregate tablets since last good check, raise a deviation if required).

## 4. Troubleshooting
| Defect | Likely causes | First things to try |
|---|---|---|
| **Capping / lamination** (top splits off) | Trapped air, too much force, high speed, over-dry granules, worn dies (ring) | Raise pre-compression, lower main force, slow down; check LOD of granules; inspect dies |
| **Sticking / picking** (material on punch face/embossing) | Wet granules, worn/damaged tips, low lubricant, fine embossing | Clean/polish punches, check granule moisture, check tooling coating; escalate formulation issues |
| **Weight variation** | Poor flow, segregation, feeder speed, hopper level swinging, worn lower punches | Keep hopper level steady, adjust feeder, check punch length uniformity |
| **Low hardness** | Low force, over-lubricated blend (over-blending with magnesium stearate), high speed | Increase force within limits, slow down; flag blend time to QA |
| **Black specks** | Excess punch oil, worn seals, dirty turret | Clean, reduce oil, check guards |
| **Chipping** | Brittle tablets, ejection/take-off issues | Check ejection cam and take-off blade setting |

Don't change more than one setting at a time, and keep every change within the validated
ranges in the batch record — outside them is a deviation, not optimisation.

## Notes on the neighbouring steps (brief)
- **Granulation:** granule moisture (LOD) and particle size drive compression behaviour; ask for the release values.
- **Coating:** pan load, spray rate, inlet/exhaust temperature and atomising air
  determine twinning, picking and orange-peel; usually a separate operator role.
- **Encapsulation:** fill weight via dosing disc/tamping pin settings; check empty capsule
  separation and locked length.

## Verify
- [ ] Tooling IDs, condition and usage logged before start.
- [ ] Weight, hardness, thickness and friability inside limits at production speed, not just at setup speed.
- [ ] All settings inside the validated ranges stated in the batch record.
- [ ] Every IPC recorded at the time; any failure has its reaction documented.
- [ ] Tooling cleaned, inspected and returned with condition noted at end of batch.

## Checked

Date: 2026-10-25. Jurisdiction: general GMP practice; no jurisdiction-specific claim remains.

Removed as unconfirmed: the example IPC frequencies and sample sizes and the friability limit and pharmacopoeial references (paywalled). The remaining content is machine setup and troubleshooting craft that was not tied to a primary source, so the skill stays draft.

Method: documentation only; no commands were run.
