---
id: computing-software.cloud-infrastructure-engineering.pulumi.helm-release-and-chart
name: helm-release-and-chart
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, helm-release, helm-chart, helm-v3, chart-values]
level: practitioner
status: docs-checked
description: "Install Helm charts from Pulumi using kubernetes.helm.v3.Release (Helm engine) versus Chart (template to resources), with values and atomic."
sources:
  - https://www.pulumi.com/registry/packages/kubernetes/api-docs/helm/v3/release/
  - https://www.pulumi.com/registry/packages/kubernetes/api-docs/helm/v3/chart/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Helm Release vs Chart

```typescript
const rel = new k8s.helm.v3.Release("ingress", {
  chart: "ingress-nginx",
  version: "4.11.3",                       // exact chart version; latest if omitted
  repositoryOpts: { repo: "https://kubernetes.github.io/ingress-nginx" },
  namespace: "ingress", createNamespace: true,
  values: { controller: { replicaCount: 2 } },
  atomic: true, timeout: 600,
}, { provider });

const chart = new k8s.helm.v3.Chart("nginx", {   // renders templates client-side
  chart: "nginx-ingress", version: "1.24.4",
  fetchOpts: { repo: "https://charts.helm.sh/stable" },
  transformations: [(o) => { if (o.kind === "Service") o.spec.type = "ClusterIP"; }],
}, { provider });
```

- **Release**: models a Helm release as if created by the Helm CLI; the implementation embeds Helm as a library, so the full spectrum of Helm features is supported natively.
- **Chart**: a component that renders the chart's templates locally and manages the resulting objects directly with the Pulumi Kubernetes provider. Semantics are equivalent to `helm template` then managing the YAML with Pulumi; values that would be retrieved in-cluster get fake values and no server-side validity testing runs. It supports `transformations` to alter rendered resources.

## Gotchas
- Release `version`: if not specified, the latest chart version is installed, so pin it.
- Release `atomic`: the install process purges the chart on failure, and `skipAwait` is disabled automatically when atomic is used.
- By default the provider waits until all release resources are ready; `skipAwait: true` skips that. `timeout` is seconds to wait for any individual Kubernetes operation.
- Release CRDs are installed if not already present unless `skipCrds` is set.
- Pulumi documents a "Choosing the right Helm resource for your use case" page for the trade-offs.

## Verify
`helm ls -n ingress` lists a Release; for a Chart, list the rendered objects with kubectl.

## Checked

Method: docs-checked 2026-11-09 against the Pulumi Registry Kubernetes helm/v3 Release and Chart pages. Removed unconfirmed claims: in-cluster release secret details, Pulumi diff-preview limits for Release values, and the CRDs-only-at-first-install behaviour.
