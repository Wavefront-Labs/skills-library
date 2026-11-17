---
id: computing-software.cybersecurity-defensive.falco.deploy-falco-with-helm
name: deploy-falco-with-helm
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [helm-install, helm-upgrade, falcosecurity-charts, kubernetes, tty]
level: intro
status: docs-checked
description: "Install, check, upgrade and uninstall Falco on Kubernetes with the official falcosecurity Helm chart, noting the Operator recommendation."
sources:
  - https://falco.org/docs/setup/kubernetes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The docs now recommend the Falco Operator for Kubernetes, with custom resources for instances, rules, plugins and configuration, while the Helm chart remains supported. Charts live at `https://falcosecurity.github.io/charts`.

Install:

```shell
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update
helm install --replace falco --namespace falco --create-namespace --set tty=true falcosecurity/falco
kubectl get pods -n falco
kubectl wait pods --for=condition=Ready --all -n falco
```

Pods may need a few seconds to start. The default install adds Falco to all nodes through a DaemonSet and requires Falco to be privileged; a driver may be installed on the node depending on its kernel.

Configuration is passed as Helm values; see the chart README for the list.

Upgrade by choosing the chart version that matches the Falco version you want (chart `4.8.1` ships Falco `0.38.2`):

```shell
helm upgrade falco falcosecurity/falco -n falco --version 4.8.1
```

Uninstall: `helm uninstall falco -n falco`.

Without Helm you can deploy plain manifests from the deploy-kubernetes repository.

Gotcha: read the chart BREAKING-CHANGES.md page before any upgrade to avoid disruption. The cluster needs Linux nodes.

## Checked

2026-11-08. Read the cited Kubernetes setup page in full. Removed the unsupported claim that tty=true makes log output appear immediately and replaced it with the documented DaemonSet and privileged behaviour.

Method: documentation only; no commands were run.
