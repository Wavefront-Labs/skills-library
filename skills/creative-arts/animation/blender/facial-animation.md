---
id: creative-arts.animation.blender.facial-animation
name: facial-animation
category: creative-arts
field: animation
product: blender
tags: [blender, facial-animation, expression, brows, eyes, blinks, eye-darts, lip-sync, visemes, asymmetry, shape-keys, drivers, micro-expression, graph-editor, acting]
level: advanced
status: draft
description: "Animate the face to ACT in Blender: emotion over visemes, brows as emotion carrier, eye aim/darts/blinks on thought, asymmetry, lip-sync that acts not flaps."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Facial animation — the face that acts (Blender)

The face is where the audience reads the thought, and a mouth that only flaps is the
"zero acting" problem at its sharpest. This skill is how to ANIMATE the face for
performance. It uses the rig the `facial-rig`/`rigging` skill built — shape keys and
driver sliders (`mouth_A`…`mouth_X`, `blink`, `brow_up.L/.R`, `eye.L/.R` aim, and
Chip's `CHIP_FACE` enum) — it does not rebuild it. Expression choices come from
`acting-performance` (the beat/subtext); this is the execution. `lip-sync` lays the
viseme track; here you make the rest of the face act ON TOP of it.

## 1. Layer emotion OVER visemes (order matters)
The viseme track from `lip-sync` is the *bottom* layer and the least important for
acting — real faces say far more with brows and eyes than with mouth shapes. Work in
passes:
1. **Visemes** (from `lip-sync`) — the mouth-shape track, already baked.
2. **Jaw + mouth corners for emotion** — a happy line pulls corners up and widens; an
   angry line tenses and narrows; the jaw opens more on stress. This is layered over
   the raw visemes, not instead of them.
3. **Brows** — the main emotion carrier (section 3).
4. **Eyes** — aim, darts, blinks (section 4) — where the thought lives.
5. **Micro-moves + asymmetry** (sections 5–6) — kill the dead stare.

Expression changes are **keyed to the beat**, not held flat for the whole shot. When
the character's thought changes (`acting-performance` beat change), the face changes —
usually the brows and eyes move 2–3f BEFORE the line, telegraphing the new thought.

## 2. Lip-sync that ACTS, not flaps
The old renderer did one mouth state per phoneme — the flap. Fix it:
- **Jaw drives, shapes shade.** Animate the jaw open/close as the big rhythmic motion
  (`jaw_master` or the jaw-open shape key) and let the viseme shape keys shade the lip
  *form* on top. Mouth = jaw rotation + lip shape, never a single shape popping per
  phoneme.
- **Anticipate plosives/closures.** The lips must already be CLOSED a frame or two
  BEFORE a B/P/M sounds — the closure anticipates the pop. Shift the `mouth` closure
  key ~1–2f earlier than the phoneme. Same for the pucker before an "oo"/"w".
- **Don't hit every phoneme.** Mouths co-articulate — fast speech blurs sounds together.
  Hold a shape across a run of quick consonants and hit only the strong/accented vowels
  and closures. One shape per phoneme reads as manic/chattery.
- **Less is more on toon mouths.** Over-articulation looks insane. Favor the open vowels
  and the closures; let the rest ride. Snap viseme swaps with CONSTANT interpolation
  (the cel look) but keep the jaw arc eased.

## 3. Brows — the main emotion carrier
If you animate one thing on the face, animate the brows. They do more acting than the
mouth. Drive `brow_up.L/.R`, `brow_down`/furrow, and inner/outer raise:
- **Shapes = emotion:** inner-up = worry/sadness/plead; outer+inner up = surprise/fear;
  inner-down+together = anger/concentration/furrow; one brow up = skepticism/doubt.
- **Brows accent the operative word** — a brow flash (quick up-and-back over ~4–6f) hits
  the stressed word and reads as emphasis/sincerity. This single move fixes a lot of
  flat dialogue.
- **Move brows on the thought change**, slightly ahead of the body and line.
- Push them hard for MD / Rick & Morty style — stylized faces live on big brow takes.

## 4. The eyes — aim, darts, blinks
The eyes are the acting. (Expanded from `acting-performance`, at face-execution level.)
- **Aim = thought location.** Key `eye.L/.R` aim (or the eye-target control). AT the
  listener = engaged; away/down = thinking/evading. Change aim on beat changes; the eyes
  move to the new thought a few frames before the body.
- **Darts, not drifts.** Snap the eye to a new target in 1–2f (near-CONSTANT / very steep
  Bezier), then hold. Eased slow eye moves read as sedated. Humans saccade.
- **Blink timing is meaning, not a timer:**
  - Blink on a **head-direction change** (blink masks the eye re-aim — matches how real
    eyes blink across saccades).
  - Blink on a **thought shift / decision** beat.
  - Idle baseline every ~3–5s only to keep them wet — never evenly metronomic.
  - Shape: ~2f closing, 1f fully shut, ~3f opening (~6f @ 24fps). A tired/heavy blink is
    slower and the open lingers; a startled blink is a sharp snap. Vary it.
  - **Eyelids follow the gaze:** lids ride down a touch when the eyes look down, up when
    up — static lids over moving eyes read as dead.
- **Pupil/convergence:** converge slightly on near targets; a tiny dilate/contract or a
  held wide eye sells shock.

## 5. Micro-moves — kill the dead stare
A perfectly still face between beats is a mannequin. Keep the face alive with small,
decaying motion (NOT the old constant sway):
- Tiny asymmetric brow/lid adjustments as the thought ticks over.
- Occasional swallow, nostril flare, lip press, cheek twitch on tension beats.
- Eyes always working — micro-darts even in a hold as the character thinks.
- These are small and PURPOSEFUL (serving the held thought) and they settle — not a
  looping idle.

## 6. Asymmetry — the naturalism switch
Symmetrical faces read as CG/dead. Break L/R on almost everything:
- Offset L/R brow height and the blink by ~1f.
- Smirk/sneer from one mouth corner; one eye slightly more open.
- A head tilt plus off-center gaze beats a dead-level symmetrical stare every time.
Build a little asymmetry into the resting/neutral expression itself, not just the poses.

## 7. Blender execution
- **Key shape keys / driver sliders:** in the dope sheet (or the Shape Keys panel ▸
  right-click ▸ Insert Keyframe on `Value`), key the viseme/expression values; or key the
  custom-property sliders on the face control bone if the rig exposes drivers. Use
  **custom-property keys** so the `lip-sync` importer and hand-keyed expression write to
  the same named channels deterministically.
- **Graph editor for snappy stylized faces:** expression and viseme swaps use
  **CONSTANT** interpolation for the hard cel snap; brow/eye *arcs* and the jaw use eased
  Bezier. Set per-channel, never globally (same rule as `twelve-principles`): a face that
  is all-eased looks mushy, all-snap looks robotic — mix them.
- **Blink as a reusable unit:** key the ~6f blink once, then copy/paste the keys to each
  blink beat (dope sheet ▸ select the blink keys ▸ Copy ▸ move playhead ▸ Paste), tweaking
  speed per mood. Don't hand-build each blink from scratch.
- **Chip (screen-face):** no mesh shape keys — animate the `CHIP_FACE` enum/driver that
  swaps drawn mouth+eye states (mint-green), CONSTANT interpolation between states; the
  same acting rules apply (brow-equivalent line, eye darts drawn, blink states).
- **Only-Show-Selected** on, isolate the face channels; animate the face as its own pass
  layered on the body (`acting-performance` order), never fighting 40 body curves.

## 8. Automated base layer: accents from the lip-sync timing (pipeline rendering)
When a renderer keys one emotion pose at frame 1 and the last frame (a hold) and lays
visemes under it, a cold viewer calls the close-up a **"talking mask"**: still face,
moving mouth. The cheapest fix that moves the needle is not hand animation, it is
deriving section-3 brow accents from timing the pipeline already has:
- **Phrase onsets from the viseme cues.** A cue that starts after a rest (closed-mouth
  `X` cue ≥ ~0.25 s) is where the voice starts a phrase; the first cue always counts.
  Those frames are where a real speaker's brows flash.
- **Pulse, don't retarget.** Key `brow_up` as base → base+~0.3 → base over ~6 f
  (half up, half back) so the shot's held emotion survives untouched between pulses.
  Swap ~30 % of onsets for a longer, smaller `squint` (narrowing on a stressed run)
  so the pattern never reads as a metronome; seed the choice per character so a
  two-shot never flashes in unison.
- Clamp values to [0,1] and never key past the last frame; the emotion's bracketing
  keys stay the outer envelope.
This is a base layer in the sense of `shot-renderer` §"Honest limits": hero beats
still get hand-keyed thought changes (sections 1, 3, 4) on top. Keep the function in
its own module so a running batch render (which re-imports the performance module
per shot) is not changed under its feet; wire it in between renders.

## Worked micro-example (face pass over a line)
Over the cop's "I'm not doing that again" from `acting-performance`: brows start low/
furrowed-worried (fear); at the decision ("I'm", ~f30) inner brows release and pull into
a firm set (resolve) over 5f, a blink at f30 masks the eye dart up to the listener, lids
settle to a steadier (slightly narrowed, determined) set, one brow a hair higher than the
other (asymmetry); jaw drives the words with closures anticipated ~1f on the "d" of
"doing"; a single slow blink at f64 in the hold. The mouth never just flaps — it's riding
under brows and eyes that carry the decision.

## Verify (pass/fail)
- [ ] **Brows carry the emotion** and flash/accent the operative word; they change on the
      thought beat, slightly ahead of the line. (fail = flat face)
- [ ] **Eyes act:** aim changes on beats, **darts (snappy) not drifts**, lids follow gaze.
      (fail = dead stare)
- [ ] **Blinks are motivated** — on head-direction/thought changes, varied shape — not a
      metronome. (fail = robotic)
- [ ] **Lip-sync acts:** jaw drives + shapes shade, **closures anticipate plosives**, not
      one shape per phoneme; snapped swaps but eased jaw. (fail = flap)
- [ ] **Asymmetry** present (L/R brow/lid/corner offset); not a mirror-symmetrical face.
      (fail = CG)
- [ ] **Micro-moves** keep the face alive in holds, decaying and purposeful — not a loop.
      (fail = mannequin or old idle-sway)
- [ ] **Pipeline shots are not masks:** a rendered close-up with a line shows brow
      activity at phrase starts, not one pose bracketing the shot. (fail = talking mask)

See `lip-sync` (viseme track underneath), `acting-performance` (the beat/subtext that
drives these choices), `facial-rig`/`rigging` (the controls), `twelve-principles`
(snap vs ease).
