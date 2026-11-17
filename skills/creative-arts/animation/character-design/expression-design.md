---
id: creative-arts.animation.character-design.expression-design
name: expression-design
category: creative-arts
field: animation
product: character-design
tags: [expression-design, facial-acting, expression-sheet, emotions, brows, eyes, mouth, asymmetry, blendshapes, shape-keys, visemes, pose-vs-expression, fear-joy-anger-sadness-surprise-disgust, stylized, brow-eye-expression, faigin-expressions]
level: advanced
status: draft
description: "Design a character's facial acting vocabulary: canonical emotion set, the three acting zones, asymmetry, and a named blendshape sheet for the rigger."
sources:
  - "Paul Ekman, basic-emotions research (the six universal expressions)"
  - "Gary Faigin, The Artist's Complete Guide to Facial Expression (brow/eye/mouth muscle reads)"
  - "Preston Blair, Cartoon Animation (expression construction)"
  - "Ed Hooks, Acting for Animators (pose vs expression, attitude)"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# SKILL: Expression design (facial acting vocabulary)

Design the *set of faces* a character can make — not generic emotions pasted onto a
model, but acting that is drawn into **this** character's geometry, pushed for a stylised
show, and handed to the rigger as a named blendshape set they can build without guessing.
This is the bridge between `character-design-craft` (which designs the neutral face) and
`creative-arts.animation.blender.rigging` (which builds the face system) +
`creative-arts.animation.blender.lip-sync` (which drives the visemes). Target acting bar:
Murder Drones / Arcane — faces that *act*, not emote.

If the face doesn't read at the back of the room in one frame, the shot dies. Expression
design is how you guarantee it does, for every emotion, before a single key is set.

---

## 1. Pose vs expression (get this right or everything is mush)

- **Pose = the whole body's attitude.** The silhouette, the line of action, the weight.
  Ed Hooks' rule: the audience reads the *body* first, the face second. An angry
  character is angry in the shoulders before the brow.
- **Expression = the face's contribution** to that attitude. It must *agree* with the pose
  (face and body selling the same emotion) or *deliberately disagree* (a smile on a
  defeated body = the character hiding it — the most interesting acting there is).
- Design expressions assuming the body is already doing its job. A face that tries to carry
  the whole emotion alone reads as a sticker. Note on the sheet which expressions pair with
  which body attitudes (Pixel's "forced cheer" = joy face + a slumped line of action).

Downstream: body attitude is posed on the rig (`rigging`); the face expression is a
blendshape combo on top. They are separate controls on purpose.

---

## 2. The three acting zones

Every expression is built from three independent zones. Design each zone's extremes, then
all expressions are combinations. Rigging them independently is what lets you get hundreds
of faces from a small set of shapes.

1. **Brows** — the single most powerful acting zone. Inner-up (sad/worried), inner-down
   (anger/concentration), full-up (surprise/fear), flat (neutral/deadpan). The brow
   *angle* carries more emotion than the mouth. Design a brow that has real travel range.
2. **Eyes / lids** — wide (fear, surprise, mania), narrowed (anger, suspicion, smugness),
   soft/half (sad, tired, tender), squeezed shut (joy-laugh, pain). Pupil size and
   eye-line (where they look) are part of this zone. Eyes are where the audience checks
   whether the character is *lying*.
3. **Mouth** — open/closed, corners up/down, tension (lips pressed, snarl, O). The mouth is
   the loudest but *least* trustworthy zone — a mouth can smile while the eyes don't, and
   the audience believes the eyes. Design the mouth to combine cleanly with every brow/eye
   state, and to coexist with the viseme set (§7).

**The craft move:** a real expression is driven by brows+eyes; the mouth confirms. A
beginner designs the mouth and forgets the brow — that's the dead "smiley face" read. For
any expression, pose the brow first.

---

## 3. The canonical expression set

Design the **six basic (Ekman) emotions** first — they are cross-cultural and non-negotiable
— then the show-specific extras. For each, the zone recipe (push all of these past life for
a stylised show, §5):

| Emotion | Brows | Eyes/lids | Mouth | Tell |
|---------|-------|-----------|-------|------|
| **Neutral** | flat, relaxed | open, soft | closed, relaxed corners | the baseline every other blends from |
| **Joy** (true) | relaxed/slightly up | *lower* lids raised, crow's-feet squeeze | corners up AND back, teeth maybe | the lids — a fake smile leaves lower lids flat |
| **Anger** | inner-down, pulled together (vertical creases) | narrowed, intense, lower lid tensed | pressed thin OR snarl (upper teeth) | the inner-down brow; mouth alone isn't anger |
| **Fear** | inner-up AND raised (whole brow up, pulled in) | wide, upper lid high, white showing | open, corners pulled back/down, tension | raised+drawn-together brow (vs surprise's flat-up) |
| **Sadness** | inner-up, outer-down (the "bridge") | soft, upper lid droops, looking down | corners down, lower lip maybe up/out | inner-up brow is *the* sadness signal |
| **Surprise** | full-up, arched, *not* drawn together | wide, lids high | jaw drops, O-shape | brief; blends instantly into fear/joy/anger |
| **Disgust** | lowered, inner-down-ish | narrowed, lower lid up | upper lip raised (sneer), nose wrinkle | upper-lip raise + nose; often asymmetric |

**Fear vs surprise** is the one everyone confuses: surprise brows go *up and flat/arched*;
fear brows go up *and pull together* (inner-up). Design them distinctly or the character
can only ever look startled.

**Show-specific extras** — design the ones this cast actually needs, not a generic pile:
- **Deadpan / Rick-tier contempt** — flat brow, half-lids, flat mouth. The absence of
  expression *is* the expression. Needs a face designed to read "nothing" on purpose.
- **Forced cheer / mask slipping** — joy mouth, neutral-or-sad eyes (the lie, §2/§4).
- **The one-frame crack** (Pixel) — a signature single-frame break in the mask (screen
  glitch + inner-up brow) that only ever appears for 1 frame. Design it; it's canon.

---

## 4. Asymmetry (the difference between emoting and acting)

Symmetric expressions read as *illustrations*; asymmetric ones read as *performances*.
Faigin's point: real faces rarely fire muscles evenly.

- **One raised brow** (skepticism, doubt), **a one-sided smirk** (smugness, mischief —
  Rick's default), **a lopsided grimace** (discomfort). These are entire characters' worth
  of attitude and they are impossible with a symmetric face.
- Design asymmetry into the *key poses that need it* (smirk, skeptic, sneer) and keep the
  big emotions (full joy, full fear) symmetric where the muscle really is symmetric.
- This forces the rig: **left/right-split blendshapes** (`brow_up.L`/`brow_up.R`,
  `smile.L`/`smile.R`), not single-slider symmetric shapes. Decide this now so the rigger
  builds split shapes from the start — retrofitting splits later is a rebuild.

---

## 5. Pushing extremes for a stylised show

A stylised series is not a realistic drama. A naturalistic brow-raise disappears at thumbnail
size. **Caricature the expression the way you caricatured the design.**

- Push past anatomical truth: brows that leave the head on surprise, pupils to pinpricks on
  shock, a mouth that opens past the jaw. The *shape* of the expression must read as a bold
  silhouette, same discipline as the character silhouette (`character-design-craft` §3).
- **Each expression has its own silhouette and its own cel shadow.** Black out the
  expression — does the emotion still read with no interior detail? The angry brow should
  carve a recognisable dark shape; the joy-squint should change the eye silhouette.
- **Settle vs peak.** Design two levels of the strong emotions: the *peak* (pushed to
  eleven, held 1–2 frames) and the *settle* (the sustainable read it eases back to).
  Animation hits the peak then settles; if you only design the settle it never lands, if
  you only design the peak it's exhausting.
- Keep it on-model: the pushed expression must still be unmistakably *this* character
  (`character-design-craft` consistency law). Push the acting, not the identity.

---

## 6. The expression sheet (the deliverable)

A grid artifact that locks the vocabulary. It becomes a row on the
`model-sheet-turnaround` and a direct spec for the rigger.

1. **Neutral at top-left** as the reference all others deviate from (same head size, same
   3/4-or-front angle for all cells — consistency so deltas are comparable).
2. **The 6 basics + the show-specific extras**, each at *peak*, labelled.
3. **Zone callouts** on at least the tricky ones: an arrow/note on the brow angle, lid
   height, mouth tension — so the rigger sculpts the right muscle, not an approximation.
4. **The asymmetric key poses** (smirk, skeptic, sneer) shown explicitly as L/R-split.
5. **Blink + half-blink**, and the **settle** version of 2–3 strong emotions (§5).
6. **Combination demonstrations** — e.g. "anger brow + joy mouth = the mask", to prove the
   zones combine cleanly and to show the rigger which combos must not collide.

Draw them *on this character*, never trace a generic chart — a round-faced character's
anger is a different shape from a sharp-faced one's. The expression is designed, not applied.

---

## 7. Mapping to blendshapes / shape keys (hand-off spec)

The sheet is only useful if the rigger can build it deterministically. Name the shapes now,
in the convention `creative-arts.animation.blender.rigging` already uses (face props on a
control bone / face-UI panel). Two layers:

**Expression blendshapes** (combine freely with visemes):
```
brow_up.L      brow_up.R        # surprise / fear / skeptic (split)
brow_down.L    brow_down.R      # anger / concentration (split)
brow_sad.L     brow_sad.R       # inner-up — sadness/fear/the crack (split)
lid_wide.L     lid_wide.R       # fear / surprise / mania
lid_squint.L   lid_squint.R     # anger / joy-squint / suspicion
lid_soft.L     lid_soft.R       # sadness / tenderness / tired
blink.L        blink.R          # + a combined `blink` convenience driver
smile.L        smile.R          # joy (split enables the smirk)
frown.L        frown.R          # sadness / displeasure
mouth_open     mouth_tense      # jaw-drop / pressed-lips tension
sneer.L        sneer.R          # disgust (asymmetric upper-lip raise)
nose_wrinkle                    # disgust
```

**Viseme shapes** — the *separate* lip-sync set, do not overload the expression mouth
shapes with phonemes. Rhubarb's 9: `mouth_A mouth_B mouth_C mouth_D mouth_E mouth_F
mouth_G mouth_H mouth_X` (driven with CONSTANT interpolation — hard swaps, no oscillation —
per `creative-arts.animation.blender.lip-sync`).

Rules for the hand-off:
- **Expression zone and viseme zone must coexist.** The character talks (visemes) *while*
  emoting (brows/lids). Keep brows/lids fully independent of the mouth so an angry line can
  be delivered: `brow_down + lid_squint + mouth_D`. If a viseme and an expression-mouth
  shape both drive the same vertices, define the additive/combine behaviour explicitly so
  they don't cancel.
- **Split L/R everything that §4 needs asymmetric**; provide a combined convenience driver
  (`blink`, `smile`) for the symmetric common case so animators aren't keying two sliders.
- **Each named shape maps to one labelled cell** on the expression sheet — the rigger sculpts
  to that drawing, not to their idea of "anger".
- **Shader-faced characters (Pixel):** the "blendshapes" are drawn/emissive mouth+eye
  states swapped/blended via a texture driver, *same names, same set* — the rigger wires a
  `a production character_FACE` enum to the same vocabulary (`rigging` §face, `character-blockout` §face).

---

## Verify

A reviewer passes the expression design only when all hold:

- [ ] **All 6 basics present and distinct** — especially fear≠surprise (brow drawn-together
      vs flat-up) and joy's *lower-lid squeeze* present (not a mouth-only smile).
- [ ] **Brow-leads check:** cover the mouth on every cell — does the emotion still read from
      brows+eyes alone? (If an expression dies with the mouth hidden, it's a sticker.)
- [ ] **Black-silhouette per expression:** fill each face cell black — the emotion reads from
      the expression's silhouette/shadow shape with no interior detail (§5).
- [ ] **Thumbnail read:** downscale the sheet to ~64px cells — each emotion still
      distinguishable (ties to `character-design-craft` §9).
- [ ] **Designed-on-character:** expressions use this character's actual geometry, not a
      traced generic chart.
- [ ] **Asymmetry:** at least the smirk/skeptic/sneer shown as L/R split; big symmetric
      emotions kept symmetric (§4).
- [ ] **Peak + settle** designed for the strong emotions (§5).
- [ ] **Named blendshape set** written out (§7), split where §4 requires, with a combined
      convenience driver for symmetric cases.
- [ ] **Expression + viseme independence proven:** at least one combo cell shows a strong
      brow/lid expression delivered over a speaking viseme (e.g. `brow_down + mouth_D`),
      with no vertex collision between the two zones.
- [ ] **Show-specific extras** (deadpan/forced-cheer/crack) designed, not just the Ekman six.

**Runnable check (the rigger can build it without asking you):** list every name in §7 and
confirm each has exactly one labelled cell on the sheet, and each cell has a name. A mismatch
either way (a drawn expression with no name, or a name with no drawing) is a fail — that gap
is exactly where the rig guesses and goes off-model.

---

## Pitfalls

- **Mouth-only expressions** (the dead smiley) — forgetting the brow is the #1 beginner tell.
- **Fear/surprise collision** — identical up-brows → the character can only look startled.
- **Symmetric everything** → emoting, not acting; no smirk, no skepticism possible.
- **Naturalistic push on a stylised show** → expressions vanish at thumbnail size.
- **Overloading viseme shapes with emotion** (or vice-versa) → the character can't emote
  while talking; keep the two zones independent.
- **Tracing a generic expression chart** → off-model faces that don't belong to this
  character.
- **No peak/settle** → emotions that never land or never stop shouting.
- **Un-named shapes** → the rigger invents the muscle and the face drifts shot to shot.

Next: lay the locked expression row into `model-sheet-turnaround`; the rigger builds the
named set in `creative-arts.animation.blender.rigging`.
