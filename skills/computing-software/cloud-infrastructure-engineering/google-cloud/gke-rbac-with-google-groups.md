---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gke-rbac-with-google-groups
name: gke-rbac-with-google-groups
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, gke-rbac, google-groups-rbac, kubernetes-rbac, iam, multi-tenancy]
level: practitioner
status: docs-checked
description: "Grant Kubernetes RBAC to Google Groups in GKE: the gke-security-groups parent group, minimal IAM to reach the cluster, namespace RoleBindings and debugging who can do what."
sources: ["https://docs.cloud.google.com/kubernetes-engine/docs/how-to/google-groups-rbac", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/role-based-access-control"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GKE RBAC with Google Groups

IAM decides who can reach the cluster API; Kubernetes RBAC decides what they can do inside.
Use IAM for the coarse cluster-wide grant and RBAC on **groups** for namespaces.

## 1. Set up Google Groups for RBAC
1. Create a group named exactly `gke-security-groups@<your-domain>`.
2. Add the team groups (`team-payments@`, `sre@`) as **nested groups** of it; do not add individual users to it. Make sure the group has the View Members permission selected for group members.
3. Enable on the cluster:
```bash
gcloud container clusters update <C> --region=<R> --security-group=gke-security-groups@example.com
```

## 2. Minimal IAM
`container.clusters.get` (included in `roles/container.clusterViewer`) lets users authenticate to a cluster but does not authorise actions inside it; RBAC grants the rest. Broader IAM roles such as `roles/container.developer` or `roles/container.admin` grant Kubernetes permissions across the project's clusters, so avoid them for teams that should be limited by RBAC.

## 3. Namespace access
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata: {name: payments-edit, namespace: payments}
subjects:
- kind: Group
  name: team-payments@example.com
  apiGroup: rbac.authorization.k8s.io
roleRef: {kind: ClusterRole, name: edit, apiGroup: rbac.authorization.k8s.io}
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata: {name: sre-view}
subjects: [{kind: Group, name: sre@example.com, apiGroup: rbac.authorization.k8s.io}]
roleRef: {kind: ClusterRole, name: view, apiGroup: rbac.authorization.k8s.io}
```
For a `Group` subject, `name` is the email address of a Google Workspace group that is a member of the `gke-security-groups` group.

## 4. Debug
```bash
kubectl auth can-i create deployments -n payments --as=alice@example.com --as-group=team-payments@example.com
```
If you use Google Groups for RBAC, `google groups` appears in the log message of RBAC DENY audit log entries.

## Gotchas
- The parent group name `gke-security-groups` is required.
- Membership changes can take a few minutes to propagate to all clusters because group membership data is cached.
- IAM and RBAC are **additive**: a project-level `container.admin` overrides your careful RBAC.
- Prefer built-in `view`/`edit`/`admin` ClusterRoles via RoleBinding.

## Verify
- [ ] `kubectl auth can-i --list -n payments --as=<user> --as-group=team-payments@...` shows edit rights only in `payments`.
- [ ] A user in no team group gets `forbidden` on `kubectl get pods -A`.

## Checked

2026-10-24, GKE Google Groups for RBAC and role-based access control pages on docs.cloud.google.com. Confirmed: required `gke-security-groups` parent group, nesting groups and not individual users, `--security-group` on create and update, View Members permission, propagation of a few minutes, `container.clusters.get` in `roles/container.clusterViewer`, the Group subject definition, `google groups` in RBAC DENY audit entries. Removed unconfirmed claims: group visibility wording, `kubectl auth whoami` output claim, authorization decision field names, escalate/bind advice.

Method: documentation only; no commands were run.
