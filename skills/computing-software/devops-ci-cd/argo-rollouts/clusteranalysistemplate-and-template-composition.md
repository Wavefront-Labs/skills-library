---
id: computing-software.devops-ci-cd.argo-rollouts.clusteranalysistemplate-and-template-composition
name: clusteranalysistemplate-and-template-composition
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [clusteranalysistemplate, clusterscope, multiple-templates, template-reference, analysis, argo-rollouts]
level: advanced
status: docs-checked
description: "Share cluster-scoped templates and combine several AnalysisTemplates into one AnalysisRun."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/analysis/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**ClusterAnalysisTemplate.** Available since v0.9.0. It has the same spec as an AnalysisTemplate but is cluster-scoped, so rollouts in any namespace can share it. Reference it with `clusterScope: true`:

```yaml
- analysis:
    templates:
      - templateName: success-rate
        clusterScope: true
```

The resulting AnalysisRun still runs in the namespace of the Rollout.

**Multiple templates.** A Rollout can list several templates. The controller merges them by combining the `metrics` and `args` of all templates into one AnalysisRun:

```yaml
analysis:
  templates:
    - templateName: success-rate
    - templateName: error-rate
  args:
    - name: service-name
      value: guestbook-svc.default.svc.cluster.local
```

**Templates referencing templates.** An AnalysisTemplate or ClusterAnalysisTemplate may itself reference other templates, either alongside its own metrics or alone; the AnalysisRun gets the aggregate. The same restrictions apply.

The controller errors on merge when:

- multiple metrics across templates share the same name, or
- two arguments with the same name have different default values.

If the same template is referenced several times along a reference chain, the controller keeps it once and discards the duplicates.

Verify the merged result: the generated AnalysisRun's `spec.metrics` lists the metrics from every referenced template.

## Checked

2026-11-08. Confirmed against the Argo Rollouts analysis page (read in full): ClusterAnalysisTemplate since v0.9.0 with clusterScope true, AnalysisRun runs in the Rollout namespace, merge of metrics and args, merge error conditions, templates referencing templates and de-duplication.

Removed or corrected: replaced the unsourced kubectl get analysisrun verify command.

Method: documentation only; no commands were run.
