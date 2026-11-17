---
id: creative-arts.animation.pipeline.post-job-scripts-and-dependent-encodes
name: post-job-scripts-and-dependent-encodes
category: creative-arts
field: animation
product: pipeline
tags: [post-job-script, dependent-encode, render-farm, deadline, opencue, job-dependencies, automation]
level: advanced
status: draft
description: "Chain farm render jobs to automatic checks and encodes: dependent jobs and layers, post-job scripts, frame-count verification, exit codes, idempotent outputs."
sources:
  - https://docs.thinkboxsoftware.com/
  - https://www.opencue.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Post-job scripts and dependent encodes

After frames finish rendering, the next steps (check frames, encode a review movie, publish) should happen without anyone watching. Farm managers give two mechanisms.

## Mechanisms
- **Dependent jobs or layers**: in OpenCue a layer can depend on another layer of the job (`opencue-job-specs.md`). In Thinkbox Deadline, a job can depend on other jobs (and on specific frames), and does not start until the dependency finishes.
- **Post-job scripts**: Deadline lets you attach a script to run when a job completes (alongside pre-job and per-task scripts in its job options; check the Deadline docs for your version). OpenCue achieves the same with a final dependent layer that runs a script.

## Pattern for an encode
1. Render layer writes frames to a frame-numbered path.
2. Check step verifies **the frame count and no zero-byte files** (`missing-frame-detection.md`) before doing anything else, and fails loudly if frames are missing.
3. Encode step runs FFmpeg on the image sequence (`image-sequence-encode.md`) to a review file in a separate folder.
4. Optional publish step registers the movie in the production tracker (`production-tracking.md`).

## Rules for reliable scripts
- Return a **non-zero exit code** on failure so the farm marks the task as failed.
- Make the step **idempotent**: re-running overwrites the same output name, rather than creating duplicates.
- Write to a temporary name and rename on success, so reviewers never open half-written files.
- Log the command, frame range and tool versions to the job log.
- Use full paths and the farm's environment, not your workstation's.
- Keep secrets out of scripts.

## Gotchas
- A dependency on a job that was re-queued can release the encode early or never; test the failure path.
- Encodes run on the farm may compete with renders for licences and hosts; give them a separate pool or low priority.

## Verify
- [ ] A forced missing frame stops the encode and flags the job.
- [ ] Re-running produces the same output file name.
- [ ] Review movie appears only when complete.
