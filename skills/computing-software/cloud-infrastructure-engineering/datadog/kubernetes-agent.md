---
id: computing-software.cloud-infrastructure-engineering.datadog.kubernetes-agent
name: kubernetes-agent
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, kubernetes, helm, datadog-operator, daemonset]
level: practitioner
status: docs-checked
description: "Deploy the Datadog Agent on Kubernetes with the Datadog Operator or Helm, name the cluster, and enable log collection and DogStatsD."
sources: ["https://docs.datadoghq.com/containers/kubernetes/installation/", "https://docs.datadoghq.com/containers/kubernetes/log/", "https://docs.datadoghq.com/extend/dogstatsd/", "https://docs.datadoghq.com/containers/cluster_agent/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Datadog Agent on Kubernetes
Goal: monitor a cluster with the Agent DaemonSet.

Install methods: Datadog Operator (recommended by the docs), Helm, or a manual DaemonSet. Helm path from the docs:

```
helm repo add datadog https://helm.datadoghq.com
helm repo update
kubectl create secret generic datadog-secret --from-literal api-key=<DATADOG_API_KEY>
helm install datadog-agent -f datadog-values.yaml datadog/datadog
```

```yaml
# datadog-values.yaml
datadog:
  apiKeyExistingSecret: datadog-secret
  clusterName: <CLUSTER_NAME>
  site: <DATADOG_SITE>
```

Operator path: `helm install datadog-operator datadog/datadog-operator`, create the same secret, then apply a `DatadogAgent` resource (`apiVersion: datadoghq.com/v2alpha1`) with `spec.global.clusterName`, `spec.global.site` and `spec.global.credentials.apiSecret` (`secretName: datadog-secret`, `keyName: api-key`) using `kubectl apply -f datadog-agent.yaml`. On Windows nodes add `--set targetSystem=windows` to the Helm install.

- `<CLUSTER_NAME>` scopes hosts and cluster checks: lowercase letters, numbers and hyphens only, starts with a letter, ends with a letter or number, at most 80 characters.
- Logs with Helm (apply with `helm upgrade -f datadog-values.yaml <RELEASE_NAME> datadog/datadog`):

```yaml
datadog:
  logs:
    enabled: true
    containerCollectAll: true
```

With the Operator the same switches are `features.logCollection.enabled` and `features.logCollection.containerCollectAll`. When `containerCollectAll` is `false` (the default) you must define Autodiscovery log configurations.
- DogStatsD with Helm: under `datadog:` set `dogstatsd.port: 8125`, `dogstatsd.useHostPort: true`, `dogstatsd.nonLocalTraffic: true`. `hostPort` needs a CNI-compliant network provider and opens a port on the host, so restrict firewall access.
- Cluster Agent: acts as a proxy between the API server and the node Agents to reduce API server load, supplies cluster-level metadata for enrichment, and supports HPA on custom and external metrics. Enable with `clusterAgent.enabled: true` in Helm values.
- If you use APM Single Step Instrumentation, install the Agent in its own namespace, since SSI does not instrument pods in the Agent's namespace.
- Agent pods carry the label `app.kubernetes.io/component:agent`; run `kubectl exec -it <POD_NAME> -- agent status` for the status page.
- Keep the Cluster Agent and Agent on matching versions.

## Verify
- Agent pods appear on the Containers page within a few minutes of deployment.

## Checked
2026-11-03. Confirmed against the Kubernetes installation, Kubernetes log collection, DogStatsD and Cluster Agent pages. Removed: `helm upgrade --install ... --create-namespace` form, the `apm.portEnabled` key (not on the pages read), "confirm" marker on the Operator recommendation (the docs recommend it), resource-limit and `containerExclude` advice.
Method: documentation only; no commands were run.
