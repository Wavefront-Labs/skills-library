---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-katib-resume-experiments
name: kubeflow-katib-resume-experiments
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [resume-policy, resume-experiment, longrunning, fromvolume, kubectl-edit]
level: practitioner
status: docs-checked
description: "Modify a running Katib Experiment's trial counts and restart finished Experiments using the Never, LongRunning and FromVolume resume policies."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/user-guides/resume-experiment.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/user-guides/katib-config.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/user-guides/hp-tuning/configure-algorithm.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Katib resume experiments

While an Experiment runs you may change only `parallelTrialCount`, `maxTrialCount` and `maxFailedTrialCount`, for example with `kubectl edit experiment <name> -n <namespace>`. The controller reconciles immediately:
- `parallelTrialCount` changes create or delete Trials to match.
- `maxTrialCount` must exceed the current count of `Succeeded` Trials; remove it to run until the goal or failure limit.
- Removing `maxFailedTrialCount` means the Experiment never reaches `Failed` from failures.

Only an Experiment in `Succeeded` status because it reached `maxTrialCount` is restartable, again by changing those three fields. Check with `kubectl get experiment <name> -n <namespace>`.

Set `.spec.resumePolicy`:

- **Never** (default): after completion the Suggestion Deployment and Service are deleted; no restart.
- **LongRunning**: the Suggestion Deployment and Service keep running until you delete the Experiment, so you can raise the trial counts to restart.
- **FromVolume**: a PVC (and PV) is created next to the Suggestion, named `<suggestion-name>-<suggestion-algorithm>` in the Suggestion namespace (the PV is named `<suggestion-name>-<suggestion-algorithm>-<suggestion-namespace>`). After completion the Deployment and Service are deleted but algorithm state stays on the volume and is restored on restart. Deleting the Experiment removes the Deployment, Service, PVC and PV.

The algorithm page says Experiments should use `resumePolicy: FromVolume` to run the `pbt` algorithm. Volume settings (mount path, PVC and PV specs) are set in the `katib-config` suggestion volume parameters.

## Checked

2026-11-08. Confirmed against the resume guide, the Katib Config page (suggestion volume parameters) and the HP tuning algorithm page (PBT needs FromVolume). Spelled out the PVC and PV naming as the guide gives it.
Method: docs-only read of cited pages, 2026-11-08
