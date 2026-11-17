---
id: computing-software.cloud-infrastructure-engineering.kubernetes.tilt-live-update-and-inner-loop-development
name: tilt-live-update-and-inner-loop-development
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, tilt, tiltfile, live-update, inner-loop, tilt-up, docker-build, sync-steps, run-steps, trigger, local-development, dev-environment, microservices-dev, dev-loop, starlark]
level: practitioner
status: docs-checked
description: "Run the Kubernetes inner loop with Tilt: Tiltfile resources, tilt up, and live_update in-place container updates with sync and run steps, trigger paths and step ordering."
sources: ["https://docs.tilt.dev/", "https://docs.tilt.dev/tutorial/5-live-update.html", "https://docs.tilt.dev/api.html", "https://docs.tilt.dev/controlloop.html", "https://github.com/tilt-dev/tilt-extensions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tilt: inner-loop live update for Kubernetes

**Goal:** collapse the dev feedback loop from *rebuild image -> push -> re-tag manifest -> apply ->
wait for roll-out* into an in-place container update, driven by one command per repo.

Tilt automates "all the steps from a code change to a new process: watching files, building
container images, and bringing your environment up-to-date" - conceptually `docker build && kubectl
apply` or `docker-compose up`, but continuous, across a whole microservice repo. `tilt up` starts
the complete dev environment; every save afterwards triggers the smallest update that suffices.

The Tiltfile is the configuration, written in Starlark (a Python dialect) - so it supports
functions, loops and composition, which is how multi-service repos stay declarative without
duplication. Community functionality comes from the `tilt-dev/tilt-extensions` repo.

```bash
tilt up      # complete dev environment
tilt down    # tear it down
```

## live_update: the mechanism that matters
Without it, every code change pays the full pipeline cost - image rebuild, registry push, manifest
tag update, apply, roll-out - which the tutorial says is slow even with Docker layer caching. `live_update`
instead patches the **running container in place**, and pairs with frameworks that natively hot
reload (Webpack) as well as compiled languages, where Tilt restarts the process with the updated
code and still saves the image build and deployment.

```python
docker_build(
    'avatar-api',
    context='.',
    dockerfile='./deploy/api.dockerfile',
    only=['./api/'],
    live_update=[
        sync('./api/', '/app/api/'),
        run(
            'pip install -r /app/requirements.txt',
            trigger=['./api/requirements.txt'],
        )
    ]
)
```

### `sync(local, container)`
Copies changed files into the container. First argument: a path **relative to the Tiltfile** that
Tilt watches recursively; second: the **absolute path inside the container** they land at. Any
changed file under the watched path is copied - this is the cheap default for interpreted code.

Constraint worth memorising: synced files *must* fall inside paths Tilt is already watching for the
image configuration - here `sync('./api/', ...)` is legal only because of `only=['./api/']`.

### `run(cmd, trigger=[...])`
Runs a command **inside the container**, for non-code files that need processing (dependency
installs, generated assets). It executes only when a changed file matches a `trigger` path -
without a trigger it would run on every file change, which is rarely what you want.

### Step ordering
`live_update` steps run **in order**. When `requirements.txt` changes it is first *synced* into the
container, and only then does the `run()` step fire, because the change now matches its trigger -
so `sync` before `run` is the correct arrangement, and reversing them is a real bug.

## What to check before adopting
- Other `live_update` steps from the API reference: `fall_back_on(files)` makes a change to the
  given files trigger a full image build instead of a live update (it may only appear at the start
  of the step list, and the files must be among those already watched for the image);
  `restart_container()` is for Docker Compose resources only (the `restart_process` extension is
  its replacement); `ignore` patterns and `.tiltignore` stop files triggering updates.
- Local vs. Kubernetes resources: services that do not belong in the cluster can run as Tilt local
  resources alongside the deployed ones.
- Cluster choice is deliberate - Tilt's docs include a "Choosing a Local Dev Cluster" guide, and
  the existing `kind-and-minikube-local-and-ci-clusters` skill covers the cluster side.

## Failure modes
- **`run()` executes on every save** - no `trigger` path given.
- **Sync fails or copies nothing** - the synced path is outside the image's watched paths
  (`only=`), violating the constraint above.
- **Steps run in the wrong order** - `run` listed before the `sync` that delivers its inputs.
- **Full rebuilds you did not expect** - a changed file listed in `fall_back_on` always triggers a
  full image build; check that list and the `only` list.
- **Works for one service, unusable for twenty** - Tiltfile duplication; compose with Starlark
  functions instead of copy-pasting `docker_build` blocks.

## Verify
- [ ] `tilt up` brings every service in the repo up from one command.
- [ ] A source-only edit updates the running container without an image rebuild (check the Tilt UI
      shows a live update, not a build).
- [ ] A dependency-file edit triggers sync *then* install, in that order.
- [ ] `tilt down` leaves nothing running.
- [ ] A change to a `fall_back_on` file causes a full image build.

## Checked

Checked 2026-11-09 against the Tilt tutorial page 5 (Live Update), the Tiltfile API reference (live_update steps sync, run, fall_back_on, restart_container, ignore, run trigger semantics, Starlark), the control loop page (resources, local resources) and the docs home page. Removed the `tilt ci` comment and the claim that `fall_back_on` matches output lines (it matches changed files). The API reference also states that a `run` step may not precede any `sync` step.

Method: docs-checked 2026-11-09 against the pages listed above; no commands were run.
