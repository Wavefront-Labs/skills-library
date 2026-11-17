---
id: computing-software.cloud-infrastructure-engineering.kubernetes.webhook-cabundle-injection-cert-manager
name: webhook-cabundle-injection-cert-manager
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, admission-control, cabundle-injection, cert-manager, cainjector, admission-webhooks]
level: practitioner
status: docs-checked
description: "Serve admission webhooks and conversion webhooks with cert-manager certificates and let cainjector fill caBundle automatically, including rotation."
sources: ["https://cert-manager.io/docs/concepts/ca-injector/", "https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Webhook TLS with cert-manager caBundle injection

The apiserver calls webhooks over TLS and trusts only the `caBundle` in the webhook
configuration. Hand-copied bundles break on rotation; cainjector keeps them in sync.

## Certificates
```yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata: {name: selfsigned, namespace: policy}
spec: {selfSigned: {}}
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata: {name: webhook-cert, namespace: policy}
spec:
  secretName: webhook-tls
  dnsNames: [policy-webhook.policy.svc, policy-webhook.policy.svc.cluster.local]
  issuerRef: {name: selfsigned, kind: Issuer}
```
The `selfSigned` issuer is the setup used in the cert-manager CA injector examples; the injected
CA data comes from the Secret created for the `Certificate`.

## Inject
```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: policy-webhook
  annotations:
    cert-manager.io/inject-ca-from: policy/webhook-cert
webhooks:
- name: validate.policy.acme.io
  clientConfig:
    service: {name: policy-webhook, namespace: policy, path: /validate, port: 443}
  # caBundle left empty: cainjector fills it
  admissionReviewVersions: [v1]
  sideEffects: None
```
cainjector's injectable resources are ValidatingWebhookConfiguration, MutatingWebhookConfiguration,
CustomResourceDefinition (conversion webhooks) and APIService. A resource must carry one of
`cert-manager.io/inject-ca-from` (value `<namespace>/<certificate-name>`),
`cert-manager.io/inject-ca-from-secret` (inject from a Secret) or
`cert-manager.io/inject-apiserver-ca` (inject the API server's own CA). If the source is a Secret,
that Secret must also carry the annotation `cert-manager.io/allow-direct-injection: "true"`.

## Webhook server
Mount `webhook-tls` and reload certificates on change; controller-runtime's webhook server
creates a certificate watcher (`certwatcher`) for the `tls.crt`/`tls.key` files.

## Gotchas
- cainjector writes `caBundle` after the configuration is created, so any tool that compares
  live objects to Git will see that field as drift; exclude it in that tool.
- Until the CA data is injected, the API server has no CA to verify the webhook certificate; with
  `failurePolicy: Fail`, calls then fail (see the admission webhook reference for failure policy).

## Verify
Compare the `caBundle` in the webhook configuration with the `ca.crt` in the `webhook-tls` Secret
(the cert-manager example does this with `kubectl get ... -o yaml | grep caBundle` and `grep ca.crt`):
they should be identical, and after a short time the API server uses the new value.

## Checked
Checked 2026-10-24 against the cert-manager website source for "CA Injector" (injectable resource
types, the three annotations, `allow-direct-injection` for Secrets, example with `selfSigned` issuer,
comparison of `caBundle` with `ca.crt`), the Kubernetes admission-controller reference
(`clientConfig.service`, `failurePolicy`, `sideEffects`) and controller-runtime's webhook server source
(`certwatcher`). Removed: the Argo CD field name and the exact x509 error string, which no checked
documentation covers.
Method: documentation only; no commands were run.
