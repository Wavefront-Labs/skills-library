---
id: creative-arts.animation.pipeline.opencue-job-specs
name: opencue-job-specs
category: creative-arts
field: animation
product: pipeline
tags: [opencue, render-farm, job-spec, cuebot, rqd, layers, dependencies, render-management]
level: advanced
status: draft
description: "Submit and structure OpenCue render jobs: Cuebot and RQD roles, job spec layers, frame ranges and chunking, cores and memory, dependencies and monitoring."
sources:
  - https://www.opencue.io/docs/concepts/opencue-overview/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OpenCue job specs

OpenCue is an open-source render manager (an Academy Software Foundation project) for large render farms. Check https://www.opencue.io/ for current docs; command names and fields can change between releases.

## Architecture
- **Cuebot**: the central server that holds jobs, schedules frames and talks to a database.
- **RQD**: the agent on every render host; it launches frame commands and reports back.
- **CueGUI** (Cuetopia and CueCommander): monitoring and admin. **CueSubmit**: a GUI for sending jobs. **PyCue** and **PyOutline**: Python APIs for programmatic submission. The OpenCue overview page (checked 2026-10-18) also lists a Rust implementation of RQD (same function as the Python RQD) and OpenCueWeb, a browser interface with CueGUI's core functions.

## Job structure
- A job has a **show** and **shot** and belongs to a user; it contains one or more **layers**.
- A **layer** is a command run per frame (or per chunk of frames) over a frame range. Typical layers: render, then composite, then encode.
- Layer settings that matter: command line, frame range, **chunk size** (frames per task), **cores** and **memory** per task, services/tags used to select hosts, and **dependencies**.
- Dependencies: a layer can depend on another layer (the encode waits for the render) or on specific frames; this gives pipelines without manual babysitting.

## Spec files and API
Jobs can be described in an XML job spec or created with PyOutline. The XML has a job element containing layers, each with command, range, chunk, cores, memory, services and depends elements. Take the exact schema from the DTD in the OpenCue documentation for your release rather than copying examples from old posts.

## Good practice
1. **Test one frame** locally with the exact command line before submitting the range.
2. Use **environment setup** that matches the artist (a launcher or environment manager, `rez-package-environments.md`).
3. Set **memory** from a real test render to avoid out-of-memory kills, and set cores to match the renderer's threading.
4. Make output **paths absolute and cross-platform** (`cross-platform-path-mapping.md`).
5. Use **retries** limited to a small number, so a broken scene fails fast.
6. Put dependent work (encode, QC) in the same job as dependent layers (`post-job-scripts-and-dependent-encodes.md`).

## Verify
- [ ] A single-frame test produces the expected file on a farm host.
- [ ] Dependent layers start only after their inputs finish.
- [ ] Logs for failed frames are readable in CueGUI.
