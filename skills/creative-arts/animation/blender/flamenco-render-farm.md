---
id: creative-arts.animation.blender.flamenco-render-farm
name: flamenco-render-farm
category: creative-arts
field: animation
product: blender
tags: [blender, command-line, render-farm, flamenco, distributed-rendering]
level: practitioner
status: docs-checked
description: "Set up Flamenco for Blender: Manager and Workers, shared storage, setup assistant, variables for mixed platforms, task types and custom job types."
sources:
  - https://flamenco.blender.org/usage/quickstart/
  - https://flamenco.blender.org/usage/variables/
  - https://flamenco.blender.org/usage/job-types/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# flamenco-render-farm

Goal: a small studio render farm from ordinary machines, using Blender's own farm manager.

## Parts

- **Flamenco Manager**: the central software; one machine runs `flamenco-manager` (it can be one of the render machines or a dedicated one).
- **Flamenco Worker**: runs on each computer that does the work; you will probably want Blender installed there too.
- **Blender add-on**: downloaded from the Manager's web interface (link in the top-right corner of the browser page) and installed in Blender; it provides the Flamenco panel in Output Properties.
- **File sharing**: a local network with file sharing already set up so all computers reach the same files.

## Setup steps (quickstart)

1. Download Flamenco.
2. Create a directory on some storage, such as a NAS, available at the same path on each computer.
3. Install Blender on each rendering computer, in the same place everywhere.
4. Run `flamenco-manager` on the machine that will manage the farm. It starts a browser with the *Flamenco Setup Assistant*.
5. Step through the assistant, pointing it to the storage and to Blender, and confirm at the final step.
6. Download and install the Blender add-on, then give it the address of the Flamenco Manager (shown in your browser; the Manager logs also show URLs to try) and click the checkmark to check the connection.
7. Save your .blend file in the shared storage, then render it from the Flamenco panel in Output Properties.

## Variables (mixed platforms)

- Variables are configured in `flamenco-manager.yaml`. Each has a name (for example `blender`) and values per platform (`windows`, `linux`, `darwin`, or others you use) and optionally audience (`workers`, `users`, `all`, the default).
- When a Worker gets a task containing `{blender}`, it is replaced with that worker's platform value.
- Two-way variables tell Flamenco that a path on one platform is the same location as a path on another, for example a Linux mount and a Windows drive letter, so mixed Windows/Linux/macOS farms work.
- Default variables are `blender` and `blenderArgs`; custom job types can define their own.

## Job types and task types

- Job types are JavaScript *job compiler scripts*. Each defines a `JOB_TYPE` (label and settings, shown in the Blender add-on) and a `compileJob(job)` function that creates tasks.
- Default scripts are built into the Manager executable. Add custom scripts in a directory named `scripts` next to the `flamenco-manager` executable (for example `scripts/my_job_type.js`); a script with the same name as a built-in one overrides it.
- Task types: `blender`, `ffmpeg`, `file-management`, `misc`. The task type decides which worker may execute the task, so a weak machine can take file management and FFmpeg while big machines take Blender tasks. By default workers run all of these; see the worker configuration page.
- A job setting can have an `eval` key, a Python expression with access to names such as `jobname`, `settings`, `bpy`, `C`, `Path`, `abspath()` and `last_n_dir_parts()`.

## Gotchas

- Keep the .blend and output on the shared storage; paths that are not reachable from workers fail.
- Install Blender in the same place on every machine (the quickstart asks for this) or map it with a `blender` variable per platform.

## Verify

Submit a short test job. All tasks complete on several workers, and frames appear in the shared output folder.

## Checked

2026-11-09. Confirmed against the Flamenco project website sources (Quickstart, Variables, Job Types pages, read as markdown from the Flamenco repository on projects.blender.org). Removed unconfirmed claims: the Manager web UI port, automatic worker discovery, Shaman, worker tags, chunk-size advice, the "Simple Blender Render" job type name, the Windows `<FARM_DRIVE>` example, and add-on and Blender version advice.
Method: documentation only; no commands were run.
