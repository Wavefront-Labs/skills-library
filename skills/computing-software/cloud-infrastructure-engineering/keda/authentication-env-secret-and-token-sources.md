---
id: computing-software.cloud-infrastructure-engineering.keda.authentication-env-secret-and-token-sources
name: authentication-env-secret-and-token-sources
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [env, secrettargetref, boundserviceaccounttoken, serviceaccountname, parameter-mapping]
level: practitioner
status: docs-checked
description: "Pull trigger authentication parameters from container environment variables, Kubernetes Secrets or bound service account tokens in a TriggerAuthentication."
sources:
  - https://keda.sh/docs/2.17/concepts/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Authentication parameters can be pulled from many sources, and the full list of providers is in the authentication-providers section of the documentation.
Authentication parameters can come from many sources and are merged into one data set for the scaler. Three built-in Kubernetes-native sources:

Environment variables:
```yaml
env:
  - parameter: region
    name: my-env-var
    containerName: my-container
```
`parameter` is defined by the scale trigger; `name` is the variable; `containerName` is optional and defaults to the ScaledObject's `scaleTargetRef.envSourceContainerName`. The container is looked up in the workload referenced by `scaleTargetRef.name` unless stated otherwise.

Secrets:
```yaml
secretTargetRef:
  - parameter: connectionString
    name: my-keda-secret-entity
    key: azure-storage-connectionstring
```
Pull in one or more entries by Secret `name` and `key`. The Secret is read from the namespace of the workload, except for `ClusterTriggerAuthentication`, which reads from the KEDA namespace.

Bound service account tokens:
```yaml
boundServiceAccountToken:
  - parameter: connectionString
    serviceAccountName: my-service-account
```
The token of the named service account is passed as the parameter. Both fields are required, and the service account is expected in the same namespace as the workload.

## Checked

2026-11-03. Confirmed on the 2.17 Authentication page: env, secretTargetRef, boundServiceAccountToken fields, defaults and namespace assumptions, KEDA_CLUSTER_OBJECT_NAMESPACE.

Method: documentation only; no commands were run.
