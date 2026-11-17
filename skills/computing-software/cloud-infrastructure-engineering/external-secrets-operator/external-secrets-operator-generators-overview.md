---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-generators-overview
name: external-secrets-operator-generators-overview
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [generators, clustergenerator, generatorref, dynamic-secrets]
level: advanced
status: docs-checked
description: "Generate values such as passwords, tokens and keys with ESO generators referenced from dataFrom sourceRef.generatorRef and shared via ClusterGenerator."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/generator.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Generators produce a map of values from a `generator.spec` input and are consumed through `spec.dataFrom` with `sourceRef.generatorRef`:

```yaml
spec:
  refreshInterval: "30m0s"
  target:
    name: ecr-token
  dataFrom:
  - sourceRef:
      generatorRef:
        apiVersion: generators.external-secrets.io/v1alpha1
        kind: ECRAuthorizationToken
        name: "my-ecr"
```

Generators do not track what they produced: every invocation yields a new set of values, and the same value cannot be shared across ExternalSecrets or `dataFrom` entries. Outputs can be combined with `rewrite` and `template`.

A `ClusterGenerator` is a cluster-scoped definition (`spec.kind` must match the generator kind exactly, with the spec in `spec.generator`, for example `passwordSpec` with `length`, `digits`, `symbols`, `symbolCharacters`, `noUpper`, `allowRepeat`). It only makes the definition findable cluster-wide; resources are still created in the namespace of the referencing ExternalSecret.

Generator kinds include ACR, Cloudsmith, ECR, GCR, GitHub, GitLab deploy token, Quay, Password, SSHKey, STS session token, UUID, Vault dynamic secret, Webhook, Grafana, MFA and Fake.

## Checked

2026-11-03. Claims were read against guides/generator.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
