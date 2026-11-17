---
id: computing-software.systems-network-administration.immich.tags
name: tags
category: computing-software
field: systems-network-administration
product: immich
tags: [tags, hierarchical, keywords, xmp, taglist]
level: intro
status: docs-checked
description: "Enable and use hierarchical tags in Immich, import existing XMP TagsList and IPTC Keywords by rerunning metadata extraction, and write changes back to sidecars."
sources:
  - https://docs.immich.app/features/tags
  - https://docs.immich.app/features/xmp-sidecars
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: organise assets with hierarchical tags and import tags you already have.

Immich supports hierarchical tags. It can read existing tags from the XMP `TagsList` field and the IPTC `Keywords` field. Any tag change made in Immich is written back to the asset's sidecar `.xmp` file. To import existing tags for assets already in the library, re-run the metadata extraction jobs for all assets.

Enable: Account Settings, Features, Tags.

Create and apply:

1. Open a photo or video's info panel.
2. Click `+ Add` at the bottom.
3. In the tag prompt, pick an existing tag or type a new one to create it.

View: use the Tags view in the side navigation bar, or click a tag in the info panel.

Sidecar details from the XMP page:

- Immich writes tags to `digiKam:TagsList`.
- It reads tags in priority order: `digiKam:TagsList`, `lr:HierarchicalSubject`, then `IPTC:Keywords`.
- A Sidecar Write job is queued automatically after tags are updated.

If your external library is mounted read-only, metadata edits such as tags silently fail (the XMP page warns about this); see the XMP sidecars skill.

## Checked

2026-11-09. Confirmed against the Tags page (hierarchical tags, import by rerunning metadata extraction, enable path, + Add, Tags view) and the XMP Sidecars page (digiKam:TagsList write, read priority, automatic Sidecar Write job, read-only mount warning). Removed: duplicate-merge behaviour, Advanced Search filter and database query claims, not on the cited pages.
Method: documentation only; no commands were run.
