---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-katib-trial-template
name: kubeflow-katib-trial-template
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [trial-template, trial-parameters, trialspec, success-condition, primary-pod-labels, configmap-template]
level: practitioner
status: docs-checked
description: "Define a Katib trialTemplate: trialParameters and references, trialSpec versus configMap, success and failure conditions, primaryPodLabels, retain, and using Trial metadata."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/user-guides/trial-template.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Katib trial template

The Trial template lives under `.spec.trialTemplate` and describes the Worker job.

- `trialParameters`: list of `name` (replaced in the template), optional `description`, and `reference` (the parameter name the Suggestion returns, usually equal to the search space names). Every parameter must appear in the template, anywhere except `.metadata.name` and `.metadata.namespace`, using `${trialParameters.<name>}` such as `--lr=${trialParameters.learningRate}`.
- Define the template in exactly one of `trialSpec` (unstructured YAML) or `configMap` (`configMapName`, `configMapNamespace`, `templatePath`; the ConfigMap needs the label `katib.kubeflow.org/component: trial-templates`). The template omits name and namespace.
- `primaryContainerName`: container the metrics collector wraps.
- `primaryPodLabels`: labels of the pods to inject; default `job-role: master` for TFJob, PyTorchJob, MXJob, XGBoostJob; if omitted, all worker pods are wrapped.
- `successCondition` and `failureCondition`: GJSON expressions on the worker status. Job success default: `status.conditions.#(type=="Complete")#|#(status=="True")#`; training operator jobs use `Succeeded`; failure uses `Failed`.
- `retain: true` keeps Trial resources after completion (default false).

The defaults for pod labels and conditions apply only with `trialSpec`; with `configMap` you must set them yourself.

Trial metadata: point a `reference` at `${trialSpec.Name}`, `${trialSpec.Namespace}`, `${trialSpec.Kind}`, `${trialSpec.APIVersion}`, `${trialSpec.Labels[key]}` or `${trialSpec.Annotations[key]}`.

Custom CRDs as Workers: the resource must create pods, allow sidecar injection, and expose succeeded and failed status. Add a ClusterRole rule for the controller (for Tekton: `pipelineruns`, `taskruns`) and list the kind under `trialResources` in `katib-config`, such as `PipelineRun.v1beta1.tekton.dev`, then deploy Katib again and wait for the `katib-controller` Pod.

## Checked

2026-11-08. Confirmed against the Trial template guide: trialParameters rules, trialSpec and configMap sources, retain, primaryPodLabels, success and failure condition defaults (Job uses Complete; Kubeflow training jobs use Succeeded), the metadata references and the CRD steps.
Method: docs-only read of cited pages, 2026-11-08
