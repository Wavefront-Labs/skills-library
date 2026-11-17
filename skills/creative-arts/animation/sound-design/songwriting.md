---
id: creative-arts.animation.sound-design.songwriting
name: songwriting
category: creative-arts
field: animation
product: sound-design
tags: [sound-design, songwriting, musical, song, lyrics, rhyme, scansion, melody, hook, i-want-song, villain-song, verse-chorus, bridge, mido, midi, fluidsynth, soundfont, demo-vocal, tts, stems, arrangement, local]
level: advanced
status: draft
description: "Write songs for animation locally: song spotting, verse/chorus structure, lyric craft (rhyme, scansion, character voice), melody via mido->FluidSynth+SoundFont, demos, stems to final mix."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# songwriting

Goal: the feature-animation musical number — an I-want song, a villain number, an
ensemble opener — written, composed and demoed **entirely locally**: lyrics by hand,
music as code-controlled MIDI (mido) rendered through FluidSynth + a free SoundFont,
no cloud music-gen. The render toolchain, tempo-map and stem conventions are
`creative-arts.animation.sound-design.scoring`; this skill is the *songwriting
craft* on top: when to write a song, how to structure it, and how to get it to
picture and into `creative-arts.animation.sound-design.final-mix`.

## Song spotting: when a song replaces a scene

A song is the most expensive scene in the show — spot them like a dramatist, not a
fan:
- A song earns its slot when **emotion exceeds what dialogue can carry without
  embarrassment**: a character must say something too big, too interior, or too
  fast (a montage of change) for prose. The test: write the scene as dialogue; if
  the dialogue version is either a monologue or a therapy session, it's a song.
- A song must **move the story**: the character who ends the song is not the one
  who started it (decision made, mask dropped, alliance formed). A song after
  which nothing has changed is a music video and gets cut.
- Classic spots that work: the **I-want** early (establishes the engine of the
  season/film — always first act); the **villain number** at the power peak; the
  **ensemble/opener** to install world + rules fast; the **dark reprise** of the
  I-want when the want has curdled. One reprise maximum per song; reprises are
  payoffs (`comedy-writing`'s callback math applies — recall × new context).
- Comedy songs obey comedy rules: the song's *premise* is the setup, each verse an
  escalation rung, the bridge the topper. A funny song that is only funny for one
  verse is a 40-second song — length follows joke inventory, not genre habit.
- Spotting is an editorial decision: agree the slot, the in-cue and out-cue with
  `creative-arts.animation.editing.editorial-pacing` before writing a note.

## Structure

The working skeleton (deviate on purpose, never by accident):

**Verse 1 → Pre-chorus → Chorus → Verse 2 → Pre → Chorus → Bridge → Final chorus
(lifted)**

- **Verse** = story/specifics: new information each verse, conversational melody in
  a comfortable range. **Pre-chorus** = the ramp: harmonic tension (move off the
  tonic), rising melody, shorter lines. **Chorus** = the thesis: the title phrase,
  the biggest interval, the highest sustained notes; it must be singable by the
  audience after one hearing. **Bridge** = the other point of view or the doubt —
  new chord territory (relative minor/major, or the bVI), then the final chorus
  **lifts**: up a key (+2 semitones is the honest workhorse), or adds the
  countermelody/ensemble.
- Animation-length discipline: a series number is **90 seconds to 2:30**. Cut
  verse 3; nobody has ever missed verse 3.
- Map structure to picture **before composing**: each section gets a storyboard
  beat (verse = walking the village, chorus = climbs the roof). Songs are shot in
  sections; your section boundaries are editorial cut points, so put them on
  whole-bar, whole-second boundaries at your chosen tempo (e.g. 120 bpm → 2 s per
  bar; a 16-bar verse = 32 s exactly — the same frame-math discipline as
  `scoring`'s tempo map).

## Lyric craft

- **Character voice first.** A lyric is dialogue that rhymes: vocabulary, syntax
  and education level must match the speaker. The villain gets polysyllabic rhymes
  and legato lines; the kid gets monosyllables and shouted fourths. Run every line
  through the same voice-test as script dialogue — if another character could sing
  it, sharpen it.
- **Scansion is non-negotiable.** Stressed syllables must land on strong beats.
  Write the stress pattern over each line (da-DUM da-DUM...), then force melody to
  agree. The amateur tell is a wrenched stress ("to-DAY i am be-COM-ing" with COM
  on a weak beat). Sing every line on one note against a metronome before it
  keeps its place.
- **Rhyme schemes:** verses AABB or ABAB; pre-chorus can go rhymeless (tension);
  chorus rhymes hardest. **Perfect rhymes for comedy and villains** (precision
  reads as wit and control), near-rhymes (time/mine) acceptable for sincere
  ballads where perfection sounds glib. Interior rhyme is the champagne —
  budget it for the showcase lines. Never rhyme on filler words ("do/you/too"
  chains); rhyme on nouns and verbs carrying image.
- **One image system per song.** The I-want picks its metaphor (horizon, locked
  door, river) and mines it; grab-bag imagery is the #2 amateur tell.
- **Song-type specifics:** *I-want*: first person, present tense, concrete want
  plus the fear under it; must state the want inside the first chorus. *Villain*:
  the villain is the hero of this song — seduction, logic, grievance; give them
  the best tune in the show and let the lyric's self-justification expose them.
  *Ensemble*: assign lines by what each character would notice; counterpoint
  section (two melodies collide) is the form's payoff — write the two lyrics to
  answer each other.

## Melody and hook over the local toolchain

Compose as MIDI via `mido`, audition through FluidSynth + the show SoundFont —
same pipeline, programs and render flags as `scoring` (that skill owns the
`fluidsynth -ni <soundfont>.sf2 cue.mid -F cue.wav -r 48000` render and stem
conventions). Songwriting-specific craft:

- **Hook first.** Write the chorus's title phrase melody before anything: 4–8
  notes, one leap (a fourth, fifth or sixth — leaps are hooks, steps are
  wallpaper), landing on a chord tone, rhythm you can clap. Everything else in
  the song is approach and retreat from that cell. Verse melodies sit lower and
  stepwise so the chorus leap *earns* its height.
- **Range discipline:** keep each character's song within about a tenth, placed
  where their (eventual) voice lives; write the demo key low — raising a key later
  is painless in MIDI (`msg.note + 2`), a blown-out demo vocal is not.
- Sketch pattern in mido: a chord track (pads, program per `scoring`'s palette), a
  bass root track, and the **melody as its own track** named `LEAD` — that track
  later becomes the vocal guide and the karaoke stem's mute target. Keep a
  `sections = [("V1", bars 0-16), ("CH", 16-24), ...]` table in the script so
  structure edits are one-line changes and every section renders to a known
  timecode.
- Humanize deliberately, not randomly: melody quantized (it must be learnable),
  accompaniment ±10 ticks and velocity contour rising into the chorus. Velocity
  *is* your dynamics under a SoundFont — write the crescendo into velocities, don't
  expect the patch to breathe for you.
- Audition loop: render section, listen against boards/animatic, adjust, re-render.
  SoundFont GM patches are the demo reality: prefer patches that state pitch
  clearly (piano 0, strings 48, lead 80/81) for the writing phase; orchestration
  color comes later via `scoring`'s arranging palette.

## Demo vocals: local TTS limits and alternatives

Be honest about the gap: local TTS (the show's scratch-dialogue stack, e.g.
Kokoro-class voices) **speaks, it does not sing** — no sustained pitch, no vibrato,
no melisma. Options, in order of practical value:
1. **Sing it yourself** into any mic, pitch guide = the rendered `LEAD` stem in
   headphones. An imperfect human scratch vocal communicates a song to the team
   100× better than any synthesis; tune-tolerance for a scratch is high.
2. **Instrumental lead + lyric subtitles** on the animatic: `LEAD` on a vocal-ish
   patch (oboe 68, synth voice 54) with the lyric burned into picture. The
   standard "demo love theme" move; fine for editorial sign-off.
3. **Spoken-over-track**: TTS reads the lyric *rhythmically* (write it with
   line-break pacing), mixed under the instrumental — works surprisingly well for
   patter/villain-monologue sections, badly for ballads.
4. Open-source singing synthesis (DiffSinger-class / UTAU-class local tools)
   exists but costs real setup and voicebank licensing care — evaluate only when a
   number must ship without a human scratch; treat as unverified until the show
   has run one end-to-end.
Never storyboard timing to a spoken-word demo of a sung line: sung lines are
~30–60% longer. Time boards to the MIDI `LEAD`, not the TTS.

## Arranging to picture

- Arrange **after** picture lock of the sequence (or to a locked animatic):
  conform the section table to final cut-times first, then orchestrate — the
  reverse order means re-voicing every instrument when editorial trims 20 frames.
- Density maps to visual scale: verse walking = rhythm section light; chorus wide
  shot = pads + countermelody + the drum build. **The vocal owns 1–4 kHz**: keep
  accompaniment out of the melody's register while anyone sings (drop the
  countermelody an octave, save it for instrumental turnarounds).
- Hits and catches (a door slam on beat 4, the pratfall on the drum fill) are
  spotted like score stingers — frame-accurate via the tempo map; leave 1 beat of
  clearance around sung words so SFX don't fight lyrics
  (`creative-arts.animation.sound-design.sfx-design`).
- Dialogue inside a song (spoken interjections) sits in planned **holes**: write
  the hole into the MIDI (accompaniment thins to bass + pad for those bars);
  don't rely on the mix to duck it cleanly.

## Handing stems to final mix

Deliver per `scoring`'s stem conventions, plus song-specific splits:
- Render **grouped stems**, 48 kHz WAV, from bar 0 so everything aligns on drop:
  `RHYTHM` (drums/bass), `HARMONY` (pads/comping), `LEAD` (melody guide),
  `COUNTER` (countermelodies/hits), and the scratch `VOX` as its own file with a
  matching **lyric/timing sheet** (lyric line → bar/beat → timecode).
- Always render the **karaoke version** (all minus LEAD/VOX) — editorial will ask
  for it within the hour, for underscore reuse of the song's theme if nothing
  else.
- Mix targets, headroom and loudness are owned by
  `creative-arts.animation.sound-design.final-mix`; vocal-vs-dialogue level
  philosophy by `creative-arts.animation.sound-design.dialogue-mix-master` — a
  sung vocal is treated as dialogue (always intelligible), which is why the
  arrangement left it room.
- Keep the mido source scripts in `<REPO>/audio/songs/<song>/` next to the
  rendered stems: the script is the session; there is no DAW file to lose.

## Verify

- [ ] Spotting: dialogue version of the scene reads as monologue/too-big → song
      justified; character ends the song changed; slot + in/out cues agreed with
      editorial.
- [ ] Structure lands on whole bars; section table timecodes match the animatic
      cut points; total length ≤ 2:30.
- [ ] Every line scans: stressed syllables on strong beats when sung against a
      metronome; no wrenched stresses.
- [ ] Rhyme scheme consistent per section; comedy/villain rhymes perfect; one
      image system; title phrase appears in the first chorus.
- [ ] Hook test: a teammate sings the chorus back after one listen.
- [ ] Melody range within ~a tenth; `LEAD` is its own track; karaoke stem mutes
      cleanly.
- [ ] Demo path chosen per the ladder above; boards timed to MIDI `LEAD`, not to
      a spoken TTS read.
- [ ] Stems (`RHYTHM/HARMONY/LEAD/COUNTER/VOX` + karaoke) rendered from bar 0 at
      48 kHz with the lyric timing sheet; mido sources committed under
      `<REPO>/audio/songs/<song>/`.
