---
id: computing-software.cloud-infrastructure-engineering.crossplane.rbac-manager-clusterroles
name: rbac-manager-clusterroles
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [rbac-manager, clusterrole, crossplane-admin, permissions]
level: practitioner
status: docs-checked
description: "Know what the RBAC manager does and what the crossplane-admin, edit and view ClusterRoles grant."
sources:
  - https://docs.crossplane.io/latest/guides/pods/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The RBAC manager is enabled by default. It:

- creates and binds roles for Provider service accounts so they can control their managed resources,
- lets the `crossplane` service account create managed resources,
- creates ClusterRoles for accessing Crossplane resources in all namespaces.

Its init container waits for the `CompositeResourceDefinition` and `ProviderRevision` types before starting.

Disable it before install with `rbacManager.deploy: false` in Helm values, or afterwards by deleting the `crossplane-rbac-manager` deployment. You must then define all Crossplane permissions manually.

ClusterRoles it creates (inspect with `kubectl describe clusterrole <name>`):

- `crossplane-admin`: full access to Crossplane types and to all secrets and namespaces, read-only on RBAC roles, CRDs and events, and can bind roles.
- `crossplane-edit`: full access to Crossplane types and all secrets, read-only on namespaces and events.
- `crossplane-view`: read-only on Crossplane types, namespaces and events.

Note that admin and edit include all Secrets, even those unrelated to Crossplane, so grant them sparingly.

## Checked

RBAC manager duties, init container, disable steps and the permissions of the three ClusterRoles confirmed on the Crossplane Pods page.

Method: docs-checked 2026-11-09 against the raw Crossplane Pods page (docs repo, current content folder), read in full.
