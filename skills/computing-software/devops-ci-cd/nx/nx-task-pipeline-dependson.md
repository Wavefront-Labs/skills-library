---
id: computing-software.devops-ci-cd.nx.nx-task-pipeline-dependson
name: nx-task-pipeline-dependson
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, task-pipeline, dependson, targetdefaults, continuous, task-graph]
level: practitioner
status: docs-checked
description: "Define Nx task dependencies with dependsOn globally in targetDefaults or per project, mark servers continuous, and inspect the task graph."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/kb/defining-task-pipeline.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/run-tasks.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make one task run its prerequisites first (the task pipeline that becomes the task graph).

Global, in `nx.json`: `^build` means "build of my project dependencies first":

```json
{ "targetDefaults": { "build": { "dependsOn": ["^build"] } } }
```

Per project, in `project.json` (or the `nx.targets` key of `package.json`), a plain name means a target of the same project:

```json
{ "targets": {
  "prebuild": { "command": "echo Prebuild" },
  "build": { "command": "echo Build", "dependsOn": ["prebuild"] }
} }
```

Continuous tasks: a dependency that never exits (a dev server) would block its dependent forever. Mark it `continuous` so Nx does not wait for exit and runs it alongside its dependents:

```json
{ "targets": { "serve": { "continuous": true } } }
```
Typical use: an `e2e` task depending on a continuous `serve`.

Visualise: `npx nx graph`, choose "Tasks" in the top-left dropdown, pick the target (build, test, ...) and show all tasks or one project. Nx Console offers "Focus task in Nx Graph" via right-click on a project in VS Code or IntelliJ.

## Checked

2026-11-07. Confirmed against Defining a Task Pipeline: dependsOn in targetDefaults with ^build, per-project dependsOn in project.json and the nx key of package.json, the prebuild example, continuous dependencies (do not wait for exit, run alongside dependents), the e2e and serve example, and nx graph with the Tasks dropdown and Nx Console Focus task in Nx Graph. The meaning of the caret is confirmed on Run Tasks, added to sources. Removed: the claim that continuous servers' inputs are hashed into the dependent task (not on the page), and the invented Verify step.

Method: documentation only; no commands were run.
