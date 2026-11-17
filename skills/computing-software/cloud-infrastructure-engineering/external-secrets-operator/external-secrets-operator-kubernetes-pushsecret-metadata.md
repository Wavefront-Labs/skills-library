---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-kubernetes-pushsecret-metadata
name: external-secrets-operator-kubernetes-pushsecret-metadata
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [kubernetes-provider, pushsecret, metadata, mergepolicy]
level: advanced
status: docs-checked
description: "Replicate Secrets between namespaces or clusters with PushSecret and control label and annotation merging."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/provider/kubernetes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
PushSecret to the Kubernetes provider needs the source `selector`, the `secretKey` to replicate, and `remoteRef.property` naming the key in the remote Secret (plus `remoteKey` for its name). By default ESO pushes labels and annotations and merges them with existing metadata on the target.

To decouple them, set `spec.template.metadata`, and `template.data` can render values such as `mysql://{{ .hostname }}:3306/{{ .database }}`.

Fine control per entry uses `data[].metadata` with `kind: PushSecretMetadata` and `apiVersion: kubernetes.external-secrets.io/v1alpha1`:

```yaml
metadata:
  apiVersion: kubernetes.external-secrets.io/v1alpha1
  kind: PushSecretMetadata
  spec:
    sourceMergePolicy: Merge   # or Replace
    targetMergePolicy: Merge   # or Replace / Ignore
    labels:
      color: red
    annotations:
      yes: please
```

## Checked

2026-11-03. Claims were read against provider/kubernetes.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
