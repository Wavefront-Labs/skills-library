---
id: computing-software.cloud-infrastructure-engineering.rancher.hosted-gke-cluster-service-account
name: hosted-gke-cluster-service-account
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [gke, google-cloud, service-account, cloud-credentials, autopilot, project-id]
level: practitioner
status: docs-checked
description: "Provision GKE clusters from Rancher: service account roles, JSON key as cloud credential, project ID, and Standard mode only."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/kubernetes-clusters-in-rancher-setup/set-up-clusters-from-hosted-kubernetes-providers/gke
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
GKE needs a Google **service account** that operates the cluster; creating it also generates a private key for authentication. The page lists four required roles:

- Compute Viewer: `roles/compute.viewer`
- Project Viewer: `roles/viewer`
- Kubernetes Engine Admin: `roles/container.admin`
- Service Account User: `roles/iam.serviceAccountUser`

Save the key in **JSON** format. The cluster must also belong to a Google project, so you need its **project ID**. Deploying to GKE incurs charges.

Provisioning has two steps in Rancher:

1. **Create a cloud credential.** Under **Cluster Management > Cloud Credentials > Create**, name it and paste the private key JSON into the **Service Account** box, or upload the JSON file.
2. **Create the cluster.** Under **Clusters > Create > Google GKE**, enter a name, optionally set Member Roles, and complete the form.

GKE must be in **Standard mode**. Autopilot clusters restrict editing the kube-system namespace, and Rancher needs to create resources there, so you cannot create a GKE cluster in Autopilot mode from Rancher.

## Checked

2026-11-09. Read the cited Creating a GKE Cluster page in full and checked every claim against it (four roles, JSON key, project ID, cloud credential steps, Standard mode, cluster creation steps). Removed the claims about hosting Rancher on Autopilot and about registered GKE clusters needing a cluster-admin binding, which the page does not state.

Method: documentation only; no commands were run.
