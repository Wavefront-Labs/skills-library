---
id: computing-software.cloud-infrastructure-engineering.cert-manager.ca-injector
name: ca-injector
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [cainjector, ca-injector, inject-ca-from, cabundle, allow-direct-injection, webhook-configuration]
level: advanced
status: docs-checked
description: "Use cainjector annotations to populate caBundle on webhook configurations, CRDs and APIServices from a Certificate, a Secret or the API server CA."
sources:
  - https://cert-manager.io/docs/concepts/ca-injector/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
cainjector copies a CA into `caBundle` of resources that carry one of three annotations:
- `cert-manager.io/inject-ca-from: <namespace>/<name>`: a cert-manager `Certificate`; copies `ca.crt` from its Secret.
- `cert-manager.io/inject-ca-from-secret: <namespace>/<name>`: a Secret's `ca.crt`. The Secret must also carry `cert-manager.io/allow-direct-injection: "true"`.
- `cert-manager.io/inject-apiserver-ca: "true"`: the CA the Kubernetes API server uses (the one cainjector uses for its own API connection).

Injectable kinds: `ValidatingWebhookConfiguration`, `MutatingWebhookConfiguration`, `CustomResourceDefinition` (conversion webhooks) and `APIService` (validates the extension API server's serving certificate).

Requirements and behaviour:
- Every target needs one of the annotations.
- Secret-based injection works without cert-manager CRDs and before the cert-manager webhook is configured; cert-manager bootstraps its own webhook that way (the webhook generates a self-signed certificate into a Secret at startup).
- With `inject-apiserver-ca`, the webhook serving certificate must be signed by the cluster CA, which needs access to the cluster CA key and manual rotation of the webhook certificate.
- Propagation is not instant; the API server picks up the new `caBundle` after a short time.

The page documents no specific error messages. Omitting an annotation, or `allow-direct-injection` on a source Secret, are the only documented misconfigurations. The examples are partial and do not deploy webhook servers.

## Checked

2026-11-03. Confirmed on the cert-manager CA Injector page (concepts/ca-injector): the four injectable kinds, three annotations and sources, allow-direct-injection requirement, Secret-based bootstrap of cert-manager's own webhook, API server CA caveats, short propagation delay. Nothing removed.
Method: documentation only; no commands were run.
