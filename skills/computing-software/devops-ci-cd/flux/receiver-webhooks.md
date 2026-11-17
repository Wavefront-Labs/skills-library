---
id: computing-software.devops-ci-cd.flux.receiver-webhooks
name: receiver-webhooks
category: computing-software
field: devops-ci-cd
product: flux
tags: [receiver, webhook, notification-controller, ingress, hmac]
level: sme
status: docs-checked
description: "Trigger reconciliation from GitHub, GitLab, registries and generic webhooks using Receivers and an exposed webhook-receiver service."
sources:
  - https://fluxcd.io/flux/components/notification/receivers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Webhooks make pull-based delivery as responsive as push. The notification-controller exposes them through its `webhook-receiver` Kubernetes Service. To reach it from outside the cluster, put an Ingress in front of that Service.

Receiver types: `generic`, `generic-hmac`, `generic-oidc`, `github` (also Gitea), `gitlab`, `bitbucket` (Bitbucket Server), `harbor`, `dockerhub`, `quay`, `nexus`, `acr`, `gcr`, `cdevents`. Only github, gitlab, bitbucket and cdevents support filtering by `.spec.events`; if it is empty, any valid payload is handled.

```yaml
apiVersion: notification.toolkit.fluxcd.io/v1
kind: Receiver
metadata:
  name: generic-receiver
  namespace: default
spec:
  type: generic
  secretRef:
    name: webhook-token
  resources:
    - apiVersion: source.toolkit.fluxcd.io/v1
      kind: GitRepository
      name: webapp
      namespace: default
```

`.spec.resources` is required: each entry has `kind`, `name` (or `*` with `matchLabels`) and optional `apiVersion` and `namespace` (the Receiver's namespace when omitted). The generated path is in `.status.webhookPath`, formatted `/hook/sha256sum(token+name+namespace)`, where token is the `token` key of the Secret. For generic-oidc there is no Secret, so the path is `/hook/sha256sum(name+namespace)`. Register that path with the sender.

Security: the generic type performs no validation of the incoming request, so prefer the HMAC or OIDC variants.

## Checked

2026-11-08: read the notification-controller Receivers spec (docs/spec/v1/receivers.md in the fluxcd/notification-controller repo, the source of the fluxcd.io page) in full. Confirmed: the webhook-receiver Service behind an Ingress, the type list and which types support events, the generic no-validation note, resources fields, and the webhook path formula including the generic-oidc variant. Removed: port 9292, Service port 80, the LoadBalancer and HTTPRoute options, Ingress rate limits, and the network policy and cert-manager advice, none of which are in that spec.

Method: documentation only; no commands were run.
