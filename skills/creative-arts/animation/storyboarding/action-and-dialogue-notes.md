---
id: creative-arts.animation.storyboarding.action-and-dialogue-notes
name: action-and-dialogue-notes
category: creative-arts
field: animation
product: storyboarding
tags: [storyboarding, storyboard-format, board-notes, action-notes, dialogue-notes, slug, camera-notes, sfx-notes, panel-fields]
level: intro
status: draft
description: "Write clear panel notes: action descriptions, dialogue with character names and OS/VO tags, camera and SFX slugs, and what not to write."
sources:
  - https://en.wikipedia.org/wiki/Storyboard
  - https://docs.toonboom.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Action and dialogue notes

Goal: panel notes that add what the drawing cannot show, briefly and unambiguously.

## Fields
- **Action**: what happens that the drawing does not show - motion over time, intent, hidden
  information ("He pockets the key without her noticing"). Present tense, short.
- **Dialogue**: character name in caps, then the line; tag OS (off-screen), VO (voice-over),
  CONT'D. Split long lines across panels at natural pauses.
- **Slug / notes**: camera (PAN R, TRUCK IN), transitions (DISS), SFX ("SFX: thunder"), timing
  hints ("hold 2 s"), BG IDs, new design flags.

## Writing rules
- Do not describe what is clearly drawn ("He stands there").
- Name props and characters as on the design lists.
- Put timing in seconds or frames consistently.
- Mark acting intention where it is subtle ("forced smile").

## Example
```
ACTION:  Mira slides the letter under the door, glances down the hall.
DIALOGUE: MIRA (whisper): Don't be home... don't be home.
NOTES:   SLOW PUSH IN. SFX: distant footsteps OS. BG reuse: BG_HALL_02
```

## Failure modes
- Dialogue in boards not matching the current script.
- Missing OS tags (animators animate a mouth that should be off-screen).
- Notes so long the drawing is ignored.

## Verify
- [ ] Every line of the script appears in the dialogue fields.
- [ ] OS/VO marked.
- [ ] Notes add information not already drawn.

Related: `creative-arts.animation.storyboarding.board-arrows-and-move-notation`,
`creative-arts.animation.storyboarding.tv-board-format`.
