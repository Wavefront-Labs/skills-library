---
id: creative-arts.animation.voice-tts.lip-sync-review-and-offset-correction
name: lip-sync-review-and-offset-correction
category: creative-arts
field: animation
product: voice-tts
tags: [lip-sync-offset, lip-sync-review, av-sync, audio-offset, dailies, sync-tolerance]
level: practitioner
status: draft
description: "Review lip-sync in shots and correct offset: viewing procedure, ITU sync tolerances, constant versus drifting errors, frame-offset fixes and where to fix them."
sources:
  - https://www.itu.int/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Lip-sync review and offset correction

## Tolerances
- Viewers detect audio-video offset only past a threshold. ITU-R BT.1359 gives detectability thresholds of about **45 ms with audio early** and **125 ms with audio late**, with acceptability thresholds wider than those. EBU R37 recommends tighter delivery limits (about 40 ms early and 60 ms late). One frame at 24 fps is 41.7 ms, so a one-frame error is borderline and two frames is usually visible.
- Audio late is tolerated more than audio early, because that is how sound travels in real life.

## Review procedure
1. Review at full speed with the final audio, in the DAW or editor with correct frame rate and a verified 2-pop (`video-track-sync-in-the-daw.md`).
2. Watch each line twice: once for the mouth closures (M, B, P), once for the accented vowels.
3. Log issues with timecode and a direction: "mouth late by 2 frames", "closure missing at 04:12".
4. Review in context in the cut and at full screen size; small preview windows hide drift.

## Diagnose before fixing
| Pattern | Likely cause | Fix |
|---|---|---|
| Constant offset on all lines in a shot | Audio or video start offset, handle count in the export | Slide the audio or animation by the offset; fix at the source |
| Offset grows over the shot | Frame-rate or sample-rate mismatch, speed change | Correct the rate in the export |
| One line only | Animator timed to an old track | Re-read the new track (`reading-dialogue-onto-an-exposure-sheet.md`) |
| Everything off after a re-cut | Changed handles | Conform the shot to the new edit |

## Where to fix
- If animation is correct to the track, fix the audio placement (editorial) or the shot's frame offset, not the animation.
- If a shot was animated against a scratch track and the final line differs, re-time the animation.
- Record the fix as a note on the shot so it does not return in the next version.

## Verify
- [ ] No visible closure miss at full-speed review.
- [ ] Remaining offset within about one frame.
- [ ] Notes and fixes tracked per shot.
