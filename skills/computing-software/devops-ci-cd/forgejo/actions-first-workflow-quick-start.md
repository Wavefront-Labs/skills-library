---
id: computing-software.devops-ci-cd.forgejo.actions-first-workflow-quick-start
name: actions-first-workflow-quick-start
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [actions-quick-start, forgejo-workflows, runs-on, actions-checkout]
level: intro
status: docs-checked
description: "Enable Actions on a repository, confirm a runner exists, and push a first .forgejo/workflows file."
sources:
  - https://forgejo.org/docs/latest/user/actions/quick-start/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Before writing a workflow, check two things in the repository settings. First, under Units > Overview the Actions checkbox must be ticked; if it is not visible, the instance administrator has disabled Forgejo Actions. Second, under Actions > Runners at least one runner must be listed. If none is, follow the Forgejo Runner installation guide first.

Then create `.forgejo/workflows/demo.yaml`:

```
on: [push]
jobs:
  test:
    runs-on: docker
    steps:
      - run: echo All good!
```

The workflow triggers on a push event and holds one job, `test`, which runs on a runner carrying the label `docker`. Push it to the main branch and open the repository's Actions tab, where the workflow appears on the left and the run result on the right.

If the run does not start and you see a warning that no matching runner is online, you most likely forgot to change `runs-on` to a label your runner actually has.

To get your code into the job, add `- uses: actions/checkout@v7` followed by `- run: ls -la`. The checkout action takes no parameters when you only need the current repository. Commit, push, and the new steps show in the latest run.

## Checked

2026-11-04. Confirmed against the Forgejo Actions quick start guide: the Units > Overview and Actions > Runners checks, the demo.yaml sample, the no-matching-runner warning and the actions/checkout@v7 steps. Nothing removed.

Method: documentation only; no commands were run.
