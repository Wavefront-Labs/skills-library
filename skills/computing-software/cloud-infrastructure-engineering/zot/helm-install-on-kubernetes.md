---
id: computing-software.cloud-infrastructure-engineering.zot.helm-install-on-kubernetes
name: helm-install-on-kubernetes
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, helm-chart, kubernetes-install, helm-values, node-port, service-type]
level: intro
status: docs-checked
description: "Install Zot on Kubernetes with the project-zot Helm chart: add the repo, review values, install with --set or a values file, verify and uninstall."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/install-guides/install-guide-k8s.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```
helm repo add project-zot http://zotregistry.dev/helm-charts
helm search repo project-zot
helm repo update project-zot
helm show values project-zot/zot
```

Key values and defaults: `replicaCount` 1; `image.repository` `ghcr.io/project-zot/zot`; `image.pullPolicy` `IfNotPresent`; `image.tag` defaults to the chart appVersion; `serviceAccount.create` true; `service.type` `NodePort`; `service.port` 5000. `strategy.type` is also configurable (Kubernetes deployment strategy).

Customise:

```
--set image.repository=ghcr.io/project-zot/zot-minimal
--set replicaCount=2,service.port=5050
-f myfile.yaml
```

Install:

```
helm install zot project-zot/zot
helm install -f myfile.yaml zot project-zot/zot
helm install zot project-zot/zot --version 0.1.0
```

Verify: `helm list`, then derive the NodePort and node IP with kubectl and run `curl http://$NODE_IP:$NODE_PORT/v2/_catalog`; a fresh install returns `{"repositories":[]}`.

The chart installs a minimal `/etc/zot/config.json` (`rootDirectory` `/var/lib/registry`, address `0.0.0.0`, port `5000`, log level `debug`). Edit it for auth, storage and extensions.

Uninstall: `helm uninstall zot`.

## Checked

2026-11-04. Confirmed against the zot Kubernetes install guide. Reworded the strategy.type line to state only that it is a configurable value.

Method: documentation only; no commands were run.
