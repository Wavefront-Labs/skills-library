---
id: computing-software.devops-ci-cd.nx.nx-run-commands-custom-target
name: nx-run-commands-custom-target
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, run-commands, targets, project-json, affected, run-many]
level: intro
status: docs-checked
description: "Wrap any shell command as an Nx target in project.json so it is cacheable, distributable and usable with run-many and affected."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/kb/run-commands-executor.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/project-configuration.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run an arbitrary terminal command (example: `make hello`) through Nx to gain caching, distribution (task distribution on CI) and `affected` support.

1. Command to run, with a `Makefile` in the project root:

```make
hello:
  echo "Hello, world!"
```

2. Add a target to each project's `project.json`; `command` is all that is needed for the `nx:run-commands` executor:

```jsonc
"targets": {
  "make": { "command": "make hello" }
}
```
Argument forwarding and other options are in the run-commands executor reference; see also nx-pass-args-to-commands.

3. Run it with normal Nx syntax:

```shell
nx run my-app:make
nx make my-app
nx run-many -t make          # every project defining the target
nx affected -t make          # only projects affected by the change
```

Caching is opt-in per target: add `"cache": true` plus appropriate `inputs`/`outputs` (see nx-troubleshoot-cache-misses for checking the Cacheable label, and nx-configure-outputs). Dependencies between such targets are declared with `dependsOn` (nx-task-pipeline-dependson).

## Checked

2026-11-07. Confirmed against Running Custom Commands: the make hello Makefile example, a project.json target with command, the nx run, nx <target> <project>, run-many and affected invocations, and the benefits (cacheable, distributable, affected). Caching being opt-in with "cache": true is confirmed on the project configuration reference, added to sources; the Cacheable label check is on the troubleshoot-cache-misses page. Removed: the invented Verify step (expected output).

Method: documentation only; no commands were run.
