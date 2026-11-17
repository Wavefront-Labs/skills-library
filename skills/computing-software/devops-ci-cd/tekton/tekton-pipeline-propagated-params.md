---
id: computing-software.devops-ci-cd.tekton.tekton-pipeline-propagated-params
name: tekton-pipeline-propagated-params
category: computing-software
field: devops-ci-cd
product: tekton
tags: [pipeline, params, propagation, embedded-spec]
level: practitioner
status: docs-checked
description: "Use propagated parameters so inline taskSpec steps can read Pipeline params without redeclaring them, and know where explicit passing is still required."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/pipelines.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Parameters declared on a `Pipeline` can be used directly inside inlined `taskSpec` blocks and their inlined `steps`, without redeclaring them on each task.

```yaml
spec:
  params:
    - name: HELLO
      default: "Hello World!"
    - name: BYE
      default: "Bye World!"
  tasks:
    - name: echo-hello
      taskSpec:
        steps:
          - name: echo
            image: ubuntu
            script: |
              #!/usr/bin/env bash
              echo "$(params.HELLO)"
    - name: echo-bye
      taskSpec:
        steps:
          - name: echo-action
            ref:
              name: step-action-echo
            params:
              - name: msg
                value: "$(params.BYE)"
```

Where a resource is referenced by name rather than embedded (a `taskRef` PipelineTask or a StepAction used through `ref`), propagation does not apply: the parameters must be passed explicitly, as `msg` is above. The same rules apply as for embedded PipelineRuns; see the PipelineRun docs on propagated parameters.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): pipelines.md. Removed: nothing.

Method: documentation only; no commands were run.
