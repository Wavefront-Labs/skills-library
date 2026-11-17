---
id: computing-software.cloud-infrastructure-engineering.google-cloud.installing-config-connector
name: installing-config-connector
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, infrastructure-as-code, config-connector-install, kcc-setup, gke, kubernetes-resource-model]
level: advanced
status: docs-checked
description: "Install Config Connector on GKE with the add-on or the manual operator, run namespaced mode with a service account per namespace, annotate the project and verify pods."
sources: ["https://cloud.google.com/config-connector/docs/how-to/install-upgrade-uninstall", "https://cloud.google.com/config-connector/docs/how-to/install-other-kubernetes", "https://cloud.google.com/config-connector/docs/concepts/installation-types", "https://cloud.google.com/config-connector/docs/how-to/organizing-resources/project-scoped-resources"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing Config Connector

## 1. Choose an installation type
- Manual installation with the operator is the recommended option: you control the version and the upgrade time. Namespaced mode is recommended for most use cases.
- Config Controller is a hosted service that includes Config Connector, with automatic upgrades but a restriction on custom workloads.
- The GKE add-on is available on GKE Standard only (not Autopilot), and its Config Connector version is often behind by up to 12 months or more.
- The add-on needs a workload identity pool and Kubernetes Engine Monitoring on the cluster. Enabling it creates a `configconnector-operator-system` namespace: do not change or add resources there.

```bash
gcloud container clusters update CLUSTER_NAME --update-addons ConfigConnector=ENABLED
```

The add-on also creates a ConfigConnector resource in namespaced mode for legacy reasons; to use cluster mode you still apply your own ConfigConnector manifest.

## 2. Manual operator install, namespaced mode
```bash
gcloud storage cp gs://configconnector-operator/latest/release-bundle.tar.gz release-bundle.tar.gz
tar zxvf release-bundle.tar.gz
kubectl apply -f operator-system/configconnector-operator.yaml   # Autopilot: operator-system/autopilot-configconnector-operator.yaml
```
Keep a copy of the bundle: you need it to uninstall. Then apply:
```yaml
apiVersion: core.cnrm.cloud.google.com/v1beta1
kind: ConfigConnector
metadata:
  name: configconnector.core.cnrm.cloud.google.com
spec:
  mode: namespaced
  stateIntoSpec: Absent
```
Per namespace (repeat for every namespace Config Connector manages): create the namespace and an IAM service account in the host project, grant it a role on the managed project, bind it to the Kubernetes service account `cnrm-controller-manager-NAMESPACE`, and grant `roles/monitoring.metricWriter` on the host project.
```bash
gcloud iam service-accounts add-iam-policy-binding \
    NAMESPACE_GSA@HOST_PROJECT_ID.iam.gserviceaccount.com \
    --member="serviceAccount:HOST_PROJECT_ID.svc.id.goog[cnrm-system/cnrm-controller-manager-NAMESPACE]" \
    --role="roles/iam.workloadIdentityUser"
```
The page's example grants `roles/owner` (or `roles/editor`, which excludes project- and organisation-wide changes such as IAM modifications); grant only what that team's resources need.
```yaml
apiVersion: core.cnrm.cloud.google.com/v1beta1
kind: ConfigConnectorContext
metadata:
  name: configconnectorcontext.core.cnrm.cloud.google.com   # one per namespace
  namespace: NAMESPACE
spec:
  googleServiceAccount: "NAMESPACE_GSA@HOST_PROJECT_ID.iam.gserviceaccount.com"
  stateIntoSpec: Absent
```

## 3. Where resources are created
Resolution order: a scope field in the resource spec (`spec.projectRef`), then the `cnrm.cloud.google.com/project-id` annotation on the resource, then the same annotation on the namespace (a resource-level annotation overrides it). If none is set, the namespace name is used as the project ID, which Google does not recommend.
```bash
kubectl annotate namespace NAMESPACE cnrm.cloud.google.com/project-id=PROJECT_ID
```
Create and annotate the namespace before applying resources to it. Folder and organisation scope use `cnrm.cloud.google.com/folder-id` and `cnrm.cloud.google.com/organization-id`.

## 4. Verify
```bash
kubectl get serviceaccount/cnrm-controller-manager-NAMESPACE -n cnrm-system
kubectl wait -n cnrm-system --for=condition=Ready pod \
    -l cnrm.cloud.google.com/component=cnrm-controller-manager \
    -l cnrm.cloud.google.com/scoped-namespace=NAMESPACE
```
The controller pod can take several minutes to start.

## Gotchas
- Cluster mode uses one shared IAM service account: anyone who can create Config Connector resources in any namespace acts with its full permissions. Avoid it in multi-tenant clusters.
- To stop managing a namespace, delete its Config Connector resources first, then the ConfigConnectorContext. Do not delete the context while managed resources remain.
- Do not uninstall Config Connector from a Config Controller cluster (unsupported).
- Fully downgrading is not supported; from 1.123.1 you can roll back namespaced operators with `spec.version` in the ConfigConnectorContext, by at most 3 minor versions.
- Switching from the add-on to manual: disable the add-on without deleting ConfigConnector or ConfigConnectorContext objects, then install an operator of the same or a later version.

## Checked
Confirmed 2026-11-08 against the four cited Config Connector pages: installation types, add-on install, manual install (namespaced and cluster mode, upgrade, downgrade), and project-scoped resources. Removed claims the pages do not state: the `deletion-policy: abandon` annotation, acquisition of existing resources by name, and the StorageBucket readiness commands.
Method: docs-only read of cited pages, 2026-11-08
