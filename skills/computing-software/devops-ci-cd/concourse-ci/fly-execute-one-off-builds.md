---
id: computing-software.devops-ci-cd.concourse-ci.fly-execute-one-off-builds
name: fly-execute-one-off-builds
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [fly, execute, one-off-build, inputs, outputs, inputs-from, image, tag, privileged]
level: practitioner
status: docs-checked
description: "Run a task from your laptop with fly execute: upload inputs, multiple -i inputs, --inputs-from a job, --image, --output downloads, params from env vars, vars flags and --tag."
sources:
  - https://concourse-ci.org/docs/tasks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`fly execute` uploads local files and runs a task config in a container on Concourse, useful for building Linux projects from another OS and avoiding debug commits.

```shell
fly -t example execute --config tests.yml
```

The working directory name becomes the input name; if it differs from the task's input, use `-i name=.`. `fly` captures `SIGINT` and `SIGTERM` and aborts the build. Files your VCS ignores are not sent; use `--include-ignored` to send them. `-p/--privileged` runs as root.

- Multiple inputs: `--input code=. --input stemcells=../stemcells`. Once you give an input, the default is no longer added automatically.
- `--inputs-from main/integration` bases inputs on the latest candidates for that job; explicit `--input` flags override it. Add `--image some-image` to use an input as the task image like a step `image`.
- `--output stemcell=/tmp/stemcell` downloads a declared output.
- Params from the task config come from environment variables: `BAR=hello; fly execute`; unset ones use defaults.
- Vars in the config: `-l vars.yml`, `-v some_string="Hello World!"`, `-y some_bool=true`; remaining vars go to the credential manager.
- `--tag bar` runs on a worker tagged `bar`.

```shell
fly -t example execute --config task.yml --inputs-from main/integration --input foo=./foo
```

## Checked

2026-11-04. Flags and examples confirmed on the Tasks page, Running tasks with fly execute.

Method: documentation only; no commands were run.
