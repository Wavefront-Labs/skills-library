---
id: computing-software.devops-ci-cd.argo-workflows.security-permissions
name: security-permissions
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [security, controller-permissions, ui-read-only-role, automount-service-account-token, pod-controller]
level: advanced
status: docs-checked
description: "Understand what permissions the workflow controller needs, how users and pods are authorised, and a read-only UI role."
sources: ["https://argo-workflows.readthedocs.io/en/latest/security/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller and user permissions model
Controller: Kubernetes RBAC plus its ConfigMap decide access, either all namespaces (cluster install) or one managed namespace (namespace install). It needs list/get/update on workflows and cron workflows, create/get/delete on pods, PVCs and PDBs, and list/get on templates, ConfigMaps, service accounts and secrets.

Users: minimally create/read Workflows. The controller then creates pods and other resources for them, in the workflow's own namespace only, even if the user could not. So permission to create a Workflow equals permission to create pods in that namespace. Argo is a pod controller, like Job or Deployment, and apart from the workflow-restrictions feature it does not limit what pods can do.

Warning: if users may create Workflows in the controller's namespace (typically `argo`), they might modify the controller. In a namespace install the managed namespace should not be the controller's namespace.

Read-only UI: a Role with get/list/watch on core `events`, `pods`, `pods/log` and on `argoproj.io` resources `eventsources`, `sensors`, `workflows`, `workfloweventbindings`, `workflowtemplates`, `clusterworkflowtemplates`, `cronworkflows`, `workflowtaskresults`.

Workflow pods use `default` or the declared service account; no restriction applies to which one in the namespace. The token is mounted in the main container, which can patch pods; set `automountServiceAccountToken` to false to stop that. Pods run as root by default, so set a pod security context, pick the right executor, and apply these via workflow defaults.

## Checked
2026-11-03. Confirmed against the Argo Workflows Security page (Workflow Controller Security section): controller permissions, user permissions and the controller namespace warning, the pod controller note, the read-only UI role resources and verbs, and workflow pod service account, token and root defaults. Nothing removed.
Method: documentation only; no commands were run.
