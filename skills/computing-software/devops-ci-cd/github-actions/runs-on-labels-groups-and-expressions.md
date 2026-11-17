---
id: computing-software.devops-ci-cd.github-actions.runs-on-labels-groups-and-expressions
name: runs-on-labels-groups-and-expressions
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, runs-on, runs-on-group, runner-selection, runner-labels, ubuntu-latest, label-array, runner-group, dynamic-runs-on, runs-on-expression, runs-on-matrix, arm64-runners, windows-latest, macos-latest, image-migration, workflow-syntax]
level: practitioner
status: docs-checked
description: "Choose runners with runs-on: single labels, AND-ed label arrays, group plus labels objects, and expressions that pick a runner from inputs or matrix; pin images instead of -latest when it matters."
sources: ["https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idruns-on", "https://docs.github.com/en/actions/reference/runners/github-hosted-runners", "https://github.com/actions/runner-images"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# runs-on: labels, groups and expressions

**Goal:** route every job to the right machine, deterministically.

## 1. Forms
```yaml
runs-on: ubuntu-24.04                       # single label (GitHub-hosted image)
runs-on: [self-hosted, linux, x64, gpu]     # array = ALL labels must match (AND)
runs-on:                                    # object form: runner group + labels
  group: prod-deployers
  labels: [linux, x64]
runs-on: ${{ inputs.runner }}               # expression (workflow_dispatch input, matrix, vars)
runs-on: ${{ matrix.os }}
runs-on: ${{ github.event_name == 'pull_request' && 'ubuntu-latest' || 'self-hosted' }}
```
An array matches only runners that have all the listed labels; to run on several machines use `strategy`
(a matrix). A new self-hosted runner gets the `self-hosted` label by default (the `--no-default-labels`
flag prevents it); list `self-hosted` first in an array. The `self-hosted` label is not supported by
Actions Runner Controller. `runs-on` also accepts a single variable and arrays mixing strings and
expressions; quote expressions inside an array, e.g. `[self-hosted, "${{ inputs.chosen-os }}"]`.

## 2. Groups
Runner groups scope *who* may use a runner pool (org/enterprise → selected repos, selected
workflows). `group:` alone picks any runner in the group; add `labels:` to narrow. On GitHub.com a
runner group can only contain larger runners or self-hosted runners, so groups do not apply to
standard GitHub-hosted images.

## 3. GitHub-hosted labels worth knowing
- The `-latest` labels are the latest stable images GitHub provides and may not be the newest OS release.
  In the current runner table `ubuntu-latest` maps to Ubuntu 24.04 (also `ubuntu-22.04`),
  `windows-latest` to Windows Server 2025 (also `windows-2022`) and `macos-latest` to macOS 26 arm64
  (also `macos-14`, `macos-15`). Pin a version label for anything that depends on preinstalled tools.
- Arm64 Linux: `ubuntu-24.04-arm`, `ubuntu-22.04-arm`, `ubuntu-26.04-arm`; Windows arm64: `windows-11-arm`;
  Intel macOS: `macos-15-intel`, `macos-26-intel`. Re-read the supported-runners table before pinning,
  because it changes.
- `ubuntu-slim` is a single-CPU runner that runs in an unprivileged container with a 15-minute job
  timeout, for lightweight tasks; Docker-in-Docker and mounting file systems are not supported there.
- Larger runners are targeted by the name or group you configure (see the larger runners docs).

## 4. Dynamic selection pattern
```yaml
on:
  workflow_dispatch:
    inputs:
      runner:
        type: choice
        options: [ubuntu-latest, self-hosted]
        default: ubuntu-latest
jobs:
  build:
    runs-on: ${{ inputs.runner || 'ubuntu-latest' }}
```
`inputs.*` is empty on non-dispatch events, hence the `||` fallback.

## 5. Gotchas
- `runs-on` is required.
- Contexts available in `jobs.<id>.runs-on`: github, needs, strategy, matrix, vars, inputs (not env or secrets).

## Verify
- [ ] Every self-hosted job lists OS and architecture labels as well as `self-hosted`.
- [ ] Tool-version-sensitive jobs pin an image version, not `-latest`.
- [ ] Group-scoped jobs run in a repository that is allowed on that group.

## Checked

Date: 2026-10-25. Documentation release: github/docs main, commit of 2026-10-23.
- runs-on forms (string, variable, array, group and labels keys), AND semantics of arrays, self-hosted default label and --no-default-labels, ARC not supporting self-hosted: confirmed in workflow-syntax runs-on reusables.
- Runner groups on GitHub.com contain only larger or self-hosted runners; ubuntu-slim limits; the -latest note and the current label table (ubuntu-latest 24.04, windows-latest 2025, macos-latest 26, macos intel labels, arm labels): confirmed in the github-hosted-runners reference and supported-github-runners reusable.
- Removed unconfirmed claims: automatic OS and architecture labels, queue timeout wording, container and services Linux-only note, registration command, billing statement, the staged-rollout note, and the macos-13 reference (no longer in the table).

Method: documentation only; no commands were run.
