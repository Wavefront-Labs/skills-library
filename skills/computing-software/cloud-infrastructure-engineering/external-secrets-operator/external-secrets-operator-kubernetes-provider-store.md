---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-kubernetes-provider-store
name: external-secrets-operator-kubernetes-provider-store
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [kubernetes-provider, secretstore, remote-cluster, cabundle]
level: practitioner
status: docs-checked
description: "Read Secrets from another Kubernetes namespace or cluster with the ESO Kubernetes provider, its CA options and authentication choices."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/provider/kubernetes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A SecretStore points at one namespace (`remoteNamespace`) in a local or remote cluster. The store reconciler checks read access with `SelfSubjectRulesReview`, falling back to `SelfSubjectAccessReview`. `property` selects a key; empty means all pairs as JSON.

```yaml
spec:
  provider:
    kubernetes:
      remoteNamespace: default
      server:
        url: "https://myapiserver.tld"
        caProvider:
          type: ConfigMap
          name: kube-root-ca.crt
          key: ca.crt
```

`url` defaults to `kubernetes.default`. Without `caBundle` or `caProvider`, system CA roots are used, which only covers well-known CAs; cluster-internal APIs need an explicit CA. Each namespace has a `kube-root-ca.crt` ConfigMap for the local API server.

Authentication: client certificates, a bearer token or a service account. Exactly one method is allowed, and you cannot use the service account mounted in the ESO pod. This lets teams without permission to create a ClusterExternalSecret share a Secret from a dedicated namespace via a token for a service account in that namespace.

## Checked

2026-11-03. Claims were read against provider/kubernetes.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
