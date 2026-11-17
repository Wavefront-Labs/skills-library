---
id: creative-arts.animation.pipeline.asset-sourcing
name: asset-sourcing
category: creative-arts
field: animation
product: pipeline
tags: [assets, cc0, sourcing, kitbash, base-mesh, library, licensing, provenance, reuse, quaternius, kenney, polyhaven, ambientcg, mocap, blender]
level: advanced
status: verified
description: "Source and modify open-licence assets instead of modelling from primitives: what to pull, how to licence-clear it, and how to build a reusable cross-project asset library."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Asset sourcing — the professional alternative to building from primitives

**The single highest-leverage correction an automated pipeline can make.** Hand-coding
characters and sets out of spheres, cubes and cylinders has a *hard ceiling at blockout
tier* — no lighting, comp, animation or render-time rescues it, because there is no
modelling underneath. Studios don't sculpt every human from nothing; they start from
base meshes and kitbash libraries. The professional skill is **source and modify**, not
*build from zero*.

## What to source, and what each solves

| Need | Source (licence) | Solves |
|---|---|---|
| Character anatomy | **Blender Studio Human Base Meshes** (CC0) — stylized + realistic bodies, heads, hands, feet, eyes; clean quad topology | Real anatomy, **hands with fingers**, riggable topology |
| **Rig + animation** | A **universal rigged character + matching animation library** (e.g. Quaternius Universal, CC0): one shared skeleton, 100+ clips | Kills the "no skeleton, no animation" blocker outright |
| **Clothing** | **Modular outfit parts skinned to the same universal skeleton** (e.g. Quaternius Modular Outfits, CC0: body / arms / legs / feet per outfit) | Modelled hems, cuffs, belts and boots that animate with every library clip; replaces garments derived from the body mesh (z-band cuts leave sawtooth hems and bare feet) |
| Body motion | **CMU Motion Capture Database** (free, ~2.5k BVH clips) | Walks, runs, turns, idles, gestures, sits, falls |
| Stylized sets/props | **Kenney**, **Quaternius** (CC0) — modular city/interior/nature/vehicle kits | Set density by kitbash instead of extruded boxes |
| Realistic props/materials/HDRI | **Poly Haven**, **ambientCG** (CC0, both have APIs) | Lighting environments + PBR surfacing |
| Audio / music / fonts / VFX overlays | Kenney audio, GM soundfonts, OFL fonts, CC0 element packs | Score, foley, titles, comp elements |

## The library: build it ONCE, outside any project
A per-project asset dump is waste. Keep **one standalone library** (e.g. `<LIB_ROOT>`),
peer to your projects, so every future production reuses it:
```
<LIB_ROOT>/base-meshes  characters-stylized  models-stylized  models-realistic
           nature  vehicles  hdri  materials  mocap  audio-sfx  audio-music
           soundfonts  fonts  vfx-elements  brushes-alphas
           tools/   _src/   LIBRARY.md
```
- **`CATALOG.md` per folder** — a table of asset | purpose | format | source URL | **licence**.
- **`LIBRARY.md`** — master manifest: counts, sizes, licence rules, known gaps, workflow.
- **`_src/`** — the original archives, so the library is reproducible.
- **`tools/`** — *idempotent* fetchers (skip what exists, verify downloads, print a summary)
  so any category can be topped up later without redoing the research.

## Licence discipline (non-negotiable)
- **CC0** — use/modify/ship commercially, no credit. Prefer it.
- **CC-BY** — commercial OK but **credit is mandatory**; track which assets oblige you.
- Watch for **custom licences** and **"free Standard editions"** that are a deliberate
  subset of a paid version — both appear inside otherwise-CC0 catalogues.
- Accounts-required libraries (e.g. Mixamo) — verify terms per use, never assume.
- **Nothing enters production without a catalogue row recording source + licence.**

## Acquisition gotchas (all hit in practice)
- **Download pages aren't downloads.** A "zip" of ~48 KB is an HTML redirect page. Always
  verify type/size; scrape the real mirror link and retry. Automate this check in the fetcher.
- **APIs beat scraping** where they exist (Poly Haven, ambientCG) — and may need a
  `User-Agent` header or they 403 the default urllib agent.
- **Google-Drive-hosted packs** hit server-side quota walls and have no scriptable route;
  record the links as a known gap rather than pretending coverage.
- Prefer **2k** textures/HDRIs over 4k/8k — breadth of coverage beats resolution for animation.
- **Kit colour lives in different places per pack — check before restyling.** Kenney
  city/urban kits carry one `colormap` ATLAS texture (colour = UV position; a
  base-colour socket read returns fallback grey). Kenney's nature/furniture kits carry
  FLAT per-part materials, no atlas. Any restyle pass (cel conversion, outline) must
  resurface **per material slot** and keep the atlas image in the new chain where one
  exists — collapsing an object to one material strips the palette, and the same bug
  re-appears in EVERY later pass that touches materials (shell pass fixed ≠ dress pass
  fixed; it recurred exactly there). Never read `default_value` off a LINKED socket —
  it is a stale near-black leftover.
- **Modular outfit parts: import, bin their armature, weld to YOUR rig.** Each part
  ships with its own copy of the skeleton; keep only the mesh, parent it to the
  production rig with an armature modifier (vertex groups already carry the bone
  names), apply the same restyle law as the body, then delete the body faces the
  part covers (faces whose every corner's dominant bone is a covered bone; keep the
  neck ring). The Arms part brings its own hands - cut them off the part and keep the
  base hands if those already read. Check the part's joint list from the glTF before
  trusting what "Arms" means.
- **Modular "block" pieces read as boxes** when scattered as organic set dressing
  (`cliff_block*` = square construction modules). For nature scatter use the organic
  pieces (`rock_large[A-F]`), keep blocks for built structures.

## Verify
- [ ] Library lives OUTSIDE any single project and is referenced by at least two.
- [ ] Every folder has a `CATALOG.md`; every row names a licence.
- [ ] Re-running a fetcher downloads nothing new (idempotent) and reports a summary.
- [ ] No file is a disguised HTML error page (spot-check types and sizes).
- [ ] CC-BY obligations are listed somewhere the credits roll can be built from.
- [ ] A character can be started from a base mesh, and a set kitbashed, without modelling
      a primitive by hand.

**Verified (proof):** built a 16 GB, 45k-file cross-project library (CC0 human base meshes,
90 Kenney/Quaternius kits, 64 HDRIs, 79 PBR sets, 43 realistic props, 2,548 CMU BVH clips,
soundfonts, OFL fonts, VFX overlays) with per-folder catalogues, a master manifest and
four idempotent fetchers. It immediately replaced primitive-built characters and exposed a
non-CC0 pack plus eight "Standard edition" subsets that a naive pull would have shipped.

See asset-management (versioning + the lock-and-reuse law), character-modeling,
environment-modeling, mocap-retarget, rigging, production-tracking.
