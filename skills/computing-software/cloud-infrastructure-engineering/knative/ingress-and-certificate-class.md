---
id: computing-software.cloud-infrastructure-engineering.knative.ingress-and-certificate-class
name: ingress-and-certificate-class
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [ingress-class, networking-knative-dev-ingress-class, multiple-networking-layers]
level: advanced
status: docs-checked
description: "Override the networking ingress class per Service with an annotation."
sources:
  - https://knative.dev/docs/serving/services/ingress-class/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use more than one networking layer on the same cluster.

Ingress class: when a Service is created, an `ingress-class` is assigned automatically from the `config-network` ConfigMap in `knative-serving`. Changing it there affects only newly created Services. Using the default is generally recommended, but with multiple networking implementations you can set a class per Service.

```bash
kubectl annotate kservice <service-name> networking.knative.dev/ingress-class=<ingress-type>
```

The annotation overrides the `ingress-class` value in `config-network`.

Here `<service-name>` is the Service being annotated and `<ingress-type>` the ingress used as its class. If no class is specified, it defaults to `istio.ingress.networking.knative.dev`.

## Checked

2026-11-03. Confirmed on the Knative Serving services/ingress-class page: config-network ingress-class, new-Services-only warning, annotation command and override. Removed: the certificate-class section and networking-layer list (not on the page).
Method: documentation only; no commands were run.
