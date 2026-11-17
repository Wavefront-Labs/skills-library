---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-exposing-prometheus-and-alertmanager
name: prometheus-operator-exposing-prometheus-and-alertmanager
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [exposing-services, nodeport-service, kubectl-proxy, externalurl, routeprefix, ingress]
level: practitioner
status: docs-checked
description: "Expose Prometheus and Alertmanager via NodePort, the Kubernetes API proxy with externalUrl, or Ingress, using the labels the operator puts on pods."
sources:
  - https://prometheus-operator.dev/docs/platform/exposing-prometheus-and-alertmanager/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## Pod labels to select on
Prometheus pods carry `prometheus: <name>`; Alertmanager pods carry `alertmanager: <name>`. A Service must use that selector.

## NodePort
A Service with `type: NodePort`, port 9090 and `targetPort: web`, `nodePort: 30900`, selector `prometheus: main` exposes the UI at `http://<node-ip>:30900/`. Alertmanager works the same with port 9093, `nodePort: 30903` and selector `alertmanager: main`.

## Kubernetes API proxy
Create a `ClusterIP` Service and reach it through `http(s)://control-plane-host/api/v1/proxy/namespaces/<namespace>/services/<service>:<port>/`; `kubectl proxy` handles authentication. Prometheus and Alertmanager must know the URL they are served under, so set `externalUrl`, for example `http://127.0.0.1:8001/api/v1/proxy/namespaces/default/services/prometheus-main:web/`. The host is where `kubectl proxy` listens by default. The Alertmanager object follows the same rule.

## Ingress
Needs a running Ingress controller (the example was tested with the NGINX Ingress Controller). The Ingress routes to the internal Services, so they are still required. The page's Ingress example is written with the old `extensions/v1` API (`serviceName`, `servicePort`), so adapt it to the Ingress API your cluster serves. The example uses rewrite paths `/prometheus(/|$)(.*)` and `/alertmanager(/|$)(.*)` on one host, and restricts sources with the whitelist-source-range annotation. The objects then set `externalUrl` to the public URL including the path, for example `http://monitoring.my.systems/prometheus` and `http://monitoring.my.systems/alertmanager`, matching the Ingress paths.

If the Ingress is exposed to the internet everyone gets full access, so enable external authentication or IP whitelisting.

## Checked

2026-11-08. Read the exposing Prometheus and Alertmanager page in full. Pod labels, NodePort values, API proxy URL scheme, externalUrl examples and the Ingress warning match. Added a note that the page Ingress example uses the old extensions/v1 API.

Method: documentation only; no commands were run.
