---
id: computing-software.systems-network-administration.immich.job-processing-order
name: job-processing-order
category: computing-software
field: systems-network-administration
product: immich
tags: [jobs, pipeline, nightly-tasks, thumbnails, smart-search]
level: practitioner
status: docs-checked
description: "Order in which Immich runs jobs for a new upload, where to see job status, and how nightly tasks are scheduled and configured."
sources:
  - https://docs.immich.app/administration/jobs-workers
  - https://docs.immich.app/administration/system-settings
  - https://raw.githubusercontent.com/immich-app/immich/main/docs/docs/administration/jobs-workers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: predict and troubleshoot what Immich does after an asset is uploaded.

Order of jobs for a new file:

1. Metadata extraction.
2. Storage template migration (only if the storage template is enabled).
3. Thumbnail generation: large, small, blurred and person thumbnails.
4. After thumbnails, in parallel: Smart Search, Face Detection, OCR and Video Transcoding.
5. Smart Search is followed by Duplicate Detection; Face Detection is followed by Facial Recognition.

Later jobs follow earlier ones in this chain. View job status under Administration, Jobs.

Scheduled jobs, such as memories generation, run every night at midnight by default. Change the time or disable a job under System Settings, Nightly Tasks Settings.

Some jobs have their own settings sections: External Library scanning and the Database Dump are configured separately in System Settings.

Concurrency per job type is set in System Settings, Job Settings. Do not raise thumbnail concurrency above the CPU cores you have; the docs warn this hurts API responsiveness without speeding up generation. Facial Recognition concurrency cannot be changed because the DBSCAN implementation is not parallel.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading administration/jobs-workers (Jobs section; the job-order diagram is a mermaid block in the page source on GitHub, read there) and administration/system-settings (Job Settings, Facial Recognition Concurrency).
Removed: the claim that a stuck early stage blocks later ones, and the advice to run the Missing variant, neither of which these pages state.
Method: documentation only; no commands were run.
