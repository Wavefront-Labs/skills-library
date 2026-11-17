---
id: computing-software.devops-ci-cd.argo-rollouts.experiment-step-in-canary-rollout
name: experiment-step-in-canary-rollout
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [experiment, canary-step, specref, weight, traffic-routing, podtemplatehash, argo-rollouts]
level: sme
status: docs-checked
description: "Run baseline-versus-canary Experiments as a blocking canary step, optionally with weighted traffic or generated Services."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/experiment/
  - https://argo-rollouts.readthedocs.io/en/stable/features/kubectl-plugin/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A canary Rollout can create an Experiment with an `experiment` step. The step blocks the Rollout until the Experiment succeeds, and if it fails or errors the Rollout aborts.

```yaml
steps:
  - experiment:
      duration: 1h
      templates:
        - name: baseline
          specRef: stable
        - name: canary
          specRef: canary
      analyses:
        - name: mann-whitney
          templateName: mann-whitney
          args:
            - name: baseline-hash
              value: "{{templates.baseline.podTemplateHash}}"
            - name: canary-hash
              value: "{{templates.canary.podTemplateHash}}"
```

`specRef: stable` or `canary` copies the PodSpec of that ReplicaSet. The Experiment's pod hashes intentionally differ from the Rollout's stable and canary hashes even with identical specs, so metrics for the experiment pods can be queried separately. Experiment names combine the Rollout name, pod hash, revision and step index.

**Weighted experiment** (since v1.1, SMI, ALB and Istio routers only): add `weight` to templates, e.g. `weight: 5` each, so 5% goes to each experiment pod set and 90% stays on the old stack. A Service is auto-created per template, named after the ReplicaSet, reachable via `{{templates.canary.replicaset.name}}`.

**Service without weight:** set `service: {name: test-service}` on a template to create a Service without traffic routing.

Verify with `kubectl argo rollouts get rollout NAME` which lists the Experiment and its AnalysisRuns.

## Checked

2026-11-08. Confirmed against the Argo Rollouts Experiment page (read in full): the experiment step, specRef, differing pod hashes, weighted experiments since v1.1 for SMI, ALB and Istio, auto-created Services and service without weight. The get rollout tree view is from the kubectl plugin page (read in full).

Removed or corrected: nothing; claims matched.

Method: documentation only; no commands were run.
