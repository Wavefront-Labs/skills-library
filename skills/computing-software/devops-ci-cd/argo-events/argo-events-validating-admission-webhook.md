---
id: computing-software.devops-ci-cd.argo-events.argo-events-validating-admission-webhook
name: argo-events-validating-admission-webhook
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, validating-webhook, admission, immutable-fields, install, eventbus]
level: practitioner
status: docs-checked
description: "Install the Argo Events validating admission webhook to reject invalid specs on apply and block immutable-field updates."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/validating-admission-webhook.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events validating admission webhook

Since v1.3 (alpha) Argo Events ships an optional validating admission webhook. Install it by applying the manifest for your version:

```shell
kubectl apply -n argo-events -f https://raw.githubusercontent.com/argoproj/argo-events/{version}/manifests/install-validating-webhook.yaml
```

Benefits:
- Errors appear when you apply a faulty spec instead of in the CRD `status` conditions later. Creating an exotic NATS EventBus without a cluster ID fails immediately with `admission webhook "webhook.argo-events.argoproj.io" denied the request: "spec.nats.exotic.clusterID" is missing`.
- Updates can be validated for immutable fields, which the controller reconciliation cannot do. Changing the auth strategy of a native NATS EventBus is denied with `"spec.nats.native.auth" is immutable, can not be updated`.

The docs mark the webhook as alpha. The webhook name appearing in denial messages is `webhook.argo-events.argoproj.io`.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/validating-admission-webhook.md. Confirmed: v1.3 alpha, install command, both error examples and the webhook name. Removed or changed: the OpenShift finalizers RBAC claim, the claim about the quick start offering the manifest, and other unsupported elaboration. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
