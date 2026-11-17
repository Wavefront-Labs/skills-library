---
id: creative-arts.animation.pipeline.pipeline-architecture
name: pipeline-architecture
category: creative-arts
field: animation
product: pipeline
tags: [pipeline, architecture, data-driven, shotlist, json, single-source-of-truth, renderer, locked-assets, build-queue, idempotent, resumable, batch, td, automation]
level: advanced
status: draft
description: "Designing the data-driven production pipeline: shotlist-JSON as single source of truth, data/assets/tools separation, idempotent resumable batch, how the pieces fit."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Pipeline architecture (the TD view of the whole system)

**Goal:** a system where **data decides and tools execute**, so one renderer makes 870
shots instead of 870 scripts making one shot each. This is the pipeline TD's job:
decide where state lives, how the pieces talk, and why the batch can die halfway and
resume without re-doing finished work. The individual tools (`shot-renderer.md`,
`asset-management.md`, `production-tracking.md`) are already skills; this is how they
**fit together** into one coherent, data-driven whole.

---

## 1. The governing idea: data-driven, not script-driven

The failure mode of a hobby pipeline is **one bespoke script per shot**: `ep3_sh14.py`
hard-codes the camera, the cast positions, the lip-sync. 870 of those is unmaintainable
— fix a lighting bug and you edit 870 files.

The Disney-scale move (`shot-renderer` opens with it): **the shot is DATA, the renderer
is one TOOL that reads it.** All variation lives in a data record; the tool is general.
Change the camera logic once, every shot inherits it. This single decision is what makes
the show buildable by one person + automation.

Corollary: **if you're writing per-shot code, you've found a gap in the data schema or
the tool.** The fix is to add a field to the shotlist or a capability to the renderer,
not another one-off script.

---

## 2. Single source of truth: the shotlist JSON

`EPnn_shotlist.json` is the spine the whole pipeline hangs off. One record per shot:

```json
{ "id": "EP03_014", "location": "alley", "size": "CLOSE",
  "cast": ["dill", "chip"], "line_id": "EP03_014_dill_01",
  "camera": "push in slow", "action": "Dill leans in, worried",
  "duration_src": "vo" }
```

- **Every downstream stage reads this one file.** The renderer stages/frames from it,
  the tracker mirrors it, the assembler orders the cut from it, lip-sync finds the line
  from `line_id`. One edit here propagates everywhere — no field is duplicated into a
  second file that can drift.
- **It's human-authorable and diffable** (the LLM director writes it; a human reviews a
  git diff). Plain JSON, not a binary scene or a DB blob.
- **Derived data is never hand-maintained.** Rhubarb cues, render status, asset shas —
  all *computed from* the shotlist + tools, never typed twice. Two places to set a fact
  = guaranteed drift.

The test of "is X source-of-truth data or derived?": could a tool recompute it from the
shotlist and assets? If yes, it's derived — don't store it by hand.

---

## 3. Separation of data / assets / tools

Three concerns, three homes, no mixing:

```
<REPO>/
  data/    shotlists, trackers, review logs, registry   (authored/derived JSON — diffable)
  assets/  locked .blend sets, characters, props, voices (heavy binaries — versioned, immutable once locked)
  tools/   render_shot, asset registry, tracker, assembly (general code — reads data, acts on assets)
```

- **Tools never hard-code data** (no character position in a `.py`) and **never embed
  assets** (no mesh built in code) — they *resolve* both by id from data/ and assets/.
- **Assets are locked and reused** (`character-consistency.md`): a character is modeled
  once, locked, and every shot *references* that one `.blend`. Tools open-and-read the
  locked asset; they don't rebuild it. This is why consistency is free — there's one
  Dill, not 870 Dills.
- **The maps** (`SET_MAP`, `CHAR_MAP`, voice-per-character) are the bridge: id → file
  path, defined once. Add an asset = add a map entry + the file; no tool changes.

Why it matters: you can swap a tool (new renderer) without touching data, re-render all
shots from the same data after an asset fix, or hand the data to a different machine —
because the three layers are decoupled.

---

## 4. The pieces and how they fit

```
shotlist.json ─┬─> render_shot.py ──> frames/ ──> assembly ──> episode.mp4
   (truth)      │        │  ^                                       │
               │        │  └── assets/ (locked .blend, via maps)   │
               │        v                                           v
               │   build-queue (missing assets)                 final mix
               │        │                                     (dialogue-edit,
               │        v                                       final-mix)
               └──> tracker.json <── asset registry (versions, shas)
                        │
                        └──> status report / Plans Board (production-tracking)
```

- **render_shot** reads a shot record, resolves assets via maps, stages/frames/animates,
  renders (`shot-renderer`). Missing asset → skip + log to build-queue.
- **asset registry** owns asset versions/locks/shas (`asset-management`); publishing an
  asset unblocks shots; bumping a version marks dependents `needs_rerender`.
- **tracker** is the dispatcher between them (`production-tracking`): status per shot,
  the ranked build queue, blockers.
- **assembly** concatenates approved shots in shotlist order into the episode, then
  hands off to the audio chain (`dialogue-editing`, `final-mix`) and delivery
  (`../encode-delivery/youtube-master.md`).

Each arrow is a **file hand-off**, not an in-memory call — which is what makes it
resumable (§6) and inspectable (you can open any intermediate).

---

## 5. The build queue as the scheduler's input

The renderer's skip-and-log isn't just error handling — it's how the pipeline **tells
you what to build next**. Aggregate every `missing:<asset>` across all trackers, rank
by shots-blocked, build the highest-leverage asset first (`production-tracking` §queue;
`producing-scheduling.md` turns this into a work plan). The data demand decides the
build order; no one guesses. This is the pipeline being *self-directing*.

---

## 6. Idempotent, resumable batch (the non-negotiable)

870 shots will not render in one unbroken run — a crash, a power cut, an OOM will stop
it. The batch **must** survive that:

- **Idempotent:** rendering the same shot twice gives the same result and is safe. No
  "append to a log" or "increment a counter" side effects that double on re-run.
- **Resumable / skip-done:** before rendering, check the output exists *and matches the
  current input versions* (sha of the shot record + its assets). If so, skip — don't
  re-render finished work. A plain "output file exists" check is **not** enough; it
  ships stale frames after an asset bump. Key the done-check on the **content hash**,
  not just presence.
- **Per-shot isolation:** one shot's failure logs and continues; it never aborts the
  batch. The run renders the whole coverable subset and reports what it skipped/failed.
- **Deterministic:** fixed seeds for any procedural/idle so a re-render of an unchanged
  shot is bit-stable — otherwise the skip-done hash never matches and you re-render
  forever.

```python
# ponytail: content-hash skip-done — presence-only check ships stale frames after an asset bump
def should_render(shot, assets, out):
    want = sha(shot_record(shot), *[asset_sha(a) for a in assets])  # input identity
    done = read_sidecar(out)        # the hash we rendered last time, stored beside frames
    return not (out_exists(out) and done == want)
```

This is the difference between a batch you *trust* (re-run anytime, it does only the
work that's actually needed) and one you babysit.

---

## 7. TD principles that keep it from rotting

- **Add a field, not a script.** New per-shot need → extend the schema + the general
  tool. Resist the one-off.
- **One writer per fact.** Renderer writes render status; registry writes asset
  versions; humans write creative state only. Two writers = drift.
- **Everything is a file hand-off**, diffable and inspectable. No hidden in-memory
  state between stages.
- **Fail loud, skip safe.** Missing/broken input → log + skip that unit, never fake it,
  never abort the batch.
- **Immutable locked assets.** A locked asset only changes via a version bump that
  marks dependents stale — never silently edited under running shots.
- **Scale the tool to the team.** A solo/automated show uses JSON files + scripts, not
  Shotgun/USD/OpenPipeline — the architecture principles are the same, the weight isn't.

---

## 8. Anti-patterns (how a data-driven pipeline rots back into chaos)

- **The one-off script creeps back.** `fix_ep3_sh14.py` to patch a single shot — the
  moment one exists, the data-driven contract is broken and 870 siblings diverge. Fix:
  the patch is a data field or a tool capability, always.
- **A fact stored twice.** Shot duration in the shotlist *and* copied into the tracker;
  they drift. Fix: derive one from the other, never store both.
- **Presence-only done-check.** "the mp4 exists so skip it" ships stale frames after an
  asset bump. Fix: hash the inputs (§6).
- **Asset edited in place under running shots.** A silent mesh tweak changes shots
  nobody re-reviewed. Fix: immutable locked assets, change via version bump only.
- **In-memory coupling between stages.** The renderer calling the tracker's functions
  directly makes the batch un-resumable and un-inspectable. Fix: file hand-offs.
- **Right-sizing upward too soon.** Reaching for USD/Shotgun/a job scheduler for a solo
  show. Fix: JSON + scripts until a measured limit forces more.

## 9. Scaling knobs (when the simple version stops holding)

The architecture holds for a solo/small series; know the upgrade path before you need
it, not under fire:

- **Tracker/registry scans slow** (>~1k shots per episode, cross-episode queries) →
  move the JSON into SQLite, keep the same schema and the same file hand-off contract.
- **One machine can't render in time** → the resumable, content-hash batch already
  shards cleanly: split the shot list across machines, each skips what's done; no logic
  change because shots are independent units.
- **Many hands join** → the "one writer per fact" rule is what makes that safe; add
  per-department ownership, not a new tool.

Each knob is reachable *because* the layers are decoupled and state lives in files —
the simple version doesn't have to be thrown away to scale.

---

## Verify

1. **No per-shot code.** Grep the tools: no shot id or character position hard-coded in
   any script — all variation comes from the shotlist. Rendering a brand-new shot needs
   zero new code.
2. **Single source.** Change one field in the shotlist (e.g. a shot's `size`); the
   renderer, tracker and assembly all reflect it with no other file edited.
3. **Layer swap.** Point the asset maps at a different set `.blend`; shots re-render
   from the same data/tools unchanged — proving data/assets/tools are decoupled.
4. **Resumable batch.** Kill the batch mid-run, restart it: finished shots are skipped
   (hash match), only unfinished/stale ones render, and the final result equals an
   uninterrupted run.
5. **Stale-safe skip.** Bump an asset version, re-run: shots using it re-render
   (hash mismatch) while untouched shots skip — a presence-only check would wrongly
   skip the stale ones.
6. **Self-directing.** Withhold an asset; the build queue ranks it by shots-blocked and
   names it as next-to-build with no human deciding the order.

See `shot-renderer.md` (the general tool), `asset-management.md` (versions/locks/shas),
`production-tracking.md` (the dispatcher), `producing-scheduling.md` (turns the queue
into a plan), `character-consistency.md` (why locked reuse works),
`../blender/blendercraft-headless.md` (driving Blender headless in the batch).
