---
id: computing-software.devops-ci-cd.tekton.tekton-taskrun-debugging-breakpoints
name: tekton-taskrun-debugging-breakpoints
category: computing-software
field: devops-ci-cd
product: tekton
tags: [taskrun, debug, breakpoints, alpha]
level: advanced
status: docs-checked
description: "Halt a failing Tekton step with debug breakpoints, open a shell in the step container and use the debug-continue scripts."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/taskruns.md
  - https://github.com/tektoncd/pipeline/blob/main/docs/debug.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`spec.debug` is an alpha feature: `enable-api-fields` must be `"alpha"`, and only TaskRun supports it.

```yaml
spec:
  debug:
    breakpoints:
      onFailure: "enabled"
      beforeSteps:
        - my-step-name
```

On failure the TaskRun pod stays halted instead of marking the step failed. Without user action it remains subject to the TaskRun timeout. Get a shell with `kubectl exec -it POD -c step-STEPNAME sh`.

Lifecycle scripts live in `/tekton/debug/scripts` (shared between containers):
- `debug-continue`: mark the failed step a success and leave the breakpoint.
- `debug-fail-continue`: mark it a failure and exit the breakpoint.
- `debug-beforestep-continue`: let a `beforeSteps` breakpoint step run.
- `debug-beforestep-fail-continue`: do not run the step and mark it failed.

Internally, steps coordinate with `-wait_file` and `-post_file` flags of the entrypoint binary; on failure the post file gets `.err` appended and later steps are skipped. The debug mode withholds that and waits for a `.breakpointexit` file under `/tekton/run`. Step info is under `/tekton/debug/info/<n>`.

## Checked

Checked 2026-11-08 against docs/taskruns.md (the Debugging a TaskRun section, partial read of a long file) and docs/debug.md (read in full), both in tektoncd/pipeline (main). Confirmed the alpha gate and TaskRun-only support, breakpoint YAML, timeout note, kubectl exec access, the four debug scripts, the wait_file and post_file mechanism with .err, the breakpointexit file and /tekton/debug/info. No changes needed to claims.

Method: documentation only; no commands were run.
