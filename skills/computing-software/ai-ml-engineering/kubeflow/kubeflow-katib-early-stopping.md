---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-katib-early-stopping
name: kubeflow-katib-early-stopping
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [early-stopping, medianstop, median-stopping-rule, earlystopped, min-trials-required]
level: practitioner
status: docs-checked
description: "Add early stopping to a Katib Experiment with spec.earlyStopping and the medianstop algorithm, including the log timestamp requirement and its settings."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/user-guides/early-stopping.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/user-guides/katib-config.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Katib early stopping

Early stopping ends Trials whose target metric stops improving, saving compute and limiting overfitting. You do not change the training image; only the Experiment YAML.

Configure:

```yaml
spec:
  earlyStopping:
    algorithmName: medianstop
    algorithmSettings:
      - name: min_trials_required
        value: "3"
```

How it works: the Suggestion produces Trials, the early stopping algorithm generates stopping rules for them, and a Trial that satisfies all rules is stopped with status `EarlyStopped`. Katib then asks the Suggestion for new Trials.

Constraints:
- It works only with the `StdOut` or `File` metrics collectors, because it reads the same metric stream.
- The training container must print logs with timestamps so the sequence of reported metrics is known (the page points to its PyTorch example for how to add a date format to the logs).
- A Suggestion with early stopping needs permission to update Trial status. The Katib Config page says that if you do not set a ServiceAccount in `katib-config`, the controller creates the required RBAC; a custom ServiceAccount name cannot equal `<experiment-name>-<experiment-algorithm>` and it needs permission to update the Trial status.

Median Stopping Rule (`medianstop`): stops a Trial at step S if its best objective so far is worse than the median of the running averages of completed Trials up to S. Settings: `min_trials_required` (default 3, successful Trials needed to compute the median) and `start_step` (default 4, number of reported intermediate results before stopping the Trial). `medianstop` is the only algorithm the page lists.

## Checked

2026-11-08. Confirmed against the early stopping guide and the Katib Config page (ServiceAccount rule). Reworded the example reference and the ServiceAccount rule to what the pages state.
Method: docs-only read of cited pages, 2026-11-08
