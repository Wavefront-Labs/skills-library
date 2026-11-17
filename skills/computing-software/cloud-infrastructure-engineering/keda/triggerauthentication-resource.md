---
id: computing-software.cloud-infrastructure-engineering.keda.triggerauthentication-resource
name: triggerauthentication-resource
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [triggerauthentication, authenticationref, secrettargetref, podidentity, credentials-reuse]
level: practitioner
status: docs-checked
description: "Define a TriggerAuthentication, map secrets and env vars onto scaler parameters, and reference it from a trigger with authenticationRef."
sources:
  - https://keda.sh/docs/2.17/concepts/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `TriggerAuthentication` (apiVersion `keda.sh/v1alpha1`) keeps authentication parameters separate from the ScaledObject and the workload containers. It enables pod identity, reuse across ScaledObjects, and lets another team own the credentials. It must live in the same namespace as the ScaledObject that uses it.

Its `spec` can combine several sources, all merged into the scaler's authentication data:
- `secretTargetRef`: list of `parameter`, `name` (Secret), `key`, all required.
- `env`: `parameter`, `name`, optional `containerName` (default is the ScaledObject's `envSourceContainerName`).
- `boundServiceAccountToken`, `hashiCorpVault`, `azureKeyVault`, `awsSecretManager`, `gcpSecretManager`.
- `podIdentity` with `provider`, default `none`.

`parameter` is the name the scale trigger defines, such as `connectionString`. Example:

```yaml
secretTargetRef:
  - parameter: connectionString
    name: my-keda-secret-entity
    key: azure-storage-connectionstring
```

Reference it from the ScaledObject trigger:

```yaml
triggers:
- type: {scaler-type}
  metadata:
    param1: {some-value}
  authenticationRef:
    name: {trigger-authentication-name}
```

Parameters supplied by the TriggerAuthentication need not be repeated in the trigger `metadata`. Mix and match providers to cover all required parameters.

## Checked

2026-11-03. Confirmed on the 2.17 Authentication page: TriggerAuthentication fields, namespace rule, secretTargetRef, env, merge behaviour.

Method: documentation only; no commands were run.
