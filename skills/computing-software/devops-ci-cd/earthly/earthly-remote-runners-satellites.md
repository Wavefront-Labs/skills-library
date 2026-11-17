---
id: computing-software.devops-ci-cd.earthly.earthly-remote-runners-satellites
name: earthly-remote-runners-satellites
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, satellites, remote-runner, sat-launch, sat-select, sat-unselect, org-select, remote-caching]
level: practitioner
status: docs-checked
description: "Run Earthly builds on a remote runner: launch and select an Earthly Satellite, switch back to local, use --sat per run, and how cache reuse works on remote runners."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/basics/part-7-using-remote-runners.md
  - https://github.com/earthly/earthly/blob/main/docs/caching/caching-via-remote-runners.md
  - https://github.com/earthly/earthly/blob/main/docs/caching/caching.md
  - https://github.com/earthly/earthly/blob/main/docs/cloud/satellites.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Remote runners and Earthly Satellites

Goal: execute builds on a remote machine while logs stream to your terminal.

With a remote runner, build inputs are picked up locally, execution (including `RUN --push` and `SAVE IMAGE --push`) happens remotely, and local outputs are sent back.

Useful when you want to reuse cache between CI runs, share compute and cache with coworkers or CI, need more resources or a native CPU architecture, or have a slow internet connection.

Two kinds exist: Earthly Satellites (managed by Earthly; the page cites a free tier up to 6,000 minutes/month) and a self-hosted remote BuildKit.

## Satellite commands
```bash
earthly org select <my-org>
earthly sat launch my-satellite      # automatically selected once launched
earthly sat select my-satellite      # switch to it later
earthly sat unselect                 # go back to local builds
earthly +my-target                   # builds as usual
earthly --sat my-satellite +my-target   # use one without selecting
```
A larger satellite can be launched with `earthly sat launch --size ...`.

## Secrets
Credentials available locally, including Docker/Podman credentials, are passed automatically to the remote runner when the build needs them.

## Caching
Remote caching works by reusing the same runner across builds; the runner keeps its cache between executions, so there is nothing special to configure and layer caching and cache mounts work as usual. This beats upload/download caching in ephemeral CI, where state is otherwise lost between runs.

## Gotcha
Passing Earthly's cache through traditional CI cache constructs that upload and download is described as too inefficient to be practical; run builds remotely instead. For self-hosting see the remote BuildKit skill.

## Checked

2026-11-07. Read part-7-using-remote-runners.md, caching-via-remote-runners.md and caching.md in full, and the --size line of docs/cloud/satellites.md. Commands, remote execution, credential passing and the cache-sharing statements match. Corrected: added satellites.md to sources because sat launch --size is not on the three original pages.
Method: documentation only; no commands were run.
