---
id: computing-software.ai-ml-engineering.ml-platform-engineering.kubeflow-notebooks-and-profiles
name: kubeflow-notebooks-and-profiles
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, kubeflow-notebooks, kubeflow-profiles, multi-tenancy, jupyter, poddefaults]
level: practitioner
status: docs-checked
description: "Provide multi-tenant notebooks with Kubeflow: Profiles wrapping namespaces, owner and contributor access, generated RBAC and Istio policies, quotas, automatic profile creation."
sources:
  - https://www.kubeflow.org/docs/components/notebooks/
  - https://www.kubeflow.org/docs/components/central-dash/profiles/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Kubeflow Notebooks and profiles

**Goal:** each user or team gets an isolated, quota-limited namespace on the shared Kubernetes cluster for notebook servers.

## Profiles (tenancy)
A Kubeflow Profile is a Kubernetes CRD that wraps a Namespace of the same name. A profile has a single owner and can have contributors with view or modify access. The owner (or a cluster admin) adds and removes contributors. The Profile Controller reconciles profiles and namespaces; contributors are managed by the Access Management API (KFAM).
```yaml
apiVersion: kubeflow.org/v1
kind: Profile
metadata:
  name: team-fraud          # becomes the namespace name; unexpected behaviour if it already exists
spec:
  owner: {kind: User, name: admin@example.com}
  plugins: []
  resourceQuotaSpec: {}     # optional ResourceQuota for the profile
```
Create with `kubectl apply -f`, list with `kubectl get profiles`, describe with `kubectl describe profile <name>`. Deleting a profile deletes its namespace and everything in it.

## What a profile creates
- A Namespace named like the profile.
- Owner: RoleBinding `namespaceAdmin` to ClusterRole `kubeflow-admin`, and Istio AuthorizationPolicy `ns-owner-access-istio`.
- Each contributor: RoleBinding and AuthorizationPolicy named `user-<email>-clusterrole-<edit|view>` (ClusterRole `kubeflow-edit` or `kubeflow-view`).
- ServiceAccounts `default-editor` and `default-viewer` with RoleBindings to `kubeflow-edit` and `kubeflow-view`.

Platform pattern: make a global admin the owner of all profiles and give end users only view or modify access, so they cannot add or remove contributors. The Central Dashboard "Manage Contributors" tab only adds contributors with edit access; view access needs manually created RoleBinding and AuthorizationPolicy resources.

## Automatic profile creation
Disabled by default. The `CD_REGISTRATION_FLOW` environment variable on the central-dashboard Deployment enables it: a first-time user who owns no profile is prompted to create one and becomes its owner. Often unsuitable for managed platforms.

## Notebook servers
Kubeflow Notebooks documentation covers an overview, quickstart, container images, submitting Kubernetes resources from a notebook, troubleshooting and the API reference. Offer curated images with pinned CUDA and framework versions; put long jobs in pipelines or training operators, not notebooks. Check the docs for idle-culling and PodDefault configuration for your release.

## Verify
- [ ] Users cannot list or exec into other profiles' pods.
- [ ] Quotas block exceeding GPU limits.
- [ ] Idle notebooks are reclaimed after the configured time.

## Checked
2026-11-01. Confirmed on the Kubeflow Profiles and Namespaces page and the Notebooks index: Profile CRD behaviour, owner/contributor roles, generated RoleBindings, ClusterRoles, AuthorizationPolicies and ServiceAccounts, `CD_REGISTRATION_FLOW` default, Manage Contributors limitation, kubectl commands, deletion warning, Notebooks doc sections. Removed (not on the fetched pages): the sample GPU quota values, PodDefault YAML, culling variables (`ENABLE_CULLING`, `CULL_IDLE_TIME`), Dex/OIDC header claims, time-slicing/MIG advice.
Method: documentation only; no commands were run.
