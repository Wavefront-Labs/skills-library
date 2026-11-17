---
id: creative-arts.animation.pipeline.episode-qc-cold-viewer
name: episode-qc-cold-viewer
category: creative-arts
field: animation
product: pipeline
tags: [animation, pipeline, qc, qa, quality-assurance, episode-review, cold-viewer, comprehension, dialogue-flow, speaker-on-screen, lip-sync, mouth-read, screen-tearing, clipping, intersection, hands, story-beat, props, benchmark, side-by-side, reference-show, self-review, delivery-gate, agent-review]
level: advanced
status: verified
description: "Episode-level QA as a cold viewer: watch the cut against a benchmark show, score comprehension, speaker-on-screen, lips, clipping, tearing; block delivery on red."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Episode QC as a cold viewer

The last gate before anyone outside the pipeline sees the cut. Every upstream check
in this library is **per-shot and per-department**: preflight asserts files exist,
dailies review stills, `probe` proves the container decodes. All of them can be green
while the episode is unwatchable. This skill exists because a cut passed every one of
those gates and the owner's first review was: *"the transcript is all over the place,
I can't tell what they're talking about, hands look incomplete, people stuck in walls,
screen tearing, I can hear the robot talking but I'm looking at a wall."*

None of those are shot defects. They are **viewer-experience defects**, and the only
instrument that detects them is watching the episode the way a stranger would.

## The rule

**Nobody declares an episode done from a probe and four stills.** Done means: the
reviewer (human or agent) has sat through the whole cut with sound, next to a benchmark
episode of the target show, and filled in the scorecard below with numbers and
timestamps. If a row is blank, the review did not happen.

Agents especially: a clean `ffprobe`, a full-decode with zero errors and a contact
sheet are **container proof, not content proof**. They answer "is it a valid file",
never "is it a watchable episode".

## The three realness axes

The owner's review collapses to three questions, and the scorecard below is organised
so each has a measured answer:

- **Conversation realness** — can a stranger follow who is talking, to whom, about
  what, and why it matters? (sections 1–2)
- **Character realness** — do the cast read as people: hands, lips, eyes, face motion,
  voice that is not a robot? (section 3)
- **Scenery realness** — does the world read as a place with density and depth, and
  do the characters stand IN it rather than through it? (sections 4–5)

An episode with any axis red is not a rough version of a good episode; it is a
different, broken experience, and polish on the other two axes is invisible.

## Procedure

### 0. Get the benchmark next to the cut

Pick ONE episode of the target show (the tier the brief names — e.g. Murder Drones /
Rick & Morty for a stylized series). Obtain a legitimately accessible copy for private
reference comparison. Take the same instruments from both:

- 12 evenly spaced frames + 12 frames at dialogue lines (ffmpeg `-ss T -frames:v 1`)
- the dialogue track with timestamps (benchmark: subtitles; cut: the shotlist lines
  with the clip start times accumulated from `dur_s`)
- loudness (`ebur128`) and dialogue-to-silence ratio

Side by side is the whole method. A frame judged alone always passes; the same frame
next to the benchmark's shows what is missing (density, hands, mouth, staging).

### 1. Comprehension pass (sound on, no shotlist)

Watch the full cut cold. Write, in one paragraph, what you think happened. Then diff
that against the script's own synopsis. Every beat the synopsis has that your paragraph
lacks is a **missing-beat defect**, timestamped to where it should have played.

Measure the three numbers that predict "random words":

| Metric | Red | How |
|---|---|---|
| Longest dialogue gap | > 45 s in a dialogue scene | accumulate `dur_s`; diff consecutive line starts |
| Lines with no visible subject | any | for each line: is the thing it refers to ON SCREEN in that shot or the previous one? |
| Speaker off-frame while talking | any line | per line: speaker's head bone projects inside the frame for ≥ 80% of the line |

**Lines with no visible subject** is the one that produced "one of the characters
just randomly says choreography". The line was written as a reaction to a town-wide
bell ritual — porch lights popping in a wave, heads turning. The render showed an
empty street wall. On the page it is a great one-word line; on screen, with the
referent missing, it is a non sequitur. Check the referent, not the line.

**Speaker off-frame** produced "I can hear the robot talking but I'm looking at a
wall". Lip-sync was correctly bound to the speaker; the camera simply wasn't on them.
Preflight warned *speaker ≠ primary cast* and the note was dismissed as informational.
It is not informational — it is this defect.

### 2. Story-beat props

For every action line in the shotlist that names an object (a grocery bag that splits,
an orange rolling into a drain, a receipt, a letter), confirm the object exists as a
prop in the shot. **An action beat without its prop renders as a character miming at
nothing**, and the audience loses the plot thread the beat carried.

Grep the action text for nouns, cross-reference against the set's dress list, and
list every miss. This is a 5-minute check that would have caught the bag/orange beat
(the entire premise of the rerun gag) rendering as a man crouching on an empty kerb.

### 3. Character read (benchmark side by side)

Frame the same shot sizes from both shows. Score each cast member:

- **Bible match first.** Put the character bible's design line beside the render:
  species, silhouette, head shape, palette, the one distinguishing feature. A cast
  rebuild that fixed rigging rebuilt the robot host — "box CRT head, emissive
  screen-face, square-on-round" — as a short human in a brown top, because the build
  script started from the human base mesh for every cast slot and nobody re-read the
  bible. The owner's note was "he was a robot, now he's a guy". Rigging gates passed;
  the character was wrong. Red if any bible line is contradicted.
- **Hands** — five distinct fingers in a MEDIUM shot; nothing inside-out; no fused
  claw. Low-poly base hands with a uniform outline hull fail this every time; it is the
  first thing a viewer's eye lands on after the face.
- **Mouth** — reads as lips, not a card/blob. A 2D mouth card is a legitimate
  stylized technique **only if** it is placed exactly on the lip line, scaled to the
  philtrum-to-chin span, and carries lip shapes (not just an open/closed dark oval).
  Offset by a few cm it reads as a moustache; undersized it reads as a hole.
- **Face motion in close-up** — frame-diff the face region over a CLOSE shot; red if
  the mouth region moves but brows/eyes do not (talking mask).
- **Voice** — if the reviewer's gut says "robot", measure pitch span per line (pyin);
  the fix is prosody (see `voice-casting-consistency` §6b), not volume.

### 4. Staging and mechanical defects

Three classes, all visible only in motion:

- **Clipping / stuck in walls** — a character's bounds intersect set geometry. Catch
  procedurally with `technical-animation-finaling` (bbox vs set BVH per shot) but ALSO
  by eye: characters half-inside a door frame, feet below the floor plane, a
  background extra placed at the wrong scale behind a barrier.
- **Tearing** — mesh faces stretching between bones (bad weights after a restyle),
  outline hull inverting over thin parts, or a shape key pulling a region through
  another. Shows as flickering spikes; scrub at 0.25× speed on every CLOSE and MEDIUM.
- **Scale / placement** — an extra rendered at the wrong distance reads as a toy;
  cross-check each non-primary cast member's world position against the mark table.

### 5. Scenery read

Side by side with the benchmark establishing shot: count **distinct readable objects**
in the frame (benchmark stylized shows carry 15–40 in a WIDE). A set that passed the
"not a box" gate can still be an empty lot. Red if under half the benchmark count, or
if any WIDE has no foreground element.

## Scorecard (fill every row; timestamps mandatory)

```
comprehension paragraph        : <text>
missing beats                  : n  [t=..., t=...]
longest dialogue gap           : s  (red > 45)
lines with no visible subject  : n  [line ids]
speaker off-frame while talking: n  [line ids]
action beats missing their prop: n  [shot ids]
bible contradictions           : n  [character: line]
model-sheet drift              : n  [character_view: diff]
model sheet hands/feet/hems    : n  [character: defect]
flat VO (directed cast)        : n  [character: semitones]
VO loudness spread             : n  [character: LU]
hands fail (MEDIUM+)           : n  [shot ids]
mouth misplaced / not lips     : n  [shot ids]
talking-mask closeups          : n  [shot ids]
clipping / stuck in geometry   : n  [t=...]
tearing                        : n  [t=...]
wrong-scale extras             : n  [t=...]
WIDE object count vs benchmark : ours / theirs
verdict                        : SHIP | FIX-LIST | REBUILD-SCENE
```

Any red row = not done. The verdict goes on the production board **with the counts**,
never as "QC frames pass".

## The loop, automated (review → fix → re-QC → write back)

Review without improvement grades the same cut twice. The loop that makes the
scorecard move:

1. **A script runs the measurable rows** (dialogue gaps, speaker-in-cast, action
   nouns vs prop names, bible keywords vs build config, benchmark present) and
   extracts the frame sheet (a frame at every line + 12 spaced, benchmark frames
   beside). Finaling rows (clipping, tearing) come from the per-shot reports the
   renderer writes (`technical-animation-finaling` §5). Assembly calls it and exits
   non-zero on any red row, so "done" cannot be typed over a red card.
2. **Scorecards are versioned** (`qc/<ep>_001.json`, `_002`…) and each run diffs the
   previous: FIXED / REGRESSED per row. Progress is a number.
3. **Eye-only rows carry forward** from the previous card, marked `carried`, so a
   re-run never silently resets a judgement; a cut that changed what they measure is
   re-filled from the new sheet.
4. **Each red row maps to one fix** in visibility order, and each fix re-renders only
   the shots the row named before the full re-render.
5. **Each row carries `lesson_to`:** the skill id that should have caught it. Closing
   a row means fixing the shots AND bumping that skill. That is the write-back that
   stops the same lesson being relearnt next episode.

### Rows that moved from "by ear/eye" to measured (second iteration)

- **Flat VO** — 10–90 % pitch span in semitones per character (pyin over every line,
  mean per character). Red for a *directed* character under 4; townsfolk played flat
  on purpose are exempt by name. The lead measured 1.6 while the rest of the cast sat
  at 7–9 and a dialogue slice of the benchmark at ~28: he was the "robot" the owner
  heard, and no amount of mouth work fixes that row.
- **Loudness spread** — integrated loudness (`ebur128` I) per line; red when one
  character's lines differ by more than 6 LU (reads as different takes). Measure only
  the files the shotlist names: a stray test line and a backup copy in the same folder
  produced an 11 LU false red before the filter.
- **Model-sheet drift** — the build writes a front / three-quarter / side turnaround;
  QC diffs each against the *locked* sheet in `design/model_sheets/` (48 px grey thumb,
  mean abs diff, red over 0.06) and reds any character with no locked sheet. This is
  the row that catches "the robot is a man now" before a shot renders; re-locking is
  an explicit copy, never automatic.
- **Timed transcript** — the shotlist's lines with accumulated start times, speaker
  and shot size, written beside the card so the comprehension read is done against
  what the cut actually says in order.
- **Model sheet: hands / feet / hems** — an eye row on the turnaround itself, before
  any shot: splayed paddle fingers, bare foot meshes standing in for shoes, and
  sawtooth garment hems (a z-band cut through a body mesh) all show on the sheet and
  would otherwise be found 87 shots later.

Detector hygiene: a finaling row is only as good as its detector. A parity ray test
against an *open* mesh (an interior wall plane) reports "inside" for half the room;
restrict inside tests to closed meshes (every edge shared by two faces) or the row
cries wolf on every kitchen shot.

First iteration on a real cut: 12 red rows → three measurable rows closed (speaker
off-frame 2→0, bible contradictions 1→0, missing props 20→0) before the re-render,
with the fixes landing as a robot-host rebuild, a props module, a speaker-hold camera
rule, lips/hands changes and a finaling detector — each written back to its skill.

## Who does this

A professional studio runs this as a **story-reel screening with sound**, and again
at every stage of the cut (animatic, layout, animation, final). The point of the
screening is that the people watching did not make the shots. An agent reviewing its
own render must simulate that: no shotlist open, no knowledge of what each shot was
*meant* to show, only what it shows.

## Failure modes this skill exists to prevent

1. **Declaring done from container proof.** Probe clean + decode clean + four stills
   ≠ watched. (This happened.)
2. **Judging frames alone.** Every frame passes on its own; the benchmark beside it
   is what reveals the gap.
3. **Dismissing the speaker/primary-cast warning as informational.** It is a camera
   defect: the audience hears a voice and sees a wall.
4. **Reviewing lines on the page.** Dialogue that reads on paper fails on screen
   whenever its referent didn't render. Check referents.
5. **Shot gates standing in for the episode gate.** 87 green shots do not make a
   watchable 6 minutes.
6. **Rebuilding the cast without the bible open.** A technical rebuild (rigging,
   base mesh swap) silently redesigns characters when every slot is built from the
   same template. Numeric rig checks cannot see that the robot became a man.

## Verify

Run the scorecard on a cut you believe is finished. If every row is already green on
the first pass, you did not watch it cold — hand it to someone who has never seen the
shotlist and compare their comprehension paragraph to yours.
