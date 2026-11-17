---
id: computing-software.devops-ci-cd.gitlab-ci.kubernetes-agent-user-access-and-dashboard
name: kubernetes-agent-user-access-and-dashboard
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, user-access, kubernetes-dashboard, gitlab-agent, kubeconfig, impersonation]
level: practitioner
status: docs-checked
description: "Give developers kubectl and the GitLab Kubernetes dashboard access to clusters through the agent user_access config, kubeconfig via glab, and impersonation RBAC."
sources: ["https://docs.gitlab.com/user/clusters/agent/user_access/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Agent for Kubernetes: user access and dashboard

**Goal:** people (not only CI jobs) reach the cluster through GitLab authentication, with RBAC.

## Authorise (agent config.yaml)
```yaml
user_access:
  access_as:
    agent: {}            # or user: {} to impersonate the GitLab user (Premium and Ultimate)
  projects:
    - id: path/to/project
  groups:
    - id: path/to/group
```
- Members of the listed projects/groups (descendant groups included) get access; you need the Developer role or higher to configure it. Up to 500 projects and 500 groups.
- Projects/groups must share the top-level namespace of the agent's configuration project unless instance-level authorisation is enabled.
- Granting access also enables the **Dashboard for Kubernetes** for those projects/groups.
- The default access type is agent identity since GitLab 18.3; check your version.

## Get a kubeconfig
```bash
glab cluster agent update-kubeconfig --repo 'group/project' --agent '<agent-id>' --use-context
kubectl get nodes
```
The kubeconfig calls `glab cluster agent get-token`, which issues a short-lived (same-day) personal access token. Manual alternative: a PAT with `k8s_proxy` scope against the KAS `/k8s-proxy` endpoint, user token `pat:<agent-id>:<token>`.

## Impersonation RBAC (`access_as: user`)
Username `gitlab:user:<username>`; groups `gitlab:user`, `gitlab:project_role:<project_id>:<role>`, `gitlab:group_role:<group_id>:<role>`. Bind them:
```yaml
subjects: [{kind: Group, name: "gitlab:project_role:123:maintainer", apiGroup: rbac.authorization.k8s.io}]
roleRef: {kind: ClusterRole, name: view, apiGroup: rbac.authorization.k8s.io}
```
Only directly listed projects/groups are impersonated, not parents. Impersonated requests need a ClusterRoleBinding or RoleBinding to get any permissions in the cluster.

## Verify
`kubectl get nodes` as an authorised and as an unauthorised user; the dashboard lists workloads for an authorised user and nothing for others.

## Checked

2026-11-02. Confirmed: `user_access` keys `access_as`, `projects`, `groups`; 500 project and 500 group limits; descendants included; same top-level namespace requirement; Dashboard activation; Developer role; `access_as` optional and defaults to agent identity since 18.3; `update-kubeconfig` / `get-token` (token valid to end of the day); `k8s_proxy` PAT scope and `pat:<agent-id>:<token>`; impersonation names and role groups; only directly listed projects impersonated; RBAC binding needed (GitLab Kubernetes agent user access docs). Removed: `glab cluster agent list`, kubectl auth commands.

Method: documentation only; no commands were run.
