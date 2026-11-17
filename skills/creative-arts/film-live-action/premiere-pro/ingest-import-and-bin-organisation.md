---
id: creative-arts.film-live-action.premiere-pro.ingest-import-and-bin-organisation
name: ingest-import-and-bin-organisation
category: creative-arts
field: film-live-action
product: premiere-pro
tags: [premiere-pro, film-live-action, ingest-presets, ingest-copy, ingest-transcode, premiere-bins, labels, metadata-search, import-formats, camera-folder-import, image-sequence-import, media-browser, search-bins]
level: practitioner
status: draft
description: "Bring media into Premiere Pro properly: ingest settings (copy, transcode, proxies), Media Browser for camera folders and image sequences, bins, labels and search bins."
sources:
  - "https://helpx.adobe.com/premiere-pro/using/ingest-proxy-workflow.html (Adobe - Ingest and proxy workflow)"
  - "https://helpx.adobe.com/premiere-pro/using/importing-media.html (Adobe - Importing media; Media Browser)"
  - "Adobe Certified Professional - Premiere Pro exam objectives (project setup and organisation)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ingest, import and bin organisation in Premiere Pro

**Goal:** every clip imported with its metadata intact, copied/transcoded per the
workflow, and findable in seconds.

## 1. Ingest settings
In **Import mode** (top-left) or *Project Settings > Ingest Settings*:
- **Copy**: copies media to a destination (with verification options in recent versions)
  - for card offloads straight into the project's media folder.
- **Transcode**: converts to a mezzanine codec preset (ProRes 422, DNxHR) on import.
- **Create Proxies**: generates proxies via Media Encoder (see proxy skill).
- **Copy and Create Proxies**.
Presets are Media Encoder ingest presets; save custom ones for the show.

## 2. Importing camera media
- Use **Media Browser** (or Import mode browser) for camera card structures (XAVC,
  P2, RED, ARRI MXF, Canon XF): it reads the folder structure and **spanned clips** as
  single clips with metadata. Copy the **entire card folder structure** to storage first;
  never import loose files from deep inside a card.
- **Image sequences** (EXR/DPX/PNG): select the first frame and tick **Image Sequence**
  in the import dialog (or Media Browser); set the frame rate via *Modify > Interpret
  Footage* if needed.
- Check **Interpret Footage** for frame rate, pixel aspect and alpha on unusual media.

## 3. Bins and structure
A standard project template:
`01_DAILIES/DAY01...`, `02_SCENES/Sc024...`, `03_SOUND/`, `04_MUSIC/`, `05_GFX/`,
`06_VFX/`, `07_SEQUENCES/WORKING|ARCHIVE|OUTPUT`, `08_REFERENCE/`. Duplicate project
templates for each show.

## 4. Labels and metadata
- **Labels** (colours) by type: e.g. Violet = video, Iris = audio, Mango = graphics,
  Rose = VFX. Customise in *Preferences > Labels*.
- Metadata panel: fill **Scene, Shot/Take, Description, Comment, Good** (circle) - or import
  from sound/camera metadata. Show columns in List view.
- **Search Bins** (bin from search query): saved searches like "Scene = 24" or "Good =
  true" that auto-update.

## 5. Find fast
Filter bin content (search field), use the **Project panel List view** sorted by
columns, and **Freeform view** for visual organisation of selects.

## Gotchas
- Importing individual MXF files from inside a card - lost spanning and metadata.
- Media left on removable drives that get unplugged.
- No folder template; every editor builds differently.
- Image sequences imported as stills.

## Verify
- [ ] Ingest preset matches the workflow (copy/transcode/proxies).
- [ ] Camera media imported via Media Browser from full card structures.
- [ ] Bin template and label scheme applied.
- [ ] Metadata columns populated; search bins created.
