---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-katib-sdk-tune-quickstart
name: kubeflow-katib-sdk-tune-quickstart
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [tune, katibclient, getting-started, objective-function, search-space]
level: intro
status: docs-checked
description: "Run a first Katib hyperparameter tuning Experiment with KatibClient.tune: objective function, search space, trial count, and reading the best trial."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/getting-started.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Katib sdk tune quickstart

The getting-started example maximizes `F(a,b) = 4a - b^2` using the Python SDK.

```python
def objective(parameters):
    import time
    time.sleep(5)
    result = 4 * int(parameters["a"]) - float(parameters["b"]) ** 2
    print(f"result={result}")   # Katib parses name=value

import kubeflow.katib as katib
parameters = {
    "a": katib.search.int(min=10, max=20),
    "b": katib.search.double(min=0.1, max=0.2),
}
katib_client = katib.KatibClient(namespace="kubeflow")
katib_client.tune(
    name="tune-experiment",
    objective=objective,
    parameters=parameters,
    objective_metric_name="result",
    max_trial_count=12,
    resources_per_trial={"cpu": "2"},
)
katib_client.wait_for_experiment_condition(name="tune-experiment")
print(katib_client.get_optimal_hyperparameters("tune-experiment"))
```

Key points:
- Metrics are read from stdout in the form `<metric-name>=<metric-value>`.
- The result JSON contains `best_trial_name`, `parameter_assignments` and an `observation` with `latest`, `max` and `min` per metric.
- Inside Kubeflow Community Distribution, use your profile namespace, for example `kubeflow-user-example-com`. The `kubeflow` namespace is pre-configured with the label `katib.kubeflow.org/metrics-collector-injection: enabled`; the page says to attach it to other namespaces to use the pull-based metrics collector there.
- Completed Trials also appear in the Katib UI.
- With the `tune` API you do not need to package your training code in a container image (the HP tuning guide requires an image only when you do not use `tune`). The example imports `time` inside the objective function.

## Checked

2026-11-08. Confirmed against the Katib Getting Started page: the example code, the stdout metric format, the output fields, the namespace notes and the Katib UI note. Removed an unsupported explanation of why imports sit inside the function.
Method: docs-only read of cited pages, 2026-11-08
