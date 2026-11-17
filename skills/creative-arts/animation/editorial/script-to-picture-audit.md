---
id: creative-arts.animation.editorial.script-to-picture-audit
name: script-to-picture-audit
category: creative-arts
field: animation
product: editorial
tags: [editorial, review, continuity, staging, show-dont-tell, contact-sheet, shotlist, dialogue, props, qc, ffmpeg, pil]
level: advanced
status: draft
description: "Audit a cut shot by shot: does the screen show what each action line and spoken line names? Labelled contact sheets, root-cause buckets, fix order."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Script-to-picture audit

**Goal:** find every place where the dialogue or the action line names something the
viewer never sees. A cold viewer cannot follow a story told only by the voice track.
They describe it as "broken", "random lines" or "nothing lines up" without being able
to say why. This audit names why, shot by shot.

Run it on every assembled cut, before polishing anything else. Polish on a cut that
doesn't show its story is wasted.

## Build the evidence (one pass, ten minutes)

1. Take real shot starts from the assembly, not summed durations. Grab one frame per
   shot at about 55 % of its length from the final cut.
2. Tile 12 frames per sheet, each with three caption lines: shot id, size and the
   action text; the spoken line in red; the rest of the action text in grey.
3. Read every tile and ask two questions. Is the thing the action names on screen? Is
   the thing the line refers to on screen now, or was it shown just before?

```python
subprocess.run([FF, "-ss", f"{start + dur*0.55:.2f}", "-i", cut, "-frames:v", "1",
                "-vf", "scale=480:270", tile])
draw.text((x, y+272), f"{sid} {size} | {action[:52]}"); draw.text((x, y+292), line[:58], fill=RED)
```

## Root-cause buckets (sort every miss into one)

- **Static characters.** Walks, runs, crouches, reaches, turns, hands doing things.
  If a character is a fixed drawing, every one of these misses at once.
- **One painting per location.** Shots that name a specific view (aerial, a detail,
  the far end of the street, the reveal) but show a crop of the generic set.
- **Missing props.** Objects the action or line depends on.
- **Caption dialogue.** Lines that narrate what the viewer should see ("A green line.
  Right through the wall.") in clipped fragments. They sound robotic from a TTS voice,
  and like nonsense when the thing isn't shown. Count lines averaging under four words
  per sentence; on one episode it was 37 of 63.
- **Non sequiturs.** A reply that doesn't answer the line before it. Read each line
  next to its predecessor.
- **Art contradicting a line.** The line says "same cardigan" and she wears another
  top; it says "there is no oven" over a kitchen with an oven.
- **Sound for invisible events.** Footsteps with nobody walking read as random noise.
- **The payoff shot.** Check the episode's biggest reveal first. It was the most
  expensive shot to stage, so it is the most likely to be a placeholder.

## Run it on the script first (preflight, verified 26 Oct 2026)

Every cause in the buckets above was already visible in the shot list before a frame was drawn. Auditing a shot list takes
seconds and is the cheapest check in the pipeline. Measure, per episode:

- **Filler share:** shots whose action starts with an atmosphere marker, as a share of runtime, and how many *distinct*
  descriptions they use. On one season, episodes 3 to 10 were 34 to 52 % filler built from 6 to 9 descriptions, and one
  description repeated 7 times in one episode.
- **Written length against target.** Compare the lean written script with the padded one. Here the written stories
  were 3.1 to 4.1 minutes and a coverage pass padded each to 6.5 against a 6 to 10 minute target. Padding hides a story that
  is too short, and drawing it spends the most expensive step on cutaways that carry nothing.
- **Shots with no visible action:** an action of four words or fewer ("Dill.", "Dill resolves.") or one built on a thought
  verb (thinks, resolves, decides, remembers, realises, knows). Each needs something a camera can see: a hand, an object, a
  change of posture or a look.
- **Fragment dialogue:** lines averaging under four words per sentence. Count them, then separate quick replies ("The
  what?"), which are fine, from caption lines that list what the picture should show.
- **Voice clashes:** two characters on one voice, within an episode and across the season; and a candidate voice for a
  lead that another character already uses.
- **Undeclared sets:** locations or named buildings in the actions that the set list does not contain.

Report it as a table per episode, propose rewrites for the weak lines and the thought shots, and let the writer decide
length and edits. Don't change the script silently and don't re-run the padding tool before that decision.

## Report

Lead with counts: paintings versus shots, shots missing their action, fragment lines,
misheard lines. List root causes in order of how many shots each explains. Give a
shot table of only the misses, grouped by scene: script says, screen shows, fix. End
with the fix order. The order is fixed by dependencies: character movement first,
then a painting per named setup, then props, then dialogue rewrite and re-voice, then
the re-cut. Rewriting dialogue before the picture can show things just moves the gap.

Script rewrites are the writer's decision. Propose them with the rewritten script
attached; don't change a writer's lines silently.

## Verify

The next cut's audit lists fewer misses in every bucket, and a cold viewer can retell
each scene from the picture with the sound off.

See `continuity-supervision`, `story-props-staging` and
`pipeline.episode-qc-cold-viewer`; intelligibility of the lines themselves is
`sound-design.tts-dialogue-intelligibility-gate`.
