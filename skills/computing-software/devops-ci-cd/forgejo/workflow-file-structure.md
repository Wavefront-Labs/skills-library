---
id: computing-software.devops-ci-cd.forgejo.workflow-file-structure
name: workflow-file-structure
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [workflow-file, on-key, jobs, steps]
level: intro
status: docs-checked
description: "Read the structure of a Forgejo workflow: on, jobs, runs-on, steps, uses and run."
sources:
  - https://forgejo.org/docs/latest/user/actions/basic-concepts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Workflows are `.yaml` files stored in the `.forgejo/workflows` directory of a repository. The documented minimal example is:

```
on: [push]
jobs:
  print-content:
    runs-on: docker
    steps:
      - name: checkout code
        uses: actions/checkout@v7
      - name: list directory contents
        run: ls -la
```

- `on` lists the events that trigger the workflow. You can narrow it to specific branches or use other events such as issues or pull requests.
- `jobs` holds the units of work handed to runners. By default jobs run independently of one another.
- `runs-on` is the label of the runner. This job only runs on runners labelled `docker`.
- `steps` run in order. If a step fails, the job cleans up and no later step runs.
- `uses` runs an action, a reusable procedure; checkout copies the repository into the working directory.
- `run` executes a command in the job's shell, and its output appears in the job logs.

The workflow reference page gives the complete syntax definition.

## Checked

Date: 2026-11-07
Confirmed against the "Forgejo Actions | Basic concepts" page, read in full (Basic syntax section and its example): the `.forgejo/workflows` location of `.yaml` files, the minimal example verbatim, and the explanations of `on`, `jobs`, `runs-on`, `steps`, `uses` and `run`, including independent jobs by default and stopping after a failed step.
Corrected: nothing needed; every claim matched the page text. The skill is thin (it restates one page section).
Method: documentation only; no commands were run.
