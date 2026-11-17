---
id: computing-software.cloud-infrastructure-engineering.rancher.project-resource-quotas-and-namespace-defaults
name: project-resource-quotas-and-namespace-defaults
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [resource-quotas, projects, namespaces, project-limits, namespace-default-limits, annotations, kubectl]
level: practitioner
status: docs-checked
description: "Rancher project resource quotas: project versus namespace default limits, UI versus kubectl namespaces, and the quota annotations."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/advanced-user-guides/manage-projects/manage-project-resource-quotas/about-project-resource-quotas
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Native Kubernetes applies a resource quota to one namespace at a time. Rancher applies it to a **project**, propagates it to each namespace, and Kubernetes enforces it with native ResourceQuota objects. Two limits are set when creating or editing a project:

- **Project Limits**: a total for each resource shared among all namespaces in the project.
- **Namespace Default Limits**: the default quota for each namespace, bound automatically when a namespace is created without overrides.

Nuances for namespaces made in the Rancher UI: deleting the quota at project level removes it from every namespace, overrides included; and changing a namespace default at project level is **not** pushed to existing namespaces, only to new ones. Before creating a namespace Rancher compares the project's available resources with those requested; if the request exceeds what remains, the namespace gets the remaining capacity.

Namespaces created **outside** the UI behave differently: through kubectl, Rancher assigns a quota of **zero** for any resource requesting more than remains. Join a project and optionally override defaults with annotations:

```
apiVersion: v1
kind: Namespace
metadata:
  annotations:
    field.cattle.io/projectId: <YOUR_CLUSTER_ID>:<YOUR_PROJECT_ID>
    field.cattle.io/resourceQuota: '{"limit":{"limitsCpu":"100m", "configMaps": "50"}}'
  name: my-ns
```

Rancher overrides only resources defined on the project quota, so `configMaps` would be ignored if the project quota lacks it. For extra custom limits use the `extended` map, or create dedicated native `ResourceQuota` objects in specific namespaces; Rancher ignores user-defined quotas in namespaces of a project with a quota.

## Checked

2026-11-09. Read the cited How Resource Quotas Work in Rancher Projects page in full and checked every claim against it (two limits, UI versus kubectl behaviour, annotations and example, extended map, native ResourceQuota note). Aligned the annotation placeholders with the page.

Method: documentation only; no commands were run.
