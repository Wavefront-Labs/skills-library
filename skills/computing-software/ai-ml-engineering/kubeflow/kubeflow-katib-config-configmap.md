---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-katib-config-configmap
name: kubeflow-katib-config-configmap
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [katib-config, katibconfig, cert-generator, suggestions-config, runtime-config]
level: advanced
status: docs-checked
description: "Katib Config reference: the katib-config ConfigMap with init (certGenerator, controller) and runtime (metricsCollectors, suggestions, earlyStoppings) parameters."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/user-guides/katib-config.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Katib config configmap

`katib-config` is a ConfigMap in the `KATIB_CORE_NAMESPACE` namespace (kind `KatibConfig`, apiVersion `config.kubeflow.org/v1beta1`). Edit with `kubectl edit configMap katib-config -n kubeflow`.

**init** (initialization settings for the control plane; modify them before the control plane is deployed):
- `certGenerator`: `enable` (default false), `webhookServiceName` (`katib-controller`), `webhookSecretName` (`katib-webhook-cert`); setting either name forces the generator on.
- `controller`: `trialResources` (default `[Job.v1.batch]`, format Kind.version.group), `metricsAddr` (8080), `healthzAddr` (18080), `webhookPort` (8443), `enableLeaderElection` (false), `leaderElectionID` (3fbc96e9.katib.kubeflow.org), `injectSecurityContext` (false), `experimentSuggestionName` (default).

**runtime** (read when an Experiment is created):
- `metricsCollectors`: required `kind` and `image`; optional `imagePullPolicy` (IfNotPresent), `resources`, `waitAllProcesses`. Default sidecar resources: requests 50m CPU, 10Mi memory, 500Mi ephemeral storage; limits 500m CPU, 100Mi memory, 5Gi ephemeral storage. Set negative values (the page uses -1) in requests and limits to remove a resource, for example ephemeral-storage to use the Google Kubernetes Engine cluster autoscaler.
- `suggestions`: required `algorithmName` and `image`. Images map to algorithms: suggestion-hyperopt (random, tpe), suggestion-skopt (bayesianoptimization), suggestion-goptuna (cmaes, random, tpe, sobol), suggestion-optuna (multivariate-tpe, tpe, cmaes, random, grid), suggestion-hyperband, suggestion-pbt, suggestion-enas, suggestion-darts. Optional container fields, `serviceAccountName`, and for `FromVolume`: `volumeMountPath` (default `/opt/katib/data`), `persistentVolumeClaimSpec` (default RWO 1Gi), `persistentVolumeSpec` (reclaim policy always Delete), `persistentVolumeLabels`.
- `earlyStoppings`: `algorithmName` (for example medianstop), `image`, optional `imagePullPolicy` (IfNotPresent) and `resources`.

## Checked

2026-11-08. Confirmed against the Katib Config page: namespace and name, init and runtime parameters, every default listed, the suggestion image to algorithm table and the volume parameters. Corrected the leaderElectionID and experimentSuggestionName defaults and the resource-removal wording.
Method: docs-only read of cited pages, 2026-11-08
