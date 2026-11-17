---
id: computing-software.ai-ml-engineering.ml-platform-engineering.notebook-data-access-and-credentials
name: notebook-data-access-and-credentials
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, self-service, notebook-data-access, workload-identity, irsa, short-lived-credentials, data-governance]
level: practitioner
status: draft
description: "Give notebooks and ML jobs data access without long-lived keys: per-user workload identity (IRSA, Pod Identity, GKE), secret managers, scoped roles and audit."
sources:
  - https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html
  - https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html
  - https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity
  - https://z2jh.jupyter.org/en/stable/administrator/security.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data access and credentials for notebooks

**Anti-patterns to remove:** cloud access keys pasted into notebooks or `.env` files, a shared all-powerful service account for every notebook, credentials committed with notebooks to git.

## Identity per user
Map each notebook pod to the **user's** identity so access policies and audit logs name a person:
- **AWS:** IRSA (service account annotated with `eks.amazonaws.com/role-arn`) or EKS Pod Identity associations. One Kubernetes service account per user or per team-role; KubeSpawner sets `service_account` per user via `pre_spawn_hook` or profile override.
- **GCP:** GKE Workload Identity - KSA bound to a GSA (`roles/iam.workloadIdentityUser`), or direct IAM grants to the KSA principal.
- **Azure:** Microsoft Entra Workload ID with federated credentials.
SDKs pick up these short-lived credentials automatically; nothing to paste.

```python
# z2jh hub.extraConfig snippet
async def pre_spawn_hook(spawner):
    team = (await spawner.user.get_auth_state())["oauth_user"]["groups"][0]
    spawner.service_account = f"nb-{team}"            # pre-created, mapped to a team IAM role
c.KubeSpawner.pre_spawn_hook = pre_spawn_hook
```

## Scope
- Read-only roles to curated/feature datasets by default; write only to a per-user or per-project scratch prefix.
- Raw PII datasets via governed access (Lake Formation, Unity Catalog, BigQuery column-level security/policy tags) with approval workflows, not bucket-wide grants.
- Separate dev and prod: notebooks never get production write credentials.

## Secrets that are not cloud IAM
Database passwords, API keys (LLM providers, SaaS): store in a secret manager (AWS Secrets Manager, GCP Secret Manager, Vault) and fetch at runtime with the workload identity; or mount via External Secrets Operator / CSI driver. Rotate regularly.

## Hygiene
- `nbstripout` pre-commit hook strips outputs (which often contain data samples and tokens) before commits; secret scanning on repos.
- Disable or restrict notebook terminals and outbound internet where data sensitivity requires; egress via proxy.
- Audit: CloudTrail/Cloud Audit Logs show which user identity read which dataset.

## Verify
- [ ] `aws sts get-caller-identity` (or `gcloud auth list`) inside a notebook shows the expected per-user/team role, with no static keys in env or files.
- [ ] Attempt to read a dataset outside scope fails with access denied and appears in audit logs.
- [ ] Repo scan finds no credentials or notebook outputs with data.
