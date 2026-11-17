---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-helm-chart
name: woodpecker-helm-chart
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [helm, kubernetes, metrics]
level: practitioner
status: docs-checked
description: "Install Woodpecker on Kubernetes with the Helm chart and enable metrics."
sources: ["https://woodpecker-ci.org/docs/administration/installation/helm-chart"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker Helm chart

Install the official chart from the OCI registry:

```bash
helm install woodpecker oci://ghcr.io/woodpecker-ci/helm/woodpecker --version <VERSION>
```

The chart lives in the woodpecker-ci/helm repository.

Metrics: enable them in `values.yml`:

```yaml
metrics:
  enabled: true
  port: 9001
```

This activates `/metrics` on port `9001` without authentication. The port is not exposed externally by default. For authenticated external access use the Prometheus instructions.

To have Prometheus discover the pods, enable the PodMonitor:

```yaml
prometheus:
  podmonitor:
    enabled: true
    interval: 60s
    labels: {}
```

If metrics do not arrive, check your Prometheus configuration lists your namespace explicitly in `podMonitorNamespaceSelector`, or that the selectors are disabled:

```yaml
podMonitorNamespaceSelector:
  matchLabels: {}
podMonitorSelector:
  matchLabels: {}
```

An empty `matchLabels` selects all namespaces and all pod monitors.

With the Kubernetes backend, steps run as standalone Pods; see the Kubernetes backend skills for agent variables.

Metrics stay internal unless you expose them yourself, which is the safe default. The chart installs the server, while the agent connects to it the same way as in other deployments, using the shared agent secret.

## Checked

2026-11-03. Read the Woodpecker Helm chart installation page and confirmed the chart values described in the skill. Nothing removed. 

Method: documentation only; no commands were run.
