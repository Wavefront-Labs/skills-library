---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-datafrom-extract-all-keys
name: external-secrets-operator-datafrom-extract-all-keys
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [datafrom, extract, json, environment-variables]
level: intro
status: docs-checked
description: "Use dataFrom.extract to import every key of a JSON provider secret into a Kubernetes Secret and consume it with env or envFrom."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/all-keys-one-secret.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`spec.data` maps individual keys; `spec.dataFrom` handles a variable set. With a provider secret that holds a JSON object, extract all key-value pairs without listing them:

```yaml
spec:
  target:
    name: secret-to-be-created
  dataFrom:
  - extract:
      key: all-keys-example-secret
```

The example uses GCP Secret Manager but works the same with AWS and Azure. The ExternalSecret name (`example`) differs from the Kubernetes Secret it creates (`secret-to-be-created`), and a `namespace` may be set in the metadata.

Consume a few keys with `env[].valueFrom.secretKeyRef`, or all at once:

```yaml
envFrom:
- secretRef:
    name: secret-to-be-created
```

Check a value with `kubectl get secret secret-to-be-created -n <namespace> -o jsonpath='{.data.username}' | base64 -d`.

## Checked

2026-11-03. Claims were read against guides/all-keys-one-secret.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
