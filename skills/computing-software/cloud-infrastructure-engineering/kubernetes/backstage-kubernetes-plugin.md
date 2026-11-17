---
id: computing-software.cloud-infrastructure-engineering.kubernetes.backstage-kubernetes-plugin
name: backstage-kubernetes-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, platform-engineering, backstage-kubernetes-plugin, backstage, developer-portal, rbac]
level: practitioner
status: docs-checked
description: "Set up the Backstage Kubernetes plugin so service pages show their pods, deployments and errors across clusters, with cluster config, entity annotations and read-only RBAC."
sources: ["https://backstage.io/docs/features/kubernetes/", "https://backstage.io/docs/features/kubernetes/installation", "https://backstage.io/docs/features/kubernetes/configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backstage Kubernetes plugin

## Install
```bash
yarn --cwd packages/app add @backstage/plugin-kubernetes
yarn --cwd packages/backend add @backstage/plugin-kubernetes-backend
```
```ts
// packages/backend/src/index.ts (new backend system)
backend.add(import('@backstage/plugin-kubernetes-backend'));
```
With the new frontend system the "Kubernetes" tab is added by default feature discovery for entities that carry Kubernetes data; the tab filter can be customised through `app.extensions` in `app-config.yaml`.

## Clusters (app-config.yaml)
```yaml
kubernetes:
  serviceLocatorMethod: {type: multiTenant}
  clusterLocatorMethods:
  - type: config
    clusters:
    - name: prod-eu-1
      url: https://prod-eu-1.k8s.example.com
      authProvider: serviceAccount
      serviceAccountToken: ${K8S_PROD_EU_1_TOKEN}
      caData: ${K8S_PROD_EU_1_CA}
      skipTLSVerify: false      # default false
      skipMetricsLookup: false  # default false
```
`serviceLocatorMethod` is `multiTenant` (every component runs on every cluster), `singleTenant` (a component
runs on one cluster) or `catalogRelation`. Valid `clusterLocatorMethods` types are `config`, `catalog`
(catalog Resources of type `kubernetes-cluster`), `gke`, `localKubectlProxy` and a custom
`KubernetesClustersSupplier`. Valid `authProvider` values are `aks`, `aws`, `azure`, `google`,
`googleServiceAccount`, `oidc` and `serviceAccount`; the per-user ones (`google`, `aks`, `oidc`) let users see
only what their own identity allows. A long-lived `serviceAccountToken` is probably not ideal for production.

## Linking entities to workloads
```yaml
# catalog-info.yaml
metadata:
  annotations:
    backstage.io/kubernetes-id: checkout
    # or: backstage.io/kubernetes-label-selector: 'app=checkout,component=front-end'  (takes precedence over the id)
    # optional: backstage.io/kubernetes-namespace: shop
```
Workload objects and pods need the label `backstage.io/kubernetes-id: checkout` (when using the id
annotation).

## RBAC for the service account
Read-only ClusterRole with `get`, `list`, `watch` on pods, pods/log, configmaps, services, deployments,
replicasets, horizontalpodautoscalers, ingresses, statefulsets, limitranges, resourcequotas and daemonsets,
`batch` jobs and cronjobs, plus `get`, `list` on `metrics.k8s.io` pods for usage. No Secrets.

## Verify
The service page lists the entity's Kubernetes objects per cluster, including pods and their status.

## Checked

Checked against the Backstage docs on `backstage/backstage` master (last commit 2026-10-25): `features/kubernetes/configuration.md`, `installation.md`.
Confirmed: `serviceLocatorMethod` values, `clusterLocatorMethods` types, the `authProvider` list, `skipTLSVerify` and `skipMetricsLookup` defaults (false), the `kubernetes-id`, `kubernetes-label-selector` and `kubernetes-namespace` annotations, the backend install line and the documented read-only ClusterRole.
Corrected: removed the nonexistent EKS-like and Cluster API locators and the claim that crash-looping pods are highlighted; RBAC list now matches the doc.

Method: documentation only; no commands were run.
