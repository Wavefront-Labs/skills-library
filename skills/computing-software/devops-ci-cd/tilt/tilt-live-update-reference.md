---
id: computing-software.devops-ci-cd.tilt.tilt-live-update-reference
name: tilt-live-update-reference
category: computing-software
field: devops-ci-cd
product: tilt
tags: [live-update-reference, tilt, live-update, tiltfile]
level: advanced
status: docs-checked
description: "Specification of Tilt live_update steps: initial_sync, fall_back_on, sync, run with triggers, and restarting a process."
sources:
  - "https://docs.tilt.dev/live_update_reference.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Live Update reference

Goal: update a running container in place instead of rebuilding the image and redeploying. Pass `live_update` to `docker_build()`, `custom_build()` or `k8s_custom_deploy()`.

## Step order

The list must be, in order: 0 or 1 `initial_sync`, 0 or more `fall_back_on`, 0 or more `sync`, 0 or more `run`. Steps are objects and can be assigned to variables, but every created step must be used in some Live Update call or Tilt errors. The initial build on `tilt up` is a full build, and the page says it should not rely on synced files.

On a file change: a match with `fall_back_on` causes a full rebuild and deploy; otherwise a match with a `sync` path copies the files, then runs each `run` step (if it has `triggers`, only when a changed file matches).

## Steps

- `initial_sync()`: no arguments; first in the list. Uploads all files from the `sync` paths when Tilt first sees a running container and whenever it restarts. It never deletes files. Files ignored for the image are skipped: `docker_build` respects `.dockerignore`, `ignore=` and `only=`; `custom_build` respects `ignore=` on its deps.
- `sync(local_path, remote_path)`: the only trigger for a Live Update. Deleting a local file deletes it remotely. Local paths must be inside what Tilt watches (`docker_build` `context`, or `custom_build` `deps`). Changes inside the context but matching no `sync` cause a full build; changes outside both do nothing.
- `fall_back_on(files)`: a path or list of paths, absolute or relative to the Tiltfile.
- `run(cmd, trigger=None)`: runs on the container; currently all commands run from `/`, so use absolute paths. Currently all `run` steps must come after `sync` steps; they run in the order given. A trigger must also be covered by a `sync`.

```python
docker_build('my-img', '.', live_update=[
    sync('./src', '/app'),
    run('/app/setup.sh'),
    run('cd /app/web && yarn install', trigger='./src/web/yarn.lock'),
])
```

## Restarting the process

Use the `restart_process` extension (`docker_build_with_restart` with `entrypoint`). It does not work for Docker Compose (use `restart_container()`), `custom_build`, images without a shell, or CRDs. Workarounds: the rerun-process-wrapper scripts, or `echo /restart.txt | entr -rz /path/to/bin` restarted by `run('date > /restart.txt')`.

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the Live Update Reference in full (step order, LiveUpdateSteps, initial_sync, sync, fall_back_on, run and triggers, restarting the process, workarounds, footnote on the first build). Confirmed step order, the context and deps watch rule, the full-build versus no-op cases, `run` working directory, trigger-must-be-synced rule, the restart_process exceptions and both workarounds. Not opened: the rerun-process-wrapper and restart_process repos. Trimmed or qualified: "always a full build" (page says the initial build is a full build), the ignore rules (page limits `only=` and `.dockerignore` to `docker_build`), and the run working directory and ordering (page says "currently"). 

Method: documentation only; no commands were run.
