---
id: creative-arts.animation.storywriting.shotlist-boarding
name: shotlist-boarding
category: creative-arts
field: animation
product: storywriting
tags: [shotlist, boarding, coverage, shot-size, runtime, calibration, storyboard]
level: practitioner
status: verified
description: "Decompose scene-sequence-shots: shot sizes, coverage, calibrated shot counts (~8-11/min) to hit target runtime."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SKILL: Shotlisting & boarding (teleplay → shot plan) — expert

Break a teleplay into the actual SHOTS that get built, with location, action, dialogue,
camera, and **duration** — so the episode's runtime is planned, not accidental, and
shots can be mass-produced and tracked. Pairs: `novel-to-teleplay`, `screenwriting-craft`,
`../pipeline/shot-episode-structure`, `../blender/layout-blocking`, `../blender/camera-cinematography`.

## Why shotlist before building
- It's the only way to know the episode will hit **10–15 min** BEFORE rendering 100 shots.
- It's the production database: each row = one buildable shot = one tracked task.
- It catches coverage gaps (every line needs a shot; every beat needs an establishing +
  reaction) and pacing problems on paper, where they're free to fix.

## Decompose: scene → sequence → shots
Each teleplay scene becomes a **sequence** of shots. Give every beat enough coverage:
- **Establishing** (wide) to orient the space.
- **Singles** on each speaker; **OTS/two-shot** for dialogue; **reactions** (the listener
  often matters more than the speaker).
- **Inserts/cutaways** (the orange in the drain, the counter, the seam) — the key images.
- **Re-establish** after movement. Button shot on the act-out.
Match-cut and vary shot size (wide/med/close) — never two same-size shots back to back.

## Duration budgeting (how you hit runtime)
- Estimate each shot's seconds. **Dialogue shots ≈ the VO length** (generate VO first;
  it gives real durations) + handles (~0.3–0.5s head/tail). **Action/held shots**: time
  them by the beat (establishing 3–5s, a reaction 1–2s, a reveal hold 2–4s).
- Sum per sequence, per act, per episode. Animation plays slower than you think; a
  12-min episode is typically **90–130 shots** averaging 4–8s (≈8–11 shots/min).
- If total < target, the script is thin — add beats/held moments (per screenwriting-craft),
  don't pad with dead air. If > target, cut shots or tighten.

### VERIFIED CALIBRATION (2026-10-13, Ep1–4) — the estimate failed short
**Lesson:** per-shot *seconds* were accurate; **shot COUNT was ~40% too low**, so
episodes came in ~3.5–4 min against a 6–8 min target. Measured: a dialogue-dense
novel-part adaptation at **~31–49 shots = 3.3–4.2 min**. Dialogue VO is the *floor*,
not the runtime — a 10-line scene is only ~90s of talking.
**Fix the estimate:**
- **Target shot count FIRST from runtime** (≈8–11 shots/min): 6–8 min = **~55–80 shots**,
  10–12 min = ~90–130. Author to that count, don't discover it after.
- **Coverage is the dial that fills the gap** between VO-floor and target: per dialogue
  beat add a **reaction** (listener), per location an **establishing** + at least one
  **atmosphere/mood** shot, per key image a lingering **insert**. ~2–3 non-dialogue
  shots per dialogue shot in a moody show.
- **Hold longer in a slow-burn tone:** establishing 4–6s, emotional/reveal holds 4–7s,
  silent dread beats 3–5s. Thin "plot-only" cutting (2–3s each) is what underran.
- **Sanity check before building:** `(target_min × 9) ≈ shots needed`. If the authored
  list is below that, add coverage until it clears, THEN build.

## Shotlist row schema (one per shot) — store as JSON/CSV, drives the builder
```
id            EP01_SQ03_SH020           # episode/sequence/shot
seq           "Act3 - the alley"
location      alley                      # -> assets/sets/<location>.blend
cast          [pixel, ivy]                 # -> locked assets to append
size          WIDE|MED|CLOSE|OTS|INSERT
camera        "push in slow" / lens / height
action        "Pixel enters from the street mouth, settles"
line_id       pixel_l01                   # -> VO wav + rhubarb json (lip-sync)
dialogue      "A new viewer! ..."        # for VO + reference
dur_s         5.5
fx            ["green seam", "counter"]
status        todo|vo|built|rendered|final
```
This row is exactly what the headless shot-builder consumes (see blendercraft-headless:
shot spec = JSON). Keep the shotlist in the episode folder; it IS the production tracker.

## Boarding (optional but cheap)
A rough board (stick figures / blockout screenshots) per shot locks composition before
animation. For our 3D pipeline, a fast **blockout key-still** per shot (layout-blocking)
serves as the board — build-still-approve before animating. Assemble stills in order =
a **boardomatic/animatic** (still images cut to the VO) to feel pacing before full render.

## Pipeline order (per episode)
1. Shotlist the whole teleplay (this skill) → durations sum to target.
2. Generate **all VO** (locks real dialogue durations → update dur_s).
3. Animatic: key-still per shot cut to VO (catch pacing).
4. Build sets + hero assets needed by the list.
5. Batch-build & render shots (shot chunks, never one giant job).
6. Picture-edit shots together (editing skill) + sound + grade + encode.

## Self-check
- [ ] Every teleplay line & beat has at least one shot?
- [ ] Coverage: establishing + singles + reactions + key inserts per scene?
- [ ] Shot sizes varied (no two same-size cuts adjacent)?
- [ ] Durations summed to the 10–15 min target (from VO where possible)?
- [ ] Each row has location+cast+camera+line_id → directly buildable?
- [ ] 180° line / screen direction noted per sequence?

## Pitfalls
- No shotlist → can't tell if you'll hit runtime until it's too late.
- Only speaker singles, no reactions → lifeless, undercut emotion.
- Guessing durations without VO → timing wrong, lip-sync misfits.
- Same shot size repeatedly → flat, TV-cheap. Vary size and angle.
