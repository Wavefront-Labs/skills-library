---
id: computing-software.ai-ml-engineering.kserve.kserve-config-ingress-settings
name: kserve-config-ingress-settings
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [inferenceservice-config, ingress-config, enablegatewayapi, kserveingressgateway, ingressdomain, domaintemplate, pathtemplate, urlscheme, disableingresscreation, disablehttproutetimeout, networkingkserveiovisibility, cluster-local]
level: advanced
status: docs-checked
description: "The ingress key of the inferenceservice-config ConfigMap: gateways, ingressDomain, domainTemplate, urlScheme, pathTemplate, disableIngressCreation and the visibility label."
sources: ["https://github.com/kserve/website/blob/main/docs/admin-guide/configurations.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# inferenceservice-config: ingress settings

All global defaults live in ConfigMap `inferenceservice-config` in namespace `kserve`, one JSON string per key (`ingress`, `storageInitializer`, `credentials`, `deploy`, `inferenceService`, `logger`, `batcher`, `agent`, `router`, `explainers`, `metricsAggregator`, `opentelemetryCollector`, `localModel`, `multiNode`, `service`, `security`). The ingress keys (the page lists "Per-service annotation key: Not supported" for the gateway, domain, class, template and scheme keys; `disableIngressCreation` has the per-service label shown below):

| Key | Default | Notes |
|---|---|---|
| `enableGatewayApi` | false | raw/Standard mode only |
| `kserveIngressGateway` | `kserve/kserve-ingress-gateway` | namespace/name |
| `ingressGateway` | `knative-serving/knative-ingress-gateway` | Knative with Istio |
| `localGateway` / `localGatewayService` | `knative-serving/knative-local-gateway` / `knative-local-gateway.istio-system.svc.cluster.local` | Knative with Istio; `knativeLocalGatewayService` for separate KServe gateways (strict mTLS) |
| `ingressDomain` | example.com | raw mode; `additionalIngressDomains` adds more |
| `ingressClassName` | istio | used when Gateway API is off |
| `domainTemplate` | `{{ .Name }}-{{ .Namespace }}.{{ .IngressDomain }}` | also `.Annotations.key`, `.Labels.key`; raw mode |
| `urlScheme` | http | http or https |
| `pathTemplate` | empty | e.g. `/serving/{{ .Namespace }}/{{ .Name }}`; empty means no path URL; the page describes it for serverless deployment |
| `disableIstioVirtualHost` | false | true: no top-level Istio VirtualService, so other Knative networking layers can be used (the page links the Kourier guide) |
| `disableIngressCreation` | false | raw mode |
| `disableHTTPRouteTimeout` | false | omit `spec.rules.timeouts`; needed for gateways like GKE Gateway that reject it (`Accepted=False/UnsupportedValue`) |

Per-service: label `networking.kserve.io/visibility: cluster-local` on an InferenceService keeps it off the external ingress (the page lists this label and the value `cluster-local` under `disableIngressCreation`).

## Checked

Checked 2026-11-08 against the KServe website page configurations.md, Ingress Configuration section and the ConfigMap section headings: key names, defaults, the raw versus serverless scope of each key, the visibility label and the list of ConfigMap keys. Corrected the blanket claim that no ingress key has a per-service setting, and clarified pathTemplate and disableIstioVirtualHost.

Method: docs-only read of cited pages, 2026-11-08
