---
id: creative-arts.animation.scripting.batch-render-scripting-and-farm-submission
name: batch-render-scripting-and-farm-submission
category: creative-arts
field: animation
product: scripting
tags: [render-farm, deadline, qube, tractor, batch-render, job-submission, python, dependencies, retries, chunking, cli, headless, queue, frame-ranges, priority]
level: practitioner
status: draft
description: "Scripting batch render jobs and submitting them to a render farm (Deadline/Qube/Tractor or a local queue) from the DCC or CLI, with dependencies and retries."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Batch render scripting and farm submission

**What it is:** turning "render this episode" into jobs a farm (Deadline,
Qube, Tractor, or a hand-rolled local queue) actually executes correctly —
frame chunking, dependency ordering, retries, and priority — scripted so no
one hand-submits per shot. Distinct from `scripting-basics` (building the
*scene* to render) and from `render-preflight` (catching defects *before*
spending render time) — this skill is specifically about getting a finished
scene onto a farm's job queue reliably and cheaply.

Verified against Deadline's Python API (`Deadline.Scripting`, the
`deadlinecommand`/`DeadlineCon` CLI submitter pattern most houses use);
Qube and Tractor follow the same job/task/dependency shape with different
APIs (`pyqube`, Tractor's `tractor.api.author`) — noted where the concept
differs, not verified against those two directly (unconfirmed specifics).

## 1. A job is metadata + a plugin command, not the render itself
Farm submission is two small text blobs (or API calls), not a render:
```python
# Deadline-style: a job info dict + a plugin info dict
job_info = {
    "Name": "EP03_sh012_beauty", "Frames": "1-120", "ChunkSize": 10,
    "Pool": "render", "Priority": 50, "OutputDirectory0": "<FARM_SHARE>/out/EP03/sh012",
}
plugin_info = {"SceneFile": "<FARM_SHARE>/scenes/EP03_sh012.blend", "Version": "4.2"}
```
`ChunkSize` = frames per task: 1 maximes parallelism but multiplies
per-frame startup overhead (scene load, license checkout); 10-20 is a
common sweet spot for a few-second-per-frame shot, 1 for a heavy multi-minute
frame. Tune per shot, don't use one global default.

## 2. Submit from a script, never the farm's GUI, for anything >1 job
```python
import subprocess
def submit(job_info_path, plugin_info_path):
    r = subprocess.run(["deadlinecommand", job_info_path, plugin_info_path],
                        capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"submit failed: {r.stderr}")
    return r.stdout.strip()   # job id
```
Write the info dicts to temp `.job`/`.plugin` ini-style files (Deadline's CLI
wants files, not stdin) and submit per-shot in a loop driven by the same
shotlist JSON the render pipeline already uses — one submission script run
over N shots, not N manual GUI submissions. This mirrors
`scripting-basics`'s "the shotlist IS the data" principle applied to the
farm instead of the renderer.

## 3. Dependencies: a comp job must not start before its render job finishes
```python
comp_job_info["JobDependencies"] = render_job_id   # Deadline: comma-sep job ids
```
- Chain render -> comp -> transcode as dependent jobs so the farm enforces
  order; don't poll-and-wait in your submission script (ties up a
  submission machine/license for the whole render).
- A dependency on a job that FAILS leaves the dependent job stuck pending
  forever in Deadline by default — set the dependent job's failure behaviour
  (`OnJobFailure`) deliberately, or build a watchdog that cancels downstream
  jobs when an upstream job hits its failure threshold, or dead shots pile up
  silently in the queue for days.

## 4. Retries and failure budgets — a farm WILL have flaky tasks
```python
job_info["MachineLimit"] = 0           # 0 = unlimited machines
job_info["FailureDetection"] = 3        # auto-requeue a task up to N times
job_info["OverrideTaskExtraInfoNames"] = False
```
- Set a per-job `FailureDetection`/retry count for transient failures
  (network blip reading a texture off a NAS, license checkout race at farm
  rush hour) — don't require a human to requeue. But cap it: an infinite
  retry on a *genuinely* broken frame (bad data, not transient) burns farm
  hours silently. 2-3 retries, then let it fail loud.
- Log enough in the render script itself (print the frame number, the asset
  paths resolved) that a failed task's farm log tells you WHY without
  needing to reproduce interactively — farm machines are usually headless
  and you can't attach a debugger.

## 5. Output collision is the #1 silent farm bug
Two shots (or two retries of the same task) writing to the same output
path/frame number overwrite each other with no error — the farm reports
success on both. Always derive the output path from the job's own
shot/version id (`####.exr`), never a shared
`out/` folder with filenames that collide across jobs.

## 6. HARD-WON GOTCHAS
- **Chunk boundaries can split a sequence so a comp tool "missing frame"
  check never fires on an incomplete middle chunk** if that one task retries
  forever quietly — always reconcile actual rendered frame COUNT against the
  expected frame range after the farm reports a job complete, don't trust
  the farm's own "complete" status alone.
- **Relative paths resolve against the farm worker's working directory, not
  your submission machine's** — same absolute-path discipline as
  `scripting-basics`'s render-path gotcha, but it bites harder here because
  the worker is a different machine entirely. Always submit absolute,
  network-visible paths (`<FARM_SHARE>/...` / a UNC path, not a local
  `<USER_HOME>/...`).
- **Pool/priority starvation**: a low-priority job behind a backlog of
  higher-priority jobs can sit for hours with no error — if a shot "isn't
  rendering," check queue position before assuming a submission bug.
- *(Qube/Tractor specifics for dependency and retry fields are unconfirmed
  against this skill's author's direct experience — the job/task/dependency
  shape above is the right mental model, but check each tool's own field
  names before porting the snippets literally.)*

## Verify
- [ ] A batch of N shots submits from one script run with zero GUI clicks.
- [ ] A deliberately failed task (bad path) retries up to the configured
      limit, then fails loud with a log that names the actual cause.
- [ ] A comp job submitted dependent on a render job does not start until
      the render job reports complete.
- [ ] After a "complete" job, rendered frame count on disk matches the
      requested frame range exactly — no silently-missing chunk.
- [ ] Output paths are unique per shot+version; no two jobs can write the
      same file.

See also: `scripting-basics` (building the scene these jobs render),
`render-preflight` (validate before you ever submit), `shot-renderer` (the
thing the farm task actually executes per frame).
