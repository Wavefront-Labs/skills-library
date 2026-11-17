---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-notebooks-create-notebook-server
name: kubeflow-notebooks-create-notebook-server
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [notebooks, new-server, poddefault, workspace-volume, shared-memory]
level: intro
status: docs-checked
description: "Create a Kubeflow Notebook server from the Central Dashboard: namespace, image, CPU, RAM, workspace and data volumes, PodDefault configurations, GPUs and shared memory."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/notebooks/overview.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/notebooks/quickstart-guide.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Notebooks create notebook server

Kubeflow Notebooks runs interactive JupyterLab, RStudio and Visual Studio Code (code-server) environments in the cluster. Access control uses Kubeflow RBAC, so notebooks are shareable across an organization, and admins can offer standard images.

Steps in the Central Dashboard:
1. Select the namespace matching your Kubeflow Profile.
2. Open Notebooks (Notebook Servers) and click New Server.
3. Name it (letters and numbers, no spaces).
4. Pick an image: a standard image from the admin-configured list, or Custom with `registry/image:tag`.
5. Set CPU and RAM requests.
6. Set a workspace volume, mounted as a PVC on the home folder; optionally add data volumes (PVCs).
7. Optionally select configurations. These are PodDefault resources in your profile namespace whose `selector.matchLabels` match the label you pick, for example `add-gcp-secret` mounting a secret at `/secret/gcp`.
8. Optionally request GPUs (Kubeflow sets pod limits) and enable shared memory. Kubernetes has no native shared-memory setting, so Kubeflow mounts an empty-dir volume at `/dev/shm`, which libraries such as PyTorch use for multiprocessing.
9. Click Launch, which creates a Notebook CRD; the status icon spins until the pod is provisioned. Click Connect to open the web interface.

## Checked

Confirmed the feature summary and each step of the creation flow, including the PodDefault label matching, GPU limits and the /dev/shm workaround. Nothing removed.

Method: docs-checked 2026-11-09 against the raw kubeflow/website notebooks overview.md and quickstart-guide.md pages, read in full.
