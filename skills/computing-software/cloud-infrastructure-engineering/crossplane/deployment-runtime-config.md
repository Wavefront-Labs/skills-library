---
id: computing-software.cloud-infrastructure-engineering.crossplane.deployment-runtime-config
name: deployment-runtime-config
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [deploymentruntimeconfig, provider, function, runtime, package-runtime]
level: advanced
status: docs-checked
description: "Customize a Provider or Function pod with DeploymentRuntimeConfig and runtimeConfigRef."
sources:
  - https://docs.crossplane.io/latest/packages/providers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `DeploymentRuntimeConfig` (beta, on by default) templates the Deployment, ServiceAccount and Service of packages that have a runtime. Reference it with `spec.runtimeConfigRef.name` on the Provider or Function; the default is `default`, which Crossplane creates but never overwrites, so you can customize it.

```yaml
apiVersion: pkg.crossplane.io/v1beta1
kind: DeploymentRuntimeConfig
metadata:
  name: enable-ess
spec:
  deploymentTemplate:
    spec:
      selector: {}
      template:
        spec:
          containers:
          - name: package-runtime
            args:
            - --enable-external-secret-stores
```

Rules:

- The runtime container must be named `package-runtime`. Any other name becomes a sidecar.
- The schema is the Deployment spec, so pass empty `selector: {}` and `template: {}` when you only change something like `replicas: 2`.
- Defaults if unset: replicas 1, pull policy `IfNotPresent`, run as non-root user and group 2000, no privilege escalation.
- Crossplane sets namespace, owner references, selectors, service account, pull secrets, ports, env and TLS volumes.
- `serviceAccountTemplate.metadata.name` makes the package manager own that account; sharing it across packages causes reconcile loops. To reuse an existing account, set only `deploymentTemplate.spec.template.spec.serviceAccountName`.

## Checked

Checked against the Providers page, Configure a Provider section (runtime configuration, deployment spec rules, metadata templates, service account warning), read in full.

Method: docs-checked 2026-11-09 against the packages/providers page (docs repo raw markdown).
