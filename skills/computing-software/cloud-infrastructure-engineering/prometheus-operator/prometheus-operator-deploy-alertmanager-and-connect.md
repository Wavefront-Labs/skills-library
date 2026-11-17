---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-deploy-alertmanager-and-connect
name: prometheus-operator-deploy-alertmanager-and-connect
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [deploy-alertmanager, alertmanager-service, nodeport, alerting-alertmanagers, alertmanager-cluster]
level: practitioner
status: docs-checked
description: "Deploy a 3-replica Alertmanager, expose it, and point a Prometheus resource at it through spec.alerting.alertmanagers."
sources:
  - https://prometheus-operator.dev/docs/platform/platform-guide/
  - https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/main/Documentation/developer/alerting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An Alertmanager deduplicates alerts from Prometheus, silences them, and routes grouped notifications to integrations (PagerDuty, OpsGenie, mail, chat).

## Deploy
```yaml
apiVersion: monitoring.coreos.com/v1
kind: Alertmanager
metadata:
  name: example
spec:
  replicas: 3
```
Wait with `kubectl get pods -l alertmanager=example -w`. The guide describes the three-replica Alertmanager cluster as fully functional and highly available.

## Expose
The pods carry `alertmanager: example`, so a Service selects on that label. A `NodePort` Service on port 9093 targeting the named port `web` (for example `nodePort: 30903`) is the simplest option; see the Ingress guidance for production.

## Connect Prometheus
```yaml
spec:
  serviceAccountName: prometheus
  replicas: 2
  alerting:
    alertmanagers:
    - namespace: default
      name: alertmanager-example
      port: web
```
`namespace`, `name` and `port` must match the Service. Prometheus then discovers all Alertmanager pods behind it. Verify in the Prometheus UI under Status > Runtime and Build Information that three Alertmanagers were discovered.

By default Alertmanager starts with a minimal configuration that sends no notifications (developer alerting guide); see the configuration methods skill.

## Checked

2026-11-08. Read the platform guide and the developer alerting guide in full. Manifests, label selector, NodePort values and the Prometheus alerting block match. Removed the unsourced claim that the operator forms a gossip cluster in this guide and cited the alerting guide for the minimal default configuration.

Method: documentation only; no commands were run.
