---
id: computing-software.devops-ci-cd.argo-workflows.work-avoidance
name: work-avoidance
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [work-avoidance, marker-files, optional-artifacts, exit-handler, idempotent-steps]
level: practitioner
status: docs-checked
description: "Skip already-completed steps using marker files held on a PVC and optional input artifacts, as a manual alternative to memoization."
sources: ["https://argo-workflows.readthedocs.io/en/latest/work-avoidance/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Work avoidance with marker files
Work avoidance means steps skip work that is already done, making workflows faster and resubmittable. It resembles memoization, but you control how work is skipped; memoization is the built-in feature that skips steps with cached results.

Use it when an expensive step appears in several workflows, or when unreliable tasks need resubmission.

A marker file records completion:

```sh
if [ -e /work/markers/name-of-task ]; then
    echo "work already done"
    exit 0
fi
echo "working very hard"
touch /work/markers/name-of-task
```

Make the name unique to the task, for example including the template name and parameters:

```sh
touch /work/markers/$(date +%Y-%m-%d)-echo-{{inputs.parameters.num}}
```

Markers must survive between workflows, which you do with a PVC and an optional input artifact. The full example (work-avoidance.yaml) has:
- a PVC to hold the markers
- a `load-markers` step restoring markers from artifact storage
- several `echo` tasks that skip work using markers
- a `save-markers` exit handler that saves markers even when no work was needed

## Checked

2026-11-08. Read the Argo Workflows work avoidance page in full (raw markdown) and confirmed marker files, the shell snippet, naming, PVC plus optional input artifact storage, and the example components. Removed: the closing claim about resuming partially successful runs, which the page does not state.

Method: documentation only; no commands were run.
