---
id: creative-arts.animation.storywriting.novel-to-teleplay
name: novel-to-teleplay
category: creative-arts
field: animation
product: storywriting
tags: [screenwriting, adaptation, teleplay, novel, structure, runtime, show-dont-tell, interiority, compression]
level: advanced
status: draft
description: "Adapt prose to a shootable teleplay: scene mapping, compression, externalizing interiority, act structure, runtime budgeting for a 6-8 min episode."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SKILL: Novel → Teleplay adaptation

**Goal:** turn finished prose canon (a completed novel in N parts) into shootable
animated-episode scripts that keep the story, theme, and voice intact — and that hand
the shot pipeline exactly the data it needs. Adaptation is not transcription and not
reinvention; it is **translation across a boundary** (what a reader imagines vs what a
camera photographs and a mic records), done under a hard runtime budget.

## Principle: the novel is canon, the teleplay is a lens
Every on-screen line and action must trace to a passage in the source. You are not
free to add plot; you are free — obligated — to *choose, compress, and externalize*.
Prose can live inside a head for a page ("Dill felt the old pull of being watched");
film cannot. The adapter's core job is converting interiority into **behaviour, image,
and sound** the camera can capture. If you can't shoot it, it isn't in the teleplay.

## 1. Map the whole before cutting a frame
Before writing any scene, build a one-page map of the source:
1. **Spine sentence** — the series question in one line ("can a person be real when
   their worth is metered?"). Everything that doesn't serve it is a cut candidate.
2. **Part → episode table.** Our 10-part novel maps roughly 1 part ≈ 1 episode, but
   don't take that as law — recluster to land each episode at a clean dramatic unit.
   A 6-8 min YouTube episode is *short*: it holds one escalation, not a whole part's
   worth of subplot.
3. **Beat extraction per part.** List the 3-6 load-bearing turns already in the prose
   (they're built in — a finished novel has done this work). These become your act
   structure; you are discovering it, not inventing it.
4. **Theme touch-points.** Mark where each part dramatizes the spine. Keep at least
   one per episode; cut dialogue that *states* it.

## 2. Scene selection and compression (the cutting room)
A 6-8 min episode at animation pace is ~900-1100 spoken words plus action. A novel
part is 5,000-10,000. You will cut 80%+. Rules for what survives:
- **Keep turns, cut connective tissue.** A scene earns its place only if it changes
  the character's situation or the audience's understanding. Travel, repetition, and
  "and then they talked more" are the first to go.
- **Collapse scenes.** Three prose conversations that each advance one point become
  one scene that does all three, staged over a single activity. Okafor's groceries can
  deliver "the town loops" while two other beats ride underneath.
- **Merge or cut minor characters.** Give a cut character's key function to one who's
  already load-bearing. Fewer faces to model, cast, and keep consistent.
- **Relocate exposition onto action or image.** A paragraph explaining the town's rule
  becomes one shot: the needle on the meter reading 1.
- **Externalize, don't summarize.** Never replace prose interiority with a voice-over
  that narrates the feeling. Find the behaviour that *is* the feeling (hands pressed
  flat, flat affect, the count under the breath).

## 3. Episode structure (what a 6-8 min unit needs)
- **Cold open (45-75s):** an image that opens a gap, not a recap. The orange circling
  back into the drain. End on a small turn, then the title card.
- **2-3 acts.** Each act escalates the one central question and ends on a **button**
  (a reveal, reversal, or worst-timing beat) that makes stopping feel wrong.
- **Button/cliff:** the last image resolves the *episode* question and sharpens the
  *series* question. Open-ended series never fully resolve; if episode 1 answers the
  spine, episode 2 has no reason to exist.

## 4. Teleplay format (animation)
```
INT./EXT. LOCATION — TIME
Action lines: present tense, only what the camera sees / mic hears. Short.
CHARACTER
    (parenthetical: delivery direction)
    Dialogue.
[SFX: ...]  [MUSIC: ...]  [CAMERA: push-in / whip-pan]  [FX: static glitch]
```
Action lines are filmable facts: "Dill's counter ticks up" — never "Dill feels the
warm pull of being watched." The second is a note to yourself about the first. Convert
every felt thing to its visible metric plus a performance beat. Tag `[CAMERA]`,
`[SFX]`, and `[MUSIC]` inline so the boarding pass and shotlist inherit intent.

## 5. Dialogue out of prose
- **Lift then tighten for the ear.** Spoken ≠ written. Read every line aloud; cut to
  the fewest words that land. Contractions, fragments, interruptions ("—"), trails
  ("…") are performance direction, not typos.
- **Strip narration.** Prose dialogue is often cushioned by "she said, carefully,
  knowing he'd hear the lie." Delete the cushion; put the carefulness in the
  parenthetical or let the actor (the TTS voice + direction) carry it.
- **Preserve voice-print.** Each character's rhythm/lexicon must match the novel's
  characterization so you could ID the speaker with names stripped. Keep a line-voice
  note in the consistency bible (Chip's bright TV-host menace with a one-frame crack;
  Pidge's fast sideways science; Gran Wynn's dry mercy).
- **No "As you know, Bob."** Give exposition to the character who *doesn't* know, or to
  an image.

## 6. Runtime budgeting (lock it off VO, not off page count)
Animation plays slower than live TV, and the page-per-minute rule is only a start
(~1 page ≈ 40-60s; dialogue-heavy faster, action slower). The real durations come from
the actual voice-over. Our flow: **generate VO early** (local TTS — Kokoro/Piper),
read its measured per-line seconds, and pace the episode to those numbers. If the cut
runs long, split the part at a natural act-out across two episodes; if short, restore
a prose beat you trimmed. Do not pad — a tight 6 min beats a baggy 8.

## 7. Handoff to the pipeline (novel → teleplay → shotlist)
The teleplay is an intermediate artifact, not the final data. It feeds the boarding
pass, which breaks each scene into sequences and shots with camera notes and
dialogue-timing, and emits the per-episode **shotlist JSON** (e.g.
`series/scripts/EP01_shotlist.json`) that drives the Blender render and the VO batch.
Keep dialogue IDs stable from teleplay → shotlist so VO wavs, Rhubarb visemes, and
shots stay joined. See `shotlist-boarding.md` and
`../pipeline/shot-episode-structure.md`.

## Verify
- [ ] Every on-screen line and action traces to a source passage (no invented plot).
- [ ] Each episode has a cold-open hook (image, not info), 2-3 acts, each act-out a
      button, and a cliff that escalates the series question while resolving the
      episode's.
- [ ] No action line describes a feeling the camera can't photograph; every
      interiority is rendered as behaviour/image/sound.
- [ ] No character states the theme aloud; the theme is dramatized at least once.
- [ ] Each character is identifiable with names stripped, read aloud.
- [ ] Runtime locked against measured VO, not page count; episode lands 6-8 min.
- [ ] Dialogue IDs stable from teleplay through shotlist JSON.

See also: `screenwriting-craft.md`, `shotlist-boarding.md`, `consistency-bible.md`.
