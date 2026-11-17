---
id: computing-software.devops-ci-cd.argo-rollouts.analysis-template-arguments
name: analysis-template-arguments
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [analysis, args, valuefrom, fieldref, podtemplatehashvalue, analysistemplate, argo-rollouts]
level: advanced
status: docs-checked
description: "Parameterise AnalysisTemplates with args and resolve them from literals, rollout fields, pod hashes or secrets."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/analysis/
  - https://argo-rollouts.readthedocs.io/en/stable/features/specification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
AnalysisTemplates declare `spec.args`, referenced in metric configuration as `{{ args.<name> }}`. Arguments passed by the Rollout are merged with the template's args when the AnalysisRun is created, and placeholders resolve at that time.

```yaml
# template
spec:
  args:
    - name: service-name
    - name: prometheus-port
      value: 9090
```

In a Rollout, `args` can use `valueFrom`:

```yaml
args:
  - name: stable-hash
    valueFrom:
      podTemplateHashValue: Stable
  - name: latest-hash
    valueFrom:
      podTemplateHashValue: Latest
  - name: region
    valueFrom:
      fieldRef:
        fieldPath: metadata.labels['region']
```

`podTemplateHashValue` supplies the `rollouts-pod-template-hash` of the Stable or Latest ReplicaSet, handy for per-version metric labels. `fieldRef` passes metadata such as labels. Since v1.2, `valueFrom` can also read any field from the Rollout status or its pod template, for example an AWS canary target group name from status or a version label from the pod template.

Args may also come from Kubernetes Secrets with `valueFrom.secretKeyRef` (name, key) for credentials passed to providers such as the web provider.

When several templates are merged, two arguments with the same name but different default values cause an error regardless of the Rollout's value.

Verify by reading the resolved values in `kubectl get analysisrun RUN -o yaml`.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/analysis/, https://argo-rollouts.readthedocs.io/en/stable/features/specification/.

Removed or corrected: nothing; claims matched.

Method: documentation only; no commands were run.
