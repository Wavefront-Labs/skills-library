---
id: creative-arts.animation.pipeline.storage-tiers-and-project-lifecycle
name: storage-tiers-and-project-lifecycle
category: creative-arts
field: animation
product: pipeline
tags: [storage-tiers, project-lifecycle, hot-warm-cold, tiered-storage, archive, data-management, retention]
level: practitioner
status: draft
description: "Plan storage tiers for an animation project: hot, warm and cold storage, what lives where, lifecycle triggers, capacity forecasting, close-out and retention."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Storage tiers and project lifecycle

An animation production creates a large amount of data (renders, caches, plates, textures). Putting all of it on the fastest storage is expensive; putting it all on slow storage stalls artists. Tiers match data to its use.

## Tiers
| Tier | Typical media | Holds |
|---|---|---|
| Hot | NVMe/SSD, fast shared file system | Active shots, current renders, caches, working scenes |
| Warm | NAS or object storage on disks | Finished shots in the show, recent versions, review media |
| Cold | LTO tape, cold object storage | Completed projects, old versions, source masters |
| Archive | Tape in a vault, offline copies | Final masters and deliverables kept for the long term (`lto-ltfs-archiving.md`) |

## Lifecycle
1. **Active production**: everything for current sequences on hot; completed sequences' intermediates move to warm.
2. **Delivery**: lock the final masters, verify checksums (`checksum-fixity.md`), and copy to archive with a manifest (`archive-manifest.md`).
3. **Close-out**: delete temporary renders, caches and duplicates once the archive is verified; keep what the reuse plan needs (assets, rigs, templates).
4. **Retention**: apply a retention schedule based on contracts (the distributor may require masters for years), and review at fixed dates.

## Planning capacity
- Estimate per minute of final: frames x layers x bytes per frame (EXR sizes are large) x versions retained; multiply by a safety factor. Compare with similar projects.
- Plan growth peaks during lighting and compositing.
- Include **backups** on top (`backup-strategy-3-2-1.md`).

## Rules
- Make deletion a documented step with sign-off, never a clean-up by the person running low on space.
- Put quotas and alerts on shared volumes.
- Keep a map of what is on which tier, in the tracker or a catalogue.

## Verify
- [ ] Hot storage use is below the alert threshold.
- [ ] Archive copies have verified checksums before any deletion.
- [ ] A retention schedule is written.
