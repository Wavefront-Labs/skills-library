---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-katib-install-control-plane-sdk
name: kubeflow-katib-install-control-plane-sdk
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [install, katib-standalone, python-sdk, kustomize, katib-install]
level: intro
status: docs-checked
description: "Install the Katib control plane with kustomize and the kubeflow-katib Python SDK, and verify the four control plane pods are running."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/installation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Katib install control plane sdk

Minimum requirements: Kubernetes 1.27 or newer, kubectl 1.27 or newer, Python 3.7 or newer. Skip the control plane steps if you installed the Kubeflow Community Distribution, which already includes Katib.

Control plane (standalone), stable release v0.19.0:

```shell
kubectl apply -k "github.com/kubeflow/katib.git/manifests/v1beta1/installs/katib-standalone?ref=v0.19.0"
```

Use `?ref=master` for the latest changes. Verify with `kubectl get pods -n kubeflow`; you should see `katib-controller`, `katib-db-manager`, `katib-mysql` and `katib-ui` running.

The cluster needs a StorageClass for dynamic provisioning for the Katib DB. Without dynamic volume provisioning, deploy a PersistentVolume manually to bind the PVC of the Katib DB component.

Python SDK:

```shell
pip install -U kubeflow-katib
pip install git+https://github.com/kubeflow/katib.git@master#subdirectory=sdk/python/v1beta1
```

The second form installs the latest master; you can also pin a specific commit in the same URL. Standalone installs need a local kubeconfig pointing at the cluster. Inside a Kubeflow Notebook, the SDK can run directly.

Next: run the Getting Started example, and read the page on options for installing the control plane components.

## Checked

2026-11-08. Confirmed against the Katib installation page: prerequisites, the standalone kustomize commands and v0.19.0 reference, the verification pods, the StorageClass note and the pip commands. Removed the list of alternative install variants, which this page does not give.
Method: docs-only read of cited pages, 2026-11-08
