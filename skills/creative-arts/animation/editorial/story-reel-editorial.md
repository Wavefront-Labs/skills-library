---
id: creative-arts.animation.editorial.story-reel-editorial
name: story-reel-editorial
category: creative-arts
field: animation
product: editorial
tags: [story-reel, animatic, editorial, leica-reel, boards-to-reel, scratch-audio, scratch-vo, timing, living-edit, revise-before-animation, ffmpeg, editorial-cut]
level: advanced
status: draft
description: "Cut the animatic/story reel: assemble boards and VO to a timed reel that drives production, revising timing before animation is expensive, with scratch audio."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Story reel editorial — cutting the animatic that drives the whole production

The story reel (Leica reel / animatic) is the film in its cheapest watchable form:
storyboards cut to timing with scratch audio. On an animation production it is not a
pre-viz nicety — it **is the edit**, the living document every department animates *to*.
Every timing problem you solve in the reel costs minutes; the same problem found after
animation costs days of re-animation and re-render. This skill is the discipline of
building and maintaining that reel. It takes boards from `shotlist-boarding` and overlaps
with `animatic-assembly` (the mechanical build) — this skill is the *editorial* craft on
top: deciding what's on screen and for how long. Pacing within the cut is its own skill
(`editorial-pacing`); this one is about the reel as a production instrument.

## 1. What the reel is for (why it drives everything)

- It proves the **story works before anything expensive is built**. If a scene is boring
  or confusing on boards, it will be boring in full render — only costlier to fix.
- It is the **timing contract**: each shot's duration, in frames, is what layout, animation,
  and the final cut inherit. Animators animate to the reel's handles.
- It is the **communication hub**: director, board artists, editorial, and the downstream
  pipeline all read the same reel. A decision not reflected in the reel didn't happen.

## 2. Build the first assembly

1. **Lock the frame rate and format first.** Everything is in frames at the show rate (e.g.
   24 fps for the project). A reel cut at the wrong rate hands wrong frame counts to the
   whole pipeline. Set the sequence timebase before importing a single board.
2. **Import boards in script order**, one image per board panel, onto the timeline. Hold
   each on screen for a first-guess duration (read the action/dialogue aloud and time it).
3. **Lay in scratch audio** (§3) and nudge each board's duration to the audio. The reel's
   timing is driven by performance, not by even spacing.
4. **Add scene/shot slugs and a running timecode** burn-in so everyone references shots the
   same way (pairs with `shot-episode-structure` numbering).
5. **Watch it end-to-end** before fixing anything. The reel's job is the whole, not the
   panel; first-pass notes are about where it drags, confuses, or dies.

In a local/open-source pipeline the assembly can live in a conventional NLE or be scripted:
boards + an EDL/CSV of durations assembled with ffmpeg (concat each still for N frames,
mux the scratch track). Either way the output is a single watchable file with burned-in
timecode and shot slugs.

## 3. Scratch audio — the reel's heartbeat

Timing is driven by sound, so get sound in early even if it's rough.

- **Scratch VO/dialogue.** Record a temp read of every line (yourself, a TTS voice such as
  Kokoro/Piper, anyone available). It does not need to be the final performance — it needs
  to be the **right length and intention** so boards can be timed to real speech rhythm.
  Lines timed to silence always come out wrong.
- **Temp music & SFX.** A temp music bed sets the emotional pace and tells you where the
  cut wants to breathe or drive. A few key SFX (a door, a gunshot) that the cut hinges on
  should be in from the start.
- **Keep scratch clearly labelled** and in its own tracks so final audio cleanly replaces
  it later; never let scratch quality decisions leak into picture timing.

## 4. The reel as a living edit

The reel is revised constantly — that is the point. Treat it as the master the whole show
tracks against.

1. **Version every cut** with a date/version slug burned in, so notes reference a known
   version and nobody animates to a stale reel.
2. **Fold in each stage as it arrives.** As layout, then blocking, then final animation of
   each shot land, replace the board with the newer version *in the same slot*. The reel
   thus matures from boards → layout → blocking → final without ever stopping being the edit.
   This is the single most important editorial habit in animation: one continuous document,
   not a boards reel and a separate final cut.
3. **Hold the timing contract.** When a shot's duration changes, change it in the reel and
   push the new frame count/handles to the owning department — never let the floor and the
   reel drift apart.
4. **Re-watch whole after every significant change.** A local fix often breaks the
   surrounding rhythm; the reel is judged as a whole every time.

## 5. Revise timing before animation (where the money is)

This is the economic heart of the discipline: **solve it on boards.**

- **Cut scenes that don't earn their length on boards.** If a sequence drags as cheap
  images, it will drag worse rendered. Losing a scene in the reel costs nothing; losing it
  after animation costs everything spent on it.
- **Fix confusion with new boards, not dialogue bandaids.** If the audience won't understand
  an action, add/replace boards and re-time — cheap now.
- **Push the hard conversations early.** The reel is where the director, editor, and
  department leads agree the film works. Every unresolved story/timing question left in the
  reel becomes a re-animation ticket later.
- **Lock sequences progressively.** As a sequence's timing is signed off, mark it locked so
  layout/animation can commit frame counts; keep un-signed-off sequences fluid.

## 6. Assembling the reel with open-source tools

A reel does not need a commercial NLE. A reproducible, scriptable build keeps the timing
contract machine-readable, which matters when an automated pipeline consumes frame counts.

1. **Drive it from a shot table** (CSV/JSON): one row per shot — slug, board image path,
   duration in frames, dialogue cue. This table *is* the edit; the video is a render of it.
2. **Burn metadata into the picture.** Overlay the shot slug, frame count, and version slug
   with ffmpeg's `drawtext` so every frame is self-identifying when someone pauses on a note.
3. **Hold each board for its frames**, then concat: generate a per-shot clip
   (`ffmpeg -loop 1 -i board.png -t <frames/fps> ...` or a concat demuxer with per-entry
   durations) and mux the scratch track over the whole. A 24 fps show means a 36-frame hold
   is 1.5 s — always compute durations from frames, never type seconds, or rounding drifts
   the sync over a long reel.
4. **Re-run the build from the table** on every revision so versions are deterministic and
   diffable; nobody hand-trims the exported file.

## 7. Common reel failures to watch for

- **Even-spacing drift.** Boards all held the same length regardless of content — a dead
  giveaway the reel wasn't timed to performance. Time to the scratch VO, not the clock.
- **The reel that stopped being the edit.** Once final animation starts, teams sometimes cut
  a separate final in another tool and let the reel rot. Fatal — the reel must mature in
  place or it stops governing timing.
- **Scratch quality leaking into decisions.** A flat TTS read can make a lively scene feel
  dead; judge the *length and intent*, and re-time once a better scratch read lands.
- **No handles.** Shots cut frame-exact in the reel leave animators no overlap for match
  cuts; carry a few frames of handle on each shot so `editorial-pacing` can cut on action.

## Verify

- [ ] The reel is built at the **show frame rate** and every shot carries a **frame-count
  duration**, slug, and running timecode burn-in.
- [ ] **Scratch audio** (VO/dialogue, temp music, key SFX) is laid in and boards are timed
  **to the audio**, not evenly spaced; scratch is isolated for clean later replacement.
- [ ] The reel has been **watched end-to-end** and judged as a whole, with notes on where it
  drags/confuses — not just per-panel notes.
- [ ] Each cut is **versioned with a burned-in version slug**; departments animate only to
  the current version.
- [ ] The reel is a **living edit**: boards are being replaced in place by layout → blocking
  → final in the same slots, and it never stops being the master cut.
- [ ] Shot **duration changes are reflected in the reel and pushed to the owning department**
  (the timing contract holds; floor and reel don't drift).
- [ ] Weak/confusing sequences were **fixed or cut on boards before animation**; signed-off
  sequences are marked **locked** for frame-count commitment.
