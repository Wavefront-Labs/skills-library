---
id: creative-arts.animation.blender.body-mechanics
name: body-mechanics
category: creative-arts
field: animation
product: blender
tags: [blender, body-mechanics, weight, balance, walk-cycle, run-cycle, overlapping-action, drag, follow-through, settle, overshoot, recoil, anticipation, graph-editor, physical-action]
level: advanced
status: draft
description: "Body mechanics in Blender: weight/balance, walk & run cycle keys, overlap/drag, settle/overshoot, force/recoil, and anticipation→action→follow-through on physical actions."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Body mechanics — weight, force and locomotion (Blender)

A character that doesn't carry weight reads as a puppet, and our idle-sway renders
have none. Body mechanics is the physics the audience feels even when they can't name
it: where the mass is, what pushes it, what drags behind. This is the physical
counterpart to `acting-performance`; `twelve-principles` is the keyframe grammar both
use. Everything below is keyed on the Rigify control naming from the `rigging` skill
(`hand_ik.L/.R`, `foot_ik.L/.R`, `torso`/`chest`/`hips` spine controls, `root`).

## 1. Weight and balance (the thing that's missing)
Weight is read from **how the center of mass moves**, not from the pose alone.
- The **COM sits over the support** (feet, or the hover point for Chip). A pose off its
  support must be falling or braced — otherwise it floats. Check: drop an imaginary
  plumb line from the hips; it lands between/over the contact feet, or the character is
  moving.
- Heavy = **slow to start, slow to stop, lots of ease**; the body resists changing
  velocity. Light = snappy, little ease. You sell mass in the TIMING and the ease, not
  the model.
- Weight **shifts before a step** — the hips move over the support foot before the other
  foot lifts, or the character stumbles. Every real step is a controlled fall and catch.
- On effort (lift, push), the whole body commits: knees bend, spine counter-curves,
  the move is slow-in. Nothing heavy moves fast at constant speed.

## 2. Anticipation → action → follow-through (any physical action)
The universal three-part shape. Example beats at 24fps for a **reach to grab**:
- **Anticipation (wind-up), ~4–8f:** the body gathers the opposite way first — hand
  pulls back slightly, weight loads, eyes go to the target. The bigger the action, the
  bigger the wind-up. No anticipation = the move teleports.
- **Action (the move), ~3–6f:** fast, eased OUT of the anticipation, the operative
  move. Usually the fewest frames — speed here reads as intent/force.
- **Follow-through + settle, ~6–12f:** the hand overshoots the target a touch and
  settles back; the arm's wrist/fingers drag and arrive after the arm (overlap); the
  body's counter-mass settles. The move *arrives*, never hard-stops.

Apply the same shape to a **punch** (coil → strike → recoil+settle), a **sit** (lean →
drop → squash+resettle), a **head turn** (counter-turn → turn → eyes/hair settle).

## 3. Overlapping action & drag
Loose or trailing parts (forearms, hands, hair, antennae, coat, tails) **lag the driving
part and arrive late**. This is what makes motion feel connected instead of rigid.
- **Offset the keys:** key the driver (e.g. upper arm / chest) first; copy the loose
  part's keys and shift them **+2 to +5f later** in the dope sheet (select the channel's
  keys ▸ G ▸ X ▸ type the offset). Bigger/looser/further-from-the-body = bigger lag.
- **Drag then overshoot:** the tip reaches its target AFTER the base, overshoots, and
  settles — a whip/follow curve. A chain (upper arm → forearm → hand → fingers) offsets
  progressively down the chain so it uncurls like a wave.
- **Successive breaking of joints:** on a fast arm throw, the shoulder leads, elbow
  trails, wrist trails more, fingers last. Stagger the keys down the hierarchy; never
  key the whole arm on the same frame or it reads as one stiff plank.

## 4. Settle, overshoot, force and recoil
- **Overshoot/settle** is how a move stops with life: the body goes slightly PAST the
  final pose then eases back over 4–10f (heavier = more frames, less overshoot; snappy
  toon = sharper, 1 big overshoot). In the graph editor this is a single key pushed
  past the target value with the return eased.
- **Force & recoil:** action and reaction. A character firing/pushing/landing gets a
  **recoil** back along the force line — the bigger the force, the bigger the kickback,
  decaying over a couple of beats. A landing from a fall = sharp compress (squash) on
  contact, then recoil up and settle. No recoil = the force had no weight.

## 5. Walk cycle — the four key poses
A walk is a repeating controlled fall. Build it pose-to-pose with the **four standard
keys**, then add the ups/downs. At a natural ~1-step-per-12f (24-frame full cycle for
2 steps) as a starting point — faster = fewer frames:
1. **Contact** — legs at widest split, front heel strikes, back toe about to leave.
   Arms opposite the legs (right arm forward with left leg). The classic pose.
2. **Down (recoil)** — weight comes down onto the planted front leg, knee bends, the
   **hips drop to their LOWEST** (body absorbs the fall). This is the weight pose —
   skip it and the walk floats.
3. **Passing** — the free leg passes under the body, hips at mid height, body balanced
   over the single support foot. A slight hip sway/tilt toward the support side.
4. **Up (push-off)** — the support leg straightens and pushes, **hips rise to HIGHEST**,
   propelling into the next contact.

Then:
- **Hip motion:** the hips trace a figure-up/down twice per cycle (down at each Down,
  up at each Up) PLUS a side-to-side sway and a rotation (hips lead, chest counter-
  rotates). Flat hips = robot.
- **Feet:** `foot_ik` plants dead still through contact→passing (no sliding — the #1
  walk bug), then lifts with a toe roll and the ankle leads the foot swing.
- **Arms:** swing opposite the legs, with the forearm/hand **dragging** (overlap,
  section 3) — the hand follows the arm by 2–3f.
- **Personality:** the walk IS character — bounce height, sway, head carriage, tempo.
  Chip hovers/bounces (no real walk — a float with antennae drag). A tired cop: low
  hips, little bounce, heavy down pose, long slow timing.

## 6. Run cycle
A run is a walk with **a flight frame** (both feet off the ground) and no double-support.
Keys: contact (one foot, body pitched forward) → down (deep knee compress, lowest) →
push (extend, launch) → **passing/flight** (airborne, legs tucked/crossing). Faster
timing (a stride can be ~8–12f), big vertical bob, strong forward lean, arms pump
higher and tighter. The flight frame and the deep compress are what separate a run from
a fast walk.

## 7. Blender-specific setup
- **Cycle setup:** animate ONE cycle (contact→…→contact with the last key = the first).
  Add a **Cycles modifier** per F-curve (Graph Editor ▸ select channels ▸ Channel ▸
  Extrapolation ▸ Make Cyclic, or add the Cycles F-modifier) to loop infinitely. For
  forward travel, put the cycle on the feet/body *in place* and drive the `root`
  forward separately (linear), or use "Repeat with Offset" on the location channel so
  each loop continues from the last instead of snapping back.
- **In-place vs travelling:** animate in place for a treadmill test and clean feet-slide
  first; add root travel last and match stride distance to foot plant (feet must be
  world-locked during contact or they skate).
- **Offset for overlap:** box-select a loose part's keys in the dope sheet, `G X <n>`
  to slide them n frames later than the driver. Do the whole chain with increasing n.
- **Graph-editor curve shapes = the mechanics:**
  - **Snap / hit / recoil:** steep, near-vertical tangents, or CONSTANT for a hold-then-
    pop. Use for impacts, darts, accents.
  - **Ease / weight:** flatten tangents at the extremes (slow-in/out); heavy = very flat
    (long ease), light = less flat.
  - **Overshoot:** push the Bezier handle past the key, or add a key beyond the target
    and ease the return. Watch unintended overshoot from Auto handles — use Auto-Clamped
    to stop phantom bounces, then add overshoot deliberately where you want it.
  - **Linear:** root forward-travel and mechanical/constant-speed motion only; organic
    motion is never linear.
  - **Vertical/contact channels** (hip Z) should look like a bouncing arc, not a sine —
    sharper at the down (contact), rounder at the up.
- Check the hip-Z and foot curves together in the graph editor: the down pose = hip-Z
  minimum must line up with the foot-contact plant frame.

## Verify (pass/fail)
- [ ] **Weight reads:** COM over support in stance; heavy things slow-in/out, light
      things snap. (fail = puppet/float)
- [ ] Every physical action has **anticipation → action → follow-through/settle**, not a
      straight teleport. (fail = no weight)
- [ ] **Overlap/drag:** loose parts and joint chains are offset (keys shifted later),
      arrive after the driver and settle — not keyed in lockstep. (fail = stiff plank)
- [ ] Walk has the **Down (lowest hip) and Up (highest hip)** poses and hip
      sway/rotation; feet are world-locked during contact (**no foot slide**). (fail =
      floaty robot walk)
- [ ] **Overshoot/recoil** present on stops and forces; nothing hard-stops dead. (fail = CG)
- [ ] Graph curves match intent: **ease for weight, snap for impact, linear only for
      root travel**; no phantom Auto-handle bounces. (fail = tweened mush)

See `twelve-principles`, `acting-performance` (poses carry this weight), `rigging`
(control names), `mocap-retarget` (when mechanics come from capture and need polish).
