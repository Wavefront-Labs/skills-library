---
id: computing-software.messaging-and-integration.dapr.kubernetes-install-with-helm
name: kubernetes-install-with-helm
category: computing-software
field: messaging-and-integration
product: dapr
tags: [kubernetes, helm, dapr-system, high-availability, dashboard, mariner]
level: practitioner
status: docs-checked
description: "Install the Dapr control plane with Helm v3: repo add, helm upgrade --install into dapr-system, HA settings per service, optional dashboard chart, verification pods and uninstall."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/hosting/kubernetes/kubernetes-deploy.md
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/hosting/kubernetes/kubernetes-production.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dapr needs Helm v3 (Helm v2 is not supported by the current chart). Add the repo and install:

```bash
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update
# See which chart versions are available
helm search repo dapr --devel --versions
helm upgrade --install dapr dapr/dapr \
--version=<chart version> \
--namespace dapr-system \
--create-namespace \
--wait
```

High availability for everything: add `--set global.ha.enabled=true`. To scale only some services, turn the global flag off and enable the services individually:

```bash
--set global.ha.enabled=false \
--set dapr_scheduler.ha=true \
--set dapr_placement.ha=true \
```

The docs recommend keeping settings in a values file under source control rather than long `--set` lists, for example:

```yaml
global:
  ha:
    enabled: true
```

then `helm install dapr dapr/dapr --version=<Dapr chart version> --namespace dapr-system --create-namespace --values values.yml --wait`.

The dashboard is a separate chart: `helm install dapr-dashboard dapr/dapr-dashboard --namespace dapr-system`.

Verify with `kubectl get pods --namespace dapr-system`: expect `dapr-operator`, `dapr-placement`, `dapr-sidecar-injector`, `dapr-sentry` (and the dashboard if installed). For Mariner images set `--set global.tag=<version>-mariner`. Remove with `helm uninstall dapr --namespace dapr-system`.

## Checked

Helm commands, HA flags, dashboard chart, expected pods, Mariner tag and uninstall confirmed on the Deploy page (Helm tab); values-file advice and individual HA settings confirmed on the production guidelines page.

Method: docs-checked 2026-11-09 against raw v1.15 kubernetes-deploy.md (read in full) and kubernetes-production.md (read the HA, values-file and Helm sections via grep); no commands were run.
