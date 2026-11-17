---
id: creative-arts.animation.pipeline.outsourcing-service-studios
name: outsourcing-service-studios
category: creative-arts
field: animation
product: pipeline
tags: [outsourcing, production-phases, service-studio, vendor-management, packages, retakes, turnaround, bid-review, delivery-specs]
level: advanced
status: draft
description: "Outsource animation work to service studios: what to send in a package, specs and approvals, schedules with review checkpoints, retake handling and vendor QC."
sources:
  - https://www.ttp.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Outsourcing to service studios

**Goal:** work produced by an external studio (layout, animation, ink and paint, compositing, entire
episodes) comes back on-model, on schedule and in pipeline-ready form, with predictable retakes.

## Package contents (per episode or batch)

- Locked animatic/story reel with timings, and the exposure sheets or shot list with frame counts.
- Model sheets, colour models/palettes, prop and background designs, style guide with dos and don'ts.
- Rigs/puppets or asset files in the vendor's software version; scene templates.
- Audio (dialogue tracks) and lip-sync breakdowns.
- Technical spec: resolution, frame rate, naming, file formats, colour pipeline, delivery structure.
- Notes from previous episodes' retakes (recurring issues).

## Contract and schedule

- Scope by shot count/footage and complexity tiers; price per second/minute or per shot.
- Milestones with review checkpoints: layout/blocking review before full animation, then final.
- Turnaround for retakes defined (e.g. 5 working days), and how many retake rounds are included.

## Reviews and retakes

- Review in a shared tool with frame-accurate notes (drawovers). Classify notes: **vendor error** (off-model,
  missed note: vendor fixes free) vs **change of direction** (client change: may be billable).
- Track retakes per shot and vendor; recurring issues go into the next package's notes.

## Technical QC on receipt

Automated checks (naming, frame counts, formats, missing frames:
`creative-arts.animation.encode-delivery.missing-frame-detection`) before creative review, so creative time
isn't spent on broken deliveries.

## Gotchas

- Time zones: design the review loop so notes go out at the vendor's start of day.
- Content security obligations flow to vendors (`creative-arts.animation.pipeline.forensic-watermarking`
  and access control): include them in the contract.
- Software version mismatches corrupt scene files; pin versions in the spec.

## Verify

Per batch: shots delivered vs scheduled, first-pass approval rate, retake count by category; packages updated
with recurring notes before the next batch goes out.
