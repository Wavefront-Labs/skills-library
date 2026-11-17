---
id: creative-arts.music.composition.first-and-second-species-counterpoint
name: first-and-second-species-counterpoint
category: creative-arts
field: music
product: composition
tags: [counterpoint, species-counterpoint, first-species, second-species, cantus-firmus, fux, voice-leading, consonance, passing-tone, parallel-fifths, method, recipe]
level: practitioner
status: draft
description: "Write first-species (note against note) and second-species (two against one) counterpoint over a cantus firmus by Fux's rules, then check it for forbidden motion."
sources: ["Johann Joseph Fux, Gradus ad Parnassum (1725), trans. Alfred Mann, The Study of Counterpoint", "Peter Schubert, Modal Counterpoint, Renaissance Style", "https://openmusictheory.github.io/firstSpecies.html", "https://openmusictheory.github.io/secondSpecies.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# First and second species counterpoint

**Goal:** add a single melodic line above or below a given cantus firmus (CF) that is
independent, singable and uses only legal consonance and dissonance.

## Setup
- CF: 8-16 whole notes, stepwise, starts and ends on the final, one climax.
- Counterpoint above: start on unison, 5th or octave. Below: start on unison or octave
  only (a 5th below puts the CF on a non-tonic bass).
- Perfect consonances: P1, P5, P8. Imperfect: m3, M3, m6, M6. The P4 is a dissonance
  in two-voice writing.

## First species (1:1)
1. Every vertical interval is consonant.
2. Ending: the cadence is a step into the final in both voices, contrary motion -
   in the counterpoint above, ti-do (raise the leading tone in Dorian, Mixolydian,
   Aeolian); below, re-do.
3. Motion: prefer contrary and oblique; use imperfect consonances for most of the line
   (aim for 3+ consecutive imperfects, max 3 parallel 3rds/6ths in a row).
4. Forbidden: parallel 5ths/8ves/unisons; similar (direct/hidden) motion into a perfect
   interval; unison except first and last note; voice crossing; overlap.
5. Melody: mostly steps; leaps up to a 6th (minor 6th ascending only) or octave; recover
   a leap by step in the opposite direction; no augmented/diminished leaps; no outlined
   tritone; one climax note that does not coincide with the CF climax.

## Second species (2:1)
- Downbeats: consonant (same rules as first species, checked downbeat to downbeat -
  5ths or 8ves on consecutive downbeats are still parallels even with a note between).
- Upbeats: consonant, or a **passing tone** dissonance approached and left by step in
  the same direction.
- Consonant upbeats may leap (a "consonant skip"), which is how the line gains range.
- Start with a half rest then the first note; the penultimate bar may be a whole note
  (first-species cadence) or keep two halves (often 5th then 6th above before the octave).
- Avoid repeated notes; avoid using the upbeat to "fix" parallels it does not actually fix.

## Checking routine
1. Write intervals between the staves for every note (number only).
2. Circle every perfect interval; check how each is approached.
3. Mark every dissonance in second species: is it on a weak beat and stepwise both sides?
4. Sing each line alone; rewrite any line that is awkward to sing.

## Gotchas
- A run of parallel 6ths that ends in a leap to an octave hides direct 8ves - check outer
  approach to every perfect interval.
- Too many leaps in a row in the same direction lose the line; balance with steps back.
- "Battuta" octaves (10th to octave by contrary step) are traditionally avoided.

## Verify
- [ ] Every downbeat consonant; every dissonance is a stepwise passing tone on a weak beat.
- [ ] No parallel or direct perfect intervals.
- [ ] Correct opening and cadence for the voice position.
- [ ] Single climax; each line is singable alone.
