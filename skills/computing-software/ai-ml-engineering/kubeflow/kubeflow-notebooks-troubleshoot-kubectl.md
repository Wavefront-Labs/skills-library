---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-notebooks-troubleshoot-kubectl
name: kubeflow-notebooks-troubleshoot-kubectl
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [troubleshooting, default-editor, kubeflow-edit, kubectl, notebook-pod]
level: practitioner
status: docs-checked
description: "Debug a Kubeflow Notebook that will not start with kubectl describe and logs, delete one manually, and understand the default-editor ServiceAccount inside notebook pods."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/notebooks/troubleshooting.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/notebooks/submit-kubernetes.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Notebooks troubleshoot kubectl

Notebook not starting: check in this order, with `MY_NOTEBOOK_NAME` and `MY_PROFILE_NAMESPACE` set:

```shell
kubectl describe notebooks "${MY_NOTEBOOK_NAME}" --namespace "${MY_PROFILE_NAMESPACE}"   # events
kubectl describe pod "${MY_NOTEBOOK_NAME}-0" --namespace "${MY_PROFILE_NAMESPACE}"       # pod events
kubectl get pod "${MY_NOTEBOOK_NAME}-0" --namespace "${MY_PROFILE_NAMESPACE}" -o yaml    # spec looks right?
kubectl logs "${MY_NOTEBOOK_NAME}-0" --namespace "${MY_PROFILE_NAMESPACE}"               # container logs
```

The notebook pod is named `<notebook-name>-0`.

Manual deletion of a stuck notebook: `kubectl delete notebook "${MY_NOTEBOOK_NAME}" --namespace "${MY_PROFILE_NAMESPACE}"`.

Submitting Kubernetes resources from inside a notebook: Kubeflow assigns the `default-editor` ServiceAccount to notebook pods. It is bound to `ClusterRole/kubeflow-edit`, which has namespace-scoped permissions on many resources (list them with `kubectl describe clusterrole kubeflow-edit`). Therefore `kubectl` works in the notebook terminal with no extra authentication, for example `kubectl create -f test.yaml --namespace "MY_PROFILE_NAMESPACE"`. Remember this ServiceAccount is highly privileged within the profile namespace.

## Checked

Confirmed the four diagnostic commands, the manual delete command, the default-editor ServiceAccount, its kubeflow-edit ClusterRole binding and the kubectl example. Removed the claim about who inherits the privileges because the page does not state it.

Method: docs-checked 2026-11-09 against the raw kubeflow/website notebooks troubleshooting.md and submit-kubernetes.md pages, read in full.
