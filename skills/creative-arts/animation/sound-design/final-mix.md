---
id: creative-arts.animation.sound-design.final-mix
name: final-mix
category: creative-arts
field: animation
product: sound-design
tags: [sound-design, final-mix, re-recording, stems, bus, ducking, loudness, lufs, true-peak, lra, dialnorm, youtube, ffmpeg, reaper, bus-routing]
level: advanced
status: draft
description: "The re-recording final mix: stems, bus structure, ducking, dynamics/LRA, mono/stereo checks, mastered to YouTube -14 LUFS / -1.5 dBTP, deliverables."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Final mix (re-recording the episode)

**Goal:** take the finished dialogue, music, effects, foley and ambience and
balance them into one coherent, loudness-legal master for YouTube — the
re-recording mixer's job. Everything funnels here: dialogue from
`dialogue-mix-master`, score from `scoring`, designed effects from `sfx-design`,
performed sound from `foley-design`, backgrounds from `ambience-beds`. The
delivery encode itself is `youtube-master`; this skill makes the master it
encodes.

## Work in stems, not a flat soundbed

A re-recording mix is a mix *of submixes*. The five stems (DME+ split):

- **DX — Dialogue:** all VO, already edited/leveled (`dialogue-mix-master`).
  The king of the mix; everything else serves intelligibility.
- **MX — Music:** score and source music (`scoring`).
- **FX — Effects:** designed/hard effects (`sfx-design`).
- **FOL — Foley:** performed feet/cloth/props (`foley-design`).
- **AMB — Ambience:** room tone, backgrounds, beds (`ambience-beds`).

(Classic broadcast collapses to D-M-E; keep FOL and AMB split from FX because
they balance and duck differently.) Delivering stems means a note — "music too
hot," "more dialogue" — is a fader move, never a re-build. Each stem is also a
deliverable in its own right.

## Bus structure

```
DX  ─┐
MX  ─┤
FX  ─┼──► [Master bus] ──► [loudness/limit] ──► print
FOL ─┤
AMB ─┘
```

- Each stem is a bus with its own fader, EQ and (where needed) compression.
- Everything sums to one **Master bus**. Do final loudness and true-peak limiting
  **only** on the master, after the balance is right — never loudness-process
  individual stems into the master or you lose control.
- Keep ~3–6 dB of headroom on the master before the limiter so dynamics survive;
  mixing into a ceiling and "fixing it with the limiter" squashes the show.

## The balance (dialogue-led)

The hierarchy almost never changes: **dialogue intelligible first, then music
and FX shaped around it.**

- **Dialogue** sits forward and steady. In a dialogue scene it's the loudest
  consistent element.
- **Music** supports, doesn't mask — it lives mostly *under* dialogue and swells
  in the gaps (a cut-away, a reaction, the end of a line).
- **Effects/Foley** punctuate; hero hits can momentarily be loudest (a door slam,
  the seam glitch) but duck back.
- **Ambience** is the floor you rarely notice — present, low, continuous, giving
  the scene a space.

Mix the **cut**, not isolated shots: ride the stems across the scene so the
balance tracks the storytelling, and check scene-to-scene so the episode doesn't
jump in level/energy at every cut.

## Ducking (side-chain, done musically)

When music/ambience masks dialogue, duck it — but gently, not a pumping gate:

- Side-chain the MX (and sometimes AMB/FX) bus to a DX send. In Reaper: a
  compressor on MX keyed off a DX send bus.
- **Settings that read as intentional, not automatic:** ratio ~2:1–3:1, a few dB
  of gain reduction (3–5 dB, not 12), slow-ish attack (10–30 ms) so transients
  breathe, release timed to the dialogue rhythm (150–400 ms) so music recovers in
  the pauses.
- Better yet, **ride the fader** on the music for hero moments and reserve
  side-chain for the busy conversational stretches. Automation beats a blanket
  ducker for a crafted show.

## Dynamics and LRA

Loudness is not just a number; it's a *range*.

- **LRA (Loudness Range)** describes how much the loudness varies across the
  episode. Too low (<4 LU) = flat, fatiguing, over-compressed; too high for
  phone/YouTube listening = quiet dialogue lost under loud peaks. For a dialogue-
  driven web series aim roughly **LRA 6–11 LU** — dynamic enough to breathe,
  controlled enough to survive earbuds in a noisy room.
- Use gentle **bus compression** on DX for consistency, and automation/rides for
  macro-dynamics, so the micro-level is steady but the scene-to-scene arc lives.

## The YouTube master: -14 LUFS / -1.5 dBTP

YouTube normalizes playback toward **−14 LUFS integrated**; delivering near that
means YouTube won't turn you down (losing your intended balance) or up:

- **Integrated loudness: −14 LUFS** (whole-episode, program-integrated).
- **True peak: ≤ −1.5 dBTP** — headroom below 0 so the lossy AAC/Opus re-encode
  (which can overshoot sample peaks) doesn't inter-sample clip. (−1.0 is the
  common floor; −1.5 is safer for a lossy platform.)
- **LRA:** whatever your creative range lands at within the 6–11 band above.

Measure and master with ffmpeg `loudnorm` (EBU R128). **Two-pass** — measure,
then apply the measured values — because single-pass is dynamic and less exact:

```bash
# Pass 1: measure
ffmpeg -i mix.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -

# Pass 2: apply measured values (paste from pass 1)
ffmpeg -i mix.wav -af \
 loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=-18.3:measured_TP=-4.1:measured_LRA=7.8:measured_thresh=-28.7:offset=0.4:linear=true \
 -ar 48000 -c:a pcm_s24le master_-14LUFS.wav
```

Prefer `linear=true` so loudnorm applies one gain offset (preserving your careful
dynamics) rather than dynamically re-compressing. Verify the result with a second
measurement pass — see Verify.

## Mono and stereo checks (non-negotiable for web)

A huge share of the audience is on phone speakers (mono or near-mono) and cheap
earbuds:

- **Mono fold-down:** sum L+R to mono and listen. Phase-cancellation (from a
  too-wide stereo reverb, an out-of-phase effect, or a hard-panned element) can
  make a sound vanish or thin out in mono. Fix phase, narrow the offending
  element, keep dialogue dead-center and mono-safe.
- **Small-speaker check:** play the mix on a laptop/phone speaker. Dialogue must
  stay intelligible with no low end — if it only works on headphones, the balance
  is wrong for the platform.
- **Loud + quiet environment:** the −14 target with a sane LRA should keep
  dialogue audible on a train and not punishing in a quiet room.

## Reverb and space (one set of sends, shared by all stems)

A mix reads as one place when dialogue, foley and effects share the same rooms.
Build **location reverb sends** on the master session — one short/medium/long bus
per recurring location (the dry Alley, the reflective catwalk, the small
interior) — and send DX, FOL and FX to the matching send per scene at matched
levels. This is what glues performed-dry foley (`foley-design`) to production VO
and designed FX into a single acoustic space instead of three dubbed layers.
Music (MX) generally stays out of the diegetic rooms — it has its own production
reverb and lives in a non-diegetic space above the world. Keep the sends modest;
over-reverbed dialogue loses intelligibility and collapses badly in mono.

## Deliverables

- **Master:** `EPnn_master_-14LUFS_48k24.wav` (48 kHz / 24-bit PCM, −14 LUFS /
  −1.5 dBTP) — the file `youtube-master` muxes to the picture.
- **Stems:** DX, MX, FX, FOL, AMB as separate full-length WAVs at mix level
  (pre-master-limiter), for future re-versions, trailers and dubs.
- **A loudness report** (the pass-2 JSON) archived with the episode.
- Keep the Reaper session + stems versioned (`asset-management`) so any episode
  can be re-mixed or re-mastered to a new spec without redoing the sound work.

## Reference and calibration

Mix against a **reference** — a couple of released shows in the same register
(dialogue-led animation on YouTube) whose balance you admire, loudness-matched to
yours so you compare mix decisions, not levels. A/B your episode against the
reference on the same system: is your dialogue as forward, your music as
restrained, your low end as controlled? Mix at a **consistent monitoring level**
(set it once with a pink-noise/SPL check and don't ride the volume knob between
sessions) — loudness judgments drift wildly with playback level, and a mix made
loud sounds thin when played back quiet. Calibrated level + a reference is how a
single mixer keeps 10 episodes sounding like one show.

## Gotchas

- **Mastering individual stems to −14** then summing → the sum is way over and
  the balance is destroyed. Only the master hits the target.
- **True peak vs sample peak:** a mix that reads −0.1 dBFS sample peak can be
  +0.5 dBTP after AAC — always measure/limit **true peak**, hence the −1.5 ceiling.
- **Over-limiting to hit loudness:** if you're slamming the limiter to reach −14,
  your mix is too quiet/too dynamic — raise the mix level, don't crush it.
- **Pumping ducker** — a blanket side-chain at high ratio/short release sounds
  amateur; ride faders for heroes.
- **Wide stereo that collapses in mono** — check mono every time.

## Verify

1. Re-measure the printed master: `ffmpeg -i master_-14LUFS.wav -af
   loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -` reports integrated
   within ~±0.5 LU of −14 and true peak ≤ −1.5 dBTP.
2. Solo each stem: it plays complete and at mix level (not loudness-mastered); the
   five stems summed equal the pre-limiter master balance.
3. Fold the master to mono: dialogue stays centered and intelligible, nothing
   vanishes or hollows out (no phase cancellation).
4. Play the master on a phone/laptop speaker: dialogue is clear with no sub-bass
   support; then in a quiet room it isn't fatiguing — the LRA sits ~6–11 LU.
5. Trigger a hero FX hit under dialogue: it punctuates then ducks back, and the
   ducking recovers the music in the pause without audible pumping.
