---
id: computing-software.ai-ml-engineering.kserve.kserve-install-dependencies
name: kserve-install-dependencies
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [dependencies, cert-manager, istio, knative-operator, gateway-api-crds, envoy-gateway, envoy-ai-gateway, lws-operator, keda-otel-addon, quick-install-definition, dependency-matrix]
level: practitioner
status: docs-checked
description: "Which infrastructure KServe needs per mode (Knative, Standard, LLMIsvc, optional KEDA), pinned versions, per-component install scripts and custom dependency definition files."
sources: ["https://github.com/kserve/website/blob/main/docs/install/dependencies.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# KServe install dependencies per mode

| Dependency | Knative | Standard | LLMIsvc |
|---|---|---|---|
| cert-manager (v1.17.0 for Knative, v1.17.0+ for Standard) | required | required | required |
| Istio (1.27.1), Istio IngressClass | required | no | no |
| Knative Operator (v1.21.1) + Serving | required | no | no |
| Gateway API CRDs + extension CRDs, Envoy Gateway, Envoy AI Gateway, GatewayClass, Gateway | no | no | required |
| LWS (LeaderWorkerSet) operator | no | no | required |
| KEDA (+ KEDA OTEL addon, OpenTelemetry Operator) | optional | optional | optional |
| External LB | optional | optional | required on Kind/Minikube |

Tools: helm, yq, kubectl (plus kustomize for Knative).

```bash
curl -fsSL https://github.com/kserve/kserve/releases/download/v0.20.0/kserve-standard-mode-dependency-install.sh | bash
# also: kserve-knative-mode-dependency-install.sh, llmisvc-dependency-install.sh, keda-dependency-install.sh
```

Individual scripts live under `hack/setup/infra/` (for example `manage.cert-manager-helm.sh`, `manage.istio-helm.sh`, `manage.keda-helm.sh`, `gateway-api/manage.gateway-api-crd.sh`).

## Custom dependency scripts
Write a `.definition` YAML with required `DESCRIPTION` and `COMPONENTS` (each `name` matches a script in `hack/setup/infra/`, optional `env`), plus optional `TOOLS`, `INCLUDE_DEFINITIONS` (last wins, cycles detected) and `GLOBAL_ENV`. Generate with `python hack/setup/scripts/install-script-generator/generator.py my.definition OUTDIR/`; run the output script, with `--uninstall` to remove. `make generate-quick-install-scripts` regenerates all from the definition files in `hack/setup/quick-install/definitions/`.

## Checked
Confirmed against the KServe website install dependencies page: per-mode component tables and versions, CLI tools, release script names, per-component scripts, definition file fields and the dependency matrix. Changed the cert-manager version note (Standard lists v1.17.0+).

Method: docs-only read of cited pages, 2026-11-08
