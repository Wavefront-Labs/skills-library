---
id: creative-arts.animation.pipeline.shot-episode-structure
name: shot-episode-structure
category: creative-arts
field: animation
product: pipeline
tags: [pipeline, shot, sequence, episode, structure, shotlist, json, schema, chunking, naming, data-driven]
level: advanced
status: verified
description: "Structure an episode as a shotlist JSON (sequences/shots with size/cast/dur_s/line_id/camera) that drives render, VO and assembly."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Shot → Sequence → Episode structure (the shotlist drives everything)

Goal: turn a 10–15 min episode into a reliable, resumable, parallelizable production —
never one monolithic job — by making **one JSON shotlist the single source of truth**.
A 15-min episode @24fps ≈ 21,600 frames; chunk it per shot. The renderer, the VO batch,
the animatic and the final assembly all read the *same* file and consume *different*
fields of it. Change the data, re-run the stage — no hidden state, no re-boarding.

## From novel to shots (the maturation chain)

```
book / CANON.md        prose truth (who, what, world facts)
  -> teleplay          acts/beats as script (the episode's dramatic structure)
    -> shotlist JSON   sequences (scenes at a location) + shots (camera setups)
      -> shots          each a render job + a VO line + a clip
```

A **sequence = one scene at one location** (its `location` is the set every shot in it
uses). A **shot = one camera setup / continuous beat** — a line of dialogue, a reaction,
an insert. The teleplay's acts map onto sequences; its beats onto shots.

## The shotlist schema (as actually consumed)

Top level (see `series/scripts/EP01_shotlist.json`):

```json
{
  "episode": "EP01",
  "title": "Reruns",
  "target_runtime_min": [10, 15],
  "voices": {"chip":"am_puck","dill":"am_adam","okafor":"am_onyx","woman":"af_sarah"},
  "sets_needed": ["mainst","kitchen","fenwick","alley","edge"],
  "sequences": [ { "id":"SQ01","name":"Cold Open","location":"mainst","shots":[ ... ] } ]
}
```

- **`voices`** — locked character → TTS voice map. This is casting-as-data; it drives
  the VO batch and is the audio half of the consistency law
  (`creative-arts.animation.pipeline.character-consistency`). Never pick a voice ad hoc;
  read it here.
- **`sets_needed`** — the set build queue; each name is a `<set>.blend` the renderer
  expects.
- **`target_runtime_min`** — the band the coverage pass aims the total `Σ dur_s` into.

A shot:
```json
{"id":"EP01_SQ01_SH020","size":"MED","camera":"static",
 "action":"Dill on the grocery wall, watching the street like a problem.",
 "cast":["dill"],"line_id":"dill_01","dialogue":"Here it comes.","dur_s":4.0,
 "fx":["gold grade"]}
```

How each field is consumed (grounding: `series/production/blender/render_shot.py` and
`series/production/build_episode.py`):

| field | consumed by | effect |
|---|---|---|
| `id` | all stages | `EP01_SQ01_SH020`; the clip, frame dir, VO key prefix |
| `size` | renderer | camera recipe `CAM[size]` = (lens, back-dist, height, fstop); `FX`/`TITLE` skip 3D entirely |
| `camera` | renderer | free-text hint; `"push"`/`"pull"` trigger a keyframed dolly, else static |
| `action` | boards / direction | animatic board text + human reference; not rendered |
| `cast` | renderer | staged on locked marks (A,B,C…); `cast[0]` = primary = speaker |
| `line_id` | VO + renderer | key to `workspace/vo/{epl}/{line_id}.wav` + `.rhubarb.json`; presence drives lip-sync + "speaker life" |
| `dialogue` | TTS source | the line voiced; also the board caption |
| `dur_s` | renderer + assembly | frame count `end = round(dur_s*24)`; clip cut to `-t dur_s` |
| `fx` | sfx-design + final splice | cue list; FX plates swapped over slates in final |
| `location` (on sequence) | renderer | `SET_MAP[location]` = the set `.blend` loaded |

The renderer resolves `location`→set, `cast`→character `.blend`s, `size`→camera, stages
cast on **locked marks**, applies VO visemes from `line_id`, and self-skips with a log if
a set or character asset doesn't exist yet (`SKIP … missing assets → BUILD QUEUE`) — so
an incomplete shotlist still produces a timed cut (missing shots become slates).

## Naming & numbering conventions

```
episode   EP01
  sequence  SQ01, SQ02 …           (a scene / location)
    shot    SH005, SH010, SH015 …  (one camera setup)
      id    EP01_SQ01_SH005        (episode_sequence_shot, fully-qualified)
      frames f_0001.png …          (zero-padded, per shot)
```

Shots numbered in **tens with 5-step headroom** (`SH005, SH010, SH015, SH020`) so an
insert drops in between without renumbering the rest (`SH008`, `SH045`). IDs are
deterministic and fully-qualified so a shot is unambiguous across the whole show and a
re-render = re-run the one id. Padded frame names (`f_%04d.png`) so ffmpeg's
`-framerate -i f_%04d.png` globs them in order.

## Build order per episode

1. **Teleplay → shotlist** — break acts into sequences (location scenes) + shots (camera
   setups) with `size`, `camera`, `dur_s`, `cast`, `line_id`, `dialogue`.
2. **VO first** (Kokoro/Piper, locked `voices`) — dialogue timing is the floor for shot
   length and drives lip-sync; set `dur_s ≥ vo_len + tail`.
3. **Animatic** — boards/blocking cut to VO; lock timing BEFORE full render (saves the
   most time). See `creative-arts.animation.editing.animatic-assembly`.
4. **Per-shot render** (`build_episode.py`, EEVEE Next) → PNG sequence per shot.
5. **Assemble** — per-shot clips cut to `dur_s` → concat → episode (animatic-assembly).
6. **Audio** — mix VO + SFX + ambience + music, master, mux
   (`creative-arts.animation.sound-design.dialogue-mix-master`).
7. **FX / grade pass** — FX plates spliced over slates in `final_assembly.py`.

## Resumability rules

- Render per shot; a failed frame costs one shot, not the episode.
- Keep intermediates (shot PNG seqs, cached `_clips` mp4s). Deliver by re-encoding/
  re-splicing, never re-render — `final_assembly.py` reuses the cached clips and only
  swaps FX.
- Match fps end-to-end (24). Verify `duration × 24 == frames` per shot.
- Lock the animatic cut; full render only after timing is signed off.
- `build_episode.py <EPID> [SEQ]` renders a single sequence for a fast proof; never
  hardcode an episode id into output names (the next episode would overwrite it).

## Throughput note

EEVEE Next cel frames render fast on the RX6900XT, so a full-episode local render in
overnight shot chunks is feasible. Reserve Cycles / heavy FX for hero shots only.

## Verify

- [ ] Every shot id is `EPnn_SQnn_SHnnn` and unique; shots numbered in tens.
- [ ] Every `cast` member has an entry in `voices` and (eventually) an asset; every set
      used appears in `sets_needed`.
- [ ] Shots with dialogue have a `line_id` whose VO wav exists before render.
- [ ] `Σ dur_s` falls inside `target_runtime_min`.
- [ ] Re-running the renderer on one `id` reproduces that shot; missing-asset shots log
      to the build queue and become slates, not failures.

status draft: the schema and consumption are grounded in the live `EP01_shotlist.json`,
`render_shot.py` and `build_episode.py`; marked draft pending review of this deepened
write-up. See `creative-arts.animation.pipeline.character-consistency` and
`creative-arts.animation.editing.animatic-assembly`.
