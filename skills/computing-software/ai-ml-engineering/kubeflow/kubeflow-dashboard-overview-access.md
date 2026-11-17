---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-dashboard-overview-access
name: kubeflow-dashboard-overview-access
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [central-dashboard, istio-gateway, port-forward, dashboard-navigation]
level: intro
status: docs-checked
description: "Central Dashboard overview: the sections it exposes per component, and how to reach it through the Istio ingress gateway with kubectl port-forward."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/central-dash/overview.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/central-dash/access.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dashboard overview access

The Central Dashboard is the authenticated web UI for Kubeflow and ecosystem components. It provides authentication and authorization based on Profiles and Namespaces, links to component UIs, and customizable links to third-party apps.

Sections by component:
- Core: Home, Manage Contributors (contributors of profiles you own).
- Kubeflow Notebooks: Notebooks, TensorBoards, Volumes (PVCs).
- Katib: Katib Experiments.
- KServe: KServe Endpoints.
- Kubeflow Pipelines: Pipelines, Experiments, Runs, Recurring Runs, Artifacts and Executions (the last two tracked in MLMD).

Access: the dashboard sits behind the Istio Gateway of the service mesh. Packaged distributions have their own access method; consult that distribution. For the Kubeflow Community Distribution use port-forwarding:

```shell
export ISTIO_NAMESPACE=istio-system
kubectl port-forward svc/istio-ingressgateway -n ${ISTIO_NAMESPACE} 8080:80
```

Open `http://localhost:8080`. Unchanged default credentials are `user@example.com` with password `12341234`; change them for anything beyond a local trial.

## Checked

Confirmed the dashboard sections per component, the Istio gateway access path, the port-forward command and the default credentials. Nothing removed.

Method: docs-checked 2026-11-09 against the raw kubeflow/website central-dash overview.md and access.md pages, read in full.
