---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-admission-webhook
name: prometheus-operator-admission-webhook
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [admission-webhook, validating-webhook, conversion-webhook, cert-manager-certificate, alertmanagerconfig-conversion]
level: advanced
status: docs-checked
description: "Deploy the Prometheus Operator admission webhook to validate and mutate PrometheusRule and convert AlertmanagerConfig versions."
sources:
  - https://prometheus-operator.dev/docs/platform/webhook/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A separate admission webhook service can:
- **validate** that `PrometheusRule` and `AlertmanagerConfig` objects are semantically valid;
- **mutate** `PrometheusRule` objects so all annotations are strings;
- **convert** `AlertmanagerConfig` between `v1alpha1` and `v1beta1`.

## Prerequisites
Admission controllers enabled on the cluster, and HTTPS: the API server talks to webhooks over TLS, so you need a certificate and key in a Secret. The guide assumes a Secret `admission-webhook-certs` (keys `tls.crt`, `tls.key`) in the webhook namespace. The recommended approach is cert-manager, which also injects the CA bundle into the webhook configuration. Example: a cert-manager `Certificate` with `dnsNames: [prometheus-operator-admission-webhook.default.svc]`, `secretName: admission-webhook-certs` and a SelfSigned `ClusterIssuer`.

## Deployment
Apply the ServiceAccount, Deployment and Service manifests shown in the guide (they live in the repo `example/admission-webhook` directory). The Service exposes port 443 to the container port named `https` (8443). The Deployment runs 2 replicas with required pod anti-affinity on `kubernetes.io/hostname`, and starts the container with `--web.enable-tls=true --web.cert-file=/etc/tls/private/tls.crt --web.key-file=/etc/tls/private/tls.key`; the image is `quay.io/prometheus-operator/admission-webhook`.

## Registering
Once the service runs, create `ValidatingWebhookConfiguration` and `MutatingWebhookConfiguration` objects telling the API server when to call it. Endpoints: `/admission-prometheusrules/validate` (rule validation), `/admission-prometheusrules/mutate` (coerces integer and boolean YAML values in `PrometheusRule` objects into strings), `/admission-alertmanagerconfigs/validate` (the guide registers it for `v1alpha1`) and `/convert` (AlertmanagerConfig conversion between `v1alpha1` and `v1beta1`). The guide's configurations use `failurePolicy: Fail`, `sideEffects: None` and a `cert-manager.io/inject-ca-from` annotation.

Conversion is not enabled by annotation alone: patch the CRD `alertmanagerconfigs.monitoring.coreos.com` with `spec.conversion.strategy: Webhook`, a `clientConfig.service` pointing at the webhook Service (path `/convert`, port 443) and `conversionReviewVersions` `v1beta1` and `v1alpha1`. Then annotate the CRD, for example `kubectl annotate crds alertmanagerconfigs.monitoring.coreos.com cert-manager.io/inject-ca-from=default/prometheus-operator-admission-webhook`, so cert-manager injects the CA.

## CA bundle
The API server verifies the webhook certificate using `caBundle` in `clientConfig`. cert-manager injects it automatically; without it, set the base64 CA certificate by hand in both webhook configurations and in the CRD.

## Checked

2026-11-08. Read the webhook guide in full. Corrected the conversion step (a CRD patch with spec.conversion is required, the annotation only injects the CA) and added the mutate and AlertmanagerConfig validate endpoints.

Method: documentation only; no commands were run.
