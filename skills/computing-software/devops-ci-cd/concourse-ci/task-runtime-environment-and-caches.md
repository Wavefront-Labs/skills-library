---
id: computing-software.devops-ci-cd.concourse-ci.task-runtime-environment-and-caches
name: task-runtime-environment-and-caches
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [task, caches, outputs, runtime, working-directory, node-modules, environment]
level: advanced
status: docs-checked
description: "Task container at run time and how caches work: fresh container each run, working directory layout, same-path input and output trick, worker-scoped caches."
sources:
  - https://concourse-ci.org/docs/tasks/
  - https://concourse-ci.org/docs/jobs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every task run uses a new container whose base filesystem `/` is the task's image. The command runs in a working directory holding each input; if any input is missing the task does not run and the container is not even created. The directory also contains empty directories for each output, and the task must place artifacts in them to export them. If a build tool lacks an output path option, declare an input and an output with the same path: the directory is populated by the input, and changes propagate downstream as an output.

Task step `params` are set in the environment alongside variables from the image (`ENV` rules in a Dockerfile). The user is whatever the image sets, such as a `USER` rule, or `root`. `privileged` is a step field and deliberately not in the task config, to stop pull requests from escalating privilege by editing task files.

**Caches.** `caches` lists directories shared between runs of the same task:

```yaml
inputs:
- name: project-src
caches:
- path: project-src/node_modules
run:
  path: project-src/ci/build
```

On the first run cache directories are empty and the task populates them. Caches are scoped to the worker, so a build on another worker misses, and the task must work whether or not the cache is warm. They are also scoped to a task name inside a job, so renaming the job, the step or the cache path loses the cache, and one-off builds have no caches. Absolute cache paths are respected. Clear them with `fly clear-task-cache`.

## Checked

Checked 2026-11-09 against the raw docs source of the Tasks page (read in full: Task runtime environment and caches sections) and the Jobs page (`fly clear-task-cache` section, which also supports `--job`, `--step` and `--cache-path`).

Method: docs-checked 2026-11-09 against concourse docs Tasks and Jobs pages (github.com/concourse/docs source); documentation only, no commands were run.
