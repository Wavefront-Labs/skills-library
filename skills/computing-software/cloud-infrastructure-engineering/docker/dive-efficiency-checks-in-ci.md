---
id: computing-software.cloud-infrastructure-engineering.docker.dive-efficiency-checks-in-ci
name: dive-efficiency-checks-in-ci
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dive, dive-ci, dive-efficiency, image-size, layer-inspection, ci]
level: practitioner
description: "Use dive to find wasted bytes per layer and gate CI on efficiency and wasted-space thresholds with CI=true and a .dive-ci rules file."
sources: ["https://github.com/wagoodman/dive", "https://docs.docker.com/reference/cli/docker/image/save/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# dive efficiency scoring and CI mode

## Interactive analysis
```sh
dive app:1                         # local image
dive --source docker-archive app.tar
dive build -t app:1 .              # build then analyse
```
Sources: `docker` (default), `docker-archive` (a tar from disk) and `podman` (Linux only). The left
pane shows layers; the right pane shows the file tree for the selected layer combined with all
previous layers. In the file tree `Ctrl+A`, `Ctrl+R`, `Ctrl+M` and `Ctrl+U` show or hide added,
removed, modified and unmodified files. The efficiency metric is described by the project as
experimental: a percentage score plus total wasted space.

What "wasted" means (per the README): files duplicated across layers, moved across layers, or
not fully removed. Layers are additive, so those bytes still ship.

Typical finds:
- `apt-get update` lists in one layer, `rm -rf /var/lib/apt/lists` in the next.
- `COPY . .` then `RUN chown -R app .` duplicates the whole tree (use `COPY --chown`).
- Build tool caches (`~/.npm`, `~/.cache/pip`, `/root/.m2`) left in a layer.

## CI mode
With `CI=true` in the environment dive skips the UI and returns pass or fail through its exit code:
```sh
CI=true dive app:1
```
Thresholds come from a `.dive-ci` file at the repo root (three metrics are supported):
```yaml
rules:
  lowestEfficiency: 0.95
  highestWastedBytes: 20MB
  highestUserWastedPercent: 0.10
```
- `lowestEfficiency`: ratio 0-1; fails if efficiency is measured below it.
- `highestWastedBytes`: expressed in B, KB, MB, GB; fails at or above it.
- `highestUserWastedPercent`: ratio 0-1; fails if the threshold is met or crossed. The base image
  layer is NOT included in the total image size.
- Override the config path with `--ci-config`.

Running dive from its container needs the Docker socket:
```sh
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock \
  docker.io/wagoodman/dive:latest app:1
```

## Gotchas
- dive needs the image in a supported engine, or an archive: `docker save -o app.tar app:1`
  then `dive --source docker-archive app.tar`.
- Efficiency measures waste, not size, so pair it with your own absolute size budget.
- "User wasted percent" excludes the base image layer, which is the part you control.

## Verify
After fixing, rerun with the same thresholds: exit 0 and the wasted-space list no longer
shows the offending paths.

## Checked
Checked 2026-10-28 against the dive README (CI integration section) and Docker Docs (`docker image
save`, Dockerfile reference for `COPY --chown`): sources list, CI=true behaviour, the three `.dive-ci`
rules and their units, `--ci-config`, key bindings, the wasted-space definition and the user-wasted
base-layer exclusion. Removed because the README does not state them: `--lowestEfficiency`-style
command-line flags, a `disabled` rule value, the "2 GB scores 100%" example, the `.Size` inspect
template and the containerd or `--load` remark. Rule values shown are examples, not defaults.
Method: documentation only; no commands were run.
