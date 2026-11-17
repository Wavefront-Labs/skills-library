---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-pipelines-connect-sdk-api
name: kubeflow-pipelines-connect-sdk-api
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [connect-api, kfp-client, serviceaccount-token, kf-pipelines-sa-token-path, poddefault-token]
level: advanced
status: docs-checked
description: "Connect the KFP SDK to the Pipelines API in multi-user Kubeflow using a projected ServiceAccount token, KF_PIPELINES_SA_TOKEN_PATH and a PodDefault."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/user-guides/core-functions/connect-api.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/operator-guides/multi-user.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipelines connect sdk api

In multi-user Kubeflow, how kfp.Client authenticates depends on whether you run inside or outside the cluster and whether KFP is standalone. From a pod in the cluster, use a projected ServiceAccount token with audience `pipelines.kubeflow.org`.

```python
import kfp
kfp_client = kfp.Client()
experiments = kfp_client.list_experiments(namespace="my-profile")
```

`kfp.Client()` automatically reads the token from the path in environment variable `KF_PIPELINES_SA_TOKEN_PATH`.

Option 1, add to the PodSpec: a projected volume with `serviceAccountToken` (`path: token`, `expirationSeconds: 7200`, `audience: pipelines.kubeflow.org`), mounted read-only at `/var/run/secrets/kubeflow/pipelines`, plus `KF_PIPELINES_SA_TOKEN_PATH=/var/run/secrets/kubeflow/pipelines/token`.

Option 2, a `PodDefault` in your profile namespace that injects the same env var and volume for pods labeled with its selector (for example `access-ml-pipeline: "true"`); pick that configuration when creating a notebook.

Multi-user isolation: Experiments belong to a namespace, and runs and recurring runs belong to their experiment's namespace. The API server rejects requests for namespaces the user cannot access. Pipeline definitions are shared across namespaces. Profile isolation is namespace-level only, with no stronger security guarantee. The API respects Kubernetes RBAC, so the ServiceAccount needs a RoleBinding such as one to ClusterRole `kubeflow-edit`; Notebook pods run as `default-editor` by default. PodDefaults are namespaced, so create one in each profile namespace. Standalone KFP has no multi-user authentication: connect with `kfp.Client(host="http://ml-pipeline-ui:80")` in the same namespace.

## Checked

2026-11-08. Confirmed against the Connect the SDK to the API and Multi-user Isolation pages: token path, volume settings, audience, PodDefault, RBAC note, isolation rules and the standalone host. Dex-based access from outside the cluster is on the page but not covered here.
Method: docs-only read of cited pages, 2026-11-08
