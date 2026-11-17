---
id: computing-software.devops-ci-cd.tekton.tekton-task-larger-results-sidecar-logs
name: tekton-task-larger-results-sidecar-logs
category: computing-software
field: devops-ci-cd
product: tekton
tags: [task, results, sidecar-logs, termination-message]
level: sme
status: docs-checked
description: "Enable larger Tekton Task results through sidecar logs instead of termination messages, with the 4 KB default and max-result-size caveats."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/tasks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Beta, guarded by the `results-from` feature flag set to `"sidecar-logs"`. Instead of storing results in the pod termination message, the TaskRun controller injects a sidecar that mounts the step results volume and logs each new result to stdout; the controller reads the sidecar logs.

- The controller needs access to Kubernetes pod logs (see the additional-configs doc for the required permission).
- Default limit is 4 KB per result, but the number of results is no longer constrained by the termination message size. A result above the limit puts the TaskRun in a failed state with `Result exceeded the maximum allowed limit.`
- Set the `max-result-size` feature flag (bytes) to allow a larger per-result limit.
- Caution from the docs: the larger the size, the more likely the CRD reaches the maximum object size enforced by etcd, which degrades user experience.

The docs' rule of thumb: if a result needs to be larger than a kilobyte, use a Workspace to store and pass it between Tasks in a Pipeline.

## Checked

Checked 2026-11-08 against docs/tasks.md in tektoncd/pipeline (main), reading the larger-results-using-sidecar-logs subsection and the results rule-of-thumb in full (partial read of a long file). Confirmed the results-from flag, sidecar behaviour, 4 KB default, failure message, max-result-size and etcd caution. Replaced an unsourced recommendation with the docs' own kilobyte rule of thumb.

Method: documentation only; no commands were run.
