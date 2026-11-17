---
id: computing-software.devops-ci-cd.tilt.tilt-api-live-update-steps
name: tilt-api-live-update-steps
category: computing-software
field: devops-ci-cd
product: tilt
tags: [api-live-update-steps]
level: advanced
status: docs-checked
description: "Tiltfile Live Update step functions: fall_back_on, initial_sync, sync, run and restart_container, with their ordering rules."
sources:
  - "https://docs.tilt.dev/api.html#api.sync"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Live Update steps

Goal: build the `live_update` step list so file changes reach a running container instead of triggering a full image build. Each function returns a LiveUpdateStep.

## Steps and ordering rules

- `fall_back_on(files)`: changes to the given files cause a full image build instead of a live update. May only go at the beginning of the step list. Files (string or list; relative paths are relative to the Tiltfile) must be a subset of files already watched for the image; otherwise an error is raised if they fall outside DockerBuild.context or CustomBuild.deps.
- `initial_sync()`: performs a full sync of all files matching the live update's `sync` rules when a container first starts (or restarts), without waiting for file-change events. Useful with pre-built images that may lack the latest local source. Must appear at most once, and only at the start of the list (before any `fall_back_on`, `sync`, `run` or `restart_container`).
- `sync(local_path, remote_path)`: changes to `local_path` are synced to `remote_path`. `local_path` is relative to the Tiltfile's directory, and may be a file or a directory (recursively). `remote_path` must be an absolute container path. May not follow any `run` steps.
- `run(cmd, trigger=[], echo_off=False)`: executes `cmd` when updating the container. May not precede any `sync` steps.
  - `cmd`: a string runs with `sh -c`; a list is passed as program name and args.
  - `trigger`: file(s) relative to the Tiltfile; the step runs only when those change. File changes must also match at least one of the Live Update's syncs; changes matching no sync are ignored.
  - `echo_off=True`: the command's output is not echoed to the Tilt UI.
- `restart_container()`: for Docker Compose resources only. The container restarts when live-updated, re-executing its `ENTRYPOINT` in the changed filesystem. May be included once, and only as the last step.

Order summary from the docstrings: initial_sync, then fall_back_on, then sync steps, then run steps, with restart_container last.

For more detail the docstrings point to the Live Update Reference (live_update_reference.html).

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/api.html#api.sync (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
