---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-disable-cluster-scoped-features
name: external-secrets-operator-disable-cluster-scoped-features
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [helm, clustersecretstore, clusterexternalsecret, crds]
level: practitioner
status: docs-checked
description: "Install ESO without ClusterSecretStore, ClusterExternalSecret and ClusterPushSecret by pairing the crds and process Helm values."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/disable-cluster-features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Helm chart installs the cluster-scoped CRDs and processes them by default. To disable them, set both the `crds.*` value (CRD installation) and the matching `process*` value (controller reconciliation), since the pair is linked:

```bash
helm install external-secrets external-secrets/external-secrets \
  --set crds.createClusterExternalSecret=false \
  --set crds.createClusterSecretStore=false \
  --set crds.createClusterPushSecret=false \
  --set processClusterExternalSecret=false \
  --set processClusterStore=false \
  --set processClusterPushSecret=false
```

You can disable only one or two of the features by setting just the relevant pairs.

## Checked

2026-11-03. Claims were read against guides/disable-cluster-features.md in the external-secrets docs source. Removed: a multi-tenant attack-surface remark not on this page.

Method: documentation only; no commands were run.
