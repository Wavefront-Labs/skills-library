---
id: creative-arts.animation.sound-design.dialogue-editing
name: dialogue-editing
category: creative-arts
field: animation
product: sound-design
tags: [sound-design, dialogue-editing, dialogue, vo, adr, tts, kokoro, piper, rhubarb, de-ess, noise, breath, ffmpeg, stem, comping]
level: advanced
status: draft
description: "Editing the dialogue track before the mix: comping takes, timing to picture, cleanup, ADR, episode consistency, prepping the stem for Rhubarb and final mix."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Dialogue editing (cutting the VO track, before the mix)

**Context:** this is the step *between* generating/recording voice
(`../pipeline/vo-lipsync-pipeline.md`) and mixing it (`dialogue-mix-master.md`,
`final-mix.md`). The mixer sets levels, EQ and balance; **the dialogue editor decides
which words the audience hears, exactly when, and clean of everything that isn't the
performance.** In a production pipeline the voice is local TTS (Kokoro/Piper), so "takes" are
*generations* and "ADR" is a *re-generation* — the craft is identical, the source
differs. A great edit makes a flat TTS read sound intentional; a sloppy edit makes
even good VO feel amateur.

---

## 1. The job, defined

Editing ≠ mixing. The dialogue edit delivers, to the mixer, a **clean, correctly
timed, consistent dialogue stem** with:

- the best take of every line chosen and comped,
- each line placed to picture (lip-sync frame-accurate),
- breaths/clicks/mouth-noise/room cleaned to taste,
- consistent level and tone line-to-line across the whole episode,
- handles and a conform that matches the locked cut.

Everything about *character balance, music ducking, final loudness* is downstream in
`final-mix`. Keep those out of the edit.

---

## 2. Selecting and comping takes

With TTS you generate several candidates per line (varying `--length_scale`, seed,
phrasing, punctuation) and pick:

- **Intelligibility first, then performance.** A take where a word mushes is out, no
  matter how nice the cadence. Read along to the script line.
- **Comp across takes.** The best reading of a sentence is often take 2's first half +
  take 4's end. Cut at a **silence or a plosive/stop consonant** (p, t, k, b, d, g) —
  never mid-vowel, which clicks. Crossfade 3–10 ms over the join.
- **Punctuation drives TTS prosody.** If a line lands flat, fix the *input text*
  (comma, em-dash, ellipsis, sentence split) and regenerate rather than warping the
  audio. A comma buys a micro-pause; an em-dash buys a longer one.
- **Keep a take log** per `line_id`: which generation won, its settings — so a
  pickup months later matches (consistency law).

---

## 3. Timing to picture

Dialogue serves the cut and the mouth.

- **VO sets shot duration here, not the reverse** — the renderer takes frame_end from
  the line (`vo-lipsync-pipeline` §pitfalls). So lock the edit of a line *before* it
  drives lip-sync.
- **Trim head/tail silence hard**, but leave a **few frames of handle** — a hard cut
  on the first phoneme clips the attack and sounds gated.
- **Respect the beat.** A line that must land on an action frame gets nudged (whole-ms
  moves) so the stressed syllable hits the picture accent. Overlaps (one character
  starting before another finishes) are placed here, not left to the mixer.
- **Room to breathe.** Don't butt every line wall-to-wall; a 4–8 frame gap between
  speakers reads as conversation, not a list.

---

## 4. Cleanup

The unglamorous core. Clean dialogue is invisible; dirty dialogue is all the audience
hears.

- **Breaths.** TTS usually has none (sounds robotic) or odd ones. Either leave natural
  inhales at a low level for life, or remove/attenuate intrusive ones — be *consistent*
  within a character. Don't silence-gate breaths to absolute zero; duck ~12–18 dB so
  the track doesn't "pump".
- **Clicks / mouth ticks.** Zoom to sample level, find the transient, pencil/redraw it
  out or cut a 1–3 ms slice with micro-crossfades. Common at TTS word joins.
- **De-ess.** Neural TTS over-sharpens sibilants. A de-esser (or a narrow dynamic
  cut ~5–8 kHz) tames harsh s/sh — subtle; over-de-essing gives a lisp.
- **Noise / hum.** Local TTS is clean, but recorded pickups or Kokoro artefacts may
  carry a floor hiss — a light broadband denoise or a learned noise print, gently
  (aggressive denoise = underwater artefacts).
- **Plosive pops** on p/b — high-pass or a short volume dip on the pop only.
- **Fades everywhere.** Every cut edge gets a tiny fade (1–5 ms) so no join clicks.

Order: comp → trim/time → declick → denoise → de-ess → breaths. De-noise before
de-ess (noise confuses the de-esser).

---

## 5. ADR = re-generation (the TTS equivalent)

Traditional ADR re-records a line that failed (bad read, line change, lip mismatch).
Here, ADR is **re-generating the line** and re-cutting it in:

- **Trigger:** script change, a flat/unclear read, or a timing that won't fit the
  shot's mouth. Re-generate from the corrected text with the character's **locked
  voice file** (never swap voices — consistency).
- **Match the surroundings.** A pickup line must sit at the same level/tone as its
  neighbours. Edit it to the same cleanup recipe, match level to the adjacent lines
  *before* handing to the mix.
- **Re-cut lip-sync.** A re-generated line has new duration and new Rhubarb cues —
  re-run Rhubarb and re-key the mouth (`../blender/lip-sync.md`). An ADR line with the
  old mouth is the classic mismatch.

---

## 6. Consistency across an episode

A whole episode must sound like one continuous world, not 87 separately-generated
clips.

- **One voice file per character, episode-wide** — set in the voice-casting lock.
- **Match level line-to-line.** Normalize each character's lines to a consistent
  working level (e.g. about -18 to -16 dBFS RMS on the stem, before the mix sets final
  loudness). The mixer should receive an *already-even* track, not a roller-coaster.
- **Match tone.** Same de-ess/EQ character-wide, so a character doesn't get brighter
  mid-episode.
- **Name and conform** every clip to `EPnn_shot_line_id` so the edit maps 1:1 to the
  shotlist and a re-cut is traceable.

---

## 7. Delivering the dialogue stem

Hand the mixer a single, clean **dialogue stem** (or one per character if the mix
wants splits), conformed to the locked picture, correct sample rate (48 kHz for video
delivery), with handles. Keep it **pre-fader of the final loudness pass** — the stem
is edited and even, not loudness-normalized to -14 LUFS (that's `final-mix` /
`../encode-delivery/youtube-master.md`'s job for the full mix).

Useful ffmpeg for edit chores (not a mixer, but handy):
```
# trim head/tail silence conservatively, keep handles
ffmpeg -i line.wav -af "silenceremove=start_periods=1:start_silence=0.1:start_threshold=-45dB:stop_periods=1:stop_silence=0.15:stop_threshold=-45dB" line_trim.wav
# measure a line's level (match lines to each other)
ffmpeg -i line.wav -af ebur128 -f null -
# gentle de-ess via a dynamic sibilance cut (tune freq/threshold)
ffmpeg -i line.wav -af "deesser=i=0.4" line_dess.wav
```
Do the delicate declick/comp work in an audio editor (Audacity/Reaper/ocenaudio);
ffmpeg is for batch trims, level measurement and muxing, as in `vo-lipsync-pipeline`.

---

## 8. TTS-specific failure modes (and the edit fix)

Local neural TTS fails in predictable ways; recognizing them is half the edit.

| Symptom | Cause | Edit fix |
|---------|-------|----------|
| Flat, no emphasis | punctuation too plain | add comma/em-dash/split sentence, regenerate |
| Runaway pace, no air | no sentence breaks | split the line into two generations, add gap |
| Word mushed/dropped | tricky grapheme (name, number) | spell it phonetically in input, or comp the word from another take |
| Harsh sibilant | neural over-sharpening | de-ess (§4) |
| Click at word join | concatenation artefact | declick at sample level (§4) |
| Robotic evenness | no breaths, metronomic | insert low-level breaths, micro-vary line gaps |
| Wrong stress on a name | model guesses | respell or re-phrase; last resort, pitch-nudge the syllable |

The recurring lesson: **fix the input text and regenerate before you fix the audio.**
TTS gives you infinite takes for free — a better comma is cheaper and cleaner than a
sample edit. Reserve destructive audio editing (declick, de-ess, comp) for artefacts
the text can't cure.

## 9. Worked example (one line, start to finish)

`EP03_014_ivy_01` — "A new viewer! No, better than that. Welcome to the show, Ivy!"

1. Generate 3 takes (`--length_scale` 1.0 / 1.1 / 1.15). Take 2 reads warm but rushes
   "Welcome to the show"; take 3 nails the welcome but drags the open.
2. **Comp:** take 2's "A new viewer! No, better than that." + take 3's "Welcome to the
   show, Ivy!" Cut at the period (a stop), 5 ms crossfade.
3. **Clean:** a click at the comp join → declick; a sharp "show"/"s" → light de-ess;
   add a soft inhale before "Welcome" for life.
4. **Time:** trim 80 ms of head silence (keep 2-frame handle), nudge so "Ivy!" lands
   on the lean-in action frame.
5. **Level:** match to EP03's other Ivy lines (~-17 dBFS RMS).
6. **Hand off:** re-run Rhubarb on the comped clip (new cues), log the take recipe,
   deliver to the stem. The line is now the shot's locked duration driver.

This is the whole loop: choose → comp → clean → time → match → conform, logged and
repeatable.

---

## Verify

1. **Intelligibility pass.** Play the stem against the script at low volume — every
   word is clear; no mushed or clipped line attacks.
2. **Click/pop pass.** Solo the dialogue, listen on headphones at the edit points — no
   clicks at cuts, no plosive pops, no abrupt breath cutoffs.
3. **Level-match pass.** Run `ebur128`/RMS across all lines of one character — they sit
   within ~2–3 dB of each other, no line jumping out.
4. **Timing pass.** Scrub the cut — each line's stressed syllable lands on its picture
   beat, speaker gaps feel conversational, and lip-sync still matches after any ADR.
5. **ADR pass.** Any re-generated line matches its neighbours in level/tone and has
   fresh Rhubarb cues driving the mouth (no old-mouth mismatch).
6. **Hand-off.** The mixer gets a conformed, even, declicked stem at 48 kHz with
   handles — not loudness-normalized, not mixed.

See `../pipeline/vo-lipsync-pipeline.md` (generate + lip-sync), `../blender/lip-sync.md`
(re-keying mouths after ADR), `dialogue-mix-master.md` and `final-mix.md` (the mix this
feeds), `../encode-delivery/youtube-master.md` (final -14 LUFS delivery).
