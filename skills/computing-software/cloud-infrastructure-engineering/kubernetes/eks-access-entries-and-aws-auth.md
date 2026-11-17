---
id: computing-software.cloud-infrastructure-engineering.kubernetes.eks-access-entries-and-aws-auth
name: eks-access-entries-and-aws-auth
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, authentication, eks-access-entries, aws-auth-configmap, aks-entra-id, eks, managed-kubernetes]
level: practitioner
status: docs-checked
description: "Manage human and CI access to EKS with access entries and access policies, migrate from the aws-auth ConfigMap, and compare with AKS Entra ID auth."
sources: ["https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html", "https://docs.aws.amazon.com/eks/latest/userguide/setting-up-access-entries.html", "https://docs.aws.amazon.com/eks/latest/userguide/creating-access-entries.html", "https://docs.aws.amazon.com/eks/latest/userguide/access-policies.html", "https://docs.aws.amazon.com/eks/latest/userguide/migrating-access-entries.html", "https://docs.aws.amazon.com/eks/latest/userguide/auth-configmap.html", "https://eksctl.io/usage/access-entries/", "https://learn.microsoft.com/en-us/azure/aks/entra-id-authorization", "https://learn.microsoft.com/en-us/azure/aks/local-accounts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EKS access entries (and AKS Entra ID)

## Authentication modes
`CONFIG_MAP` (legacy aws-auth only), `API_AND_CONFIG_MAP` (both), `API` (access entries only).
Once a mode with the EKS API is enabled you can't change back to a mode without it.
```bash
aws eks update-cluster-config --name prod --access-config authenticationMode=API_AND_CONFIG_MAP
```
In `API_AND_CONFIG_MAP`, an access entry takes precedence over an aws-auth mapping for the same
IAM principal.

## Access entries
```bash
aws eks create-access-entry --cluster-name prod \
  --principal-arn arn:aws:iam::111122223333:role/platform-admins
aws eks associate-access-policy --cluster-name prod \
  --principal-arn arn:aws:iam::111122223333:role/platform-admins \
  --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy \
  --access-scope type=cluster
# namespace-scoped:
aws eks associate-access-policy ... --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSEditPolicy \
  --access-scope type=namespace,namespaces=team-a
```
Or map to Kubernetes groups and use your own RBAC:
`create-access-entry ... --type STANDARD --kubernetes-groups team-a-devs`. EKS does not check
that RoleBindings for those groups exist; the principal has no permissions until they do.

## Legacy aws-auth
```yaml
mapRoles: |
  - rolearn: arn:aws:iam::111122223333:role/ci-deployer
    username: ci-deployer
    groups: [ci-deployers]
```
Role ARNs in aws-auth can't include a path. Access policies can't be attached to aws-auth
entries. Migrate each mapping you created to an access entry with the same ARN, username and
groups (`eksctl get iamidentitymapping` lists them), switch to API mode, then remove the
mappings.

## Gotchas
- You can't change an access entry's IAM principal or type after creating it.
- The cluster creator's implicit admin can be turned off with
  `bootstrapClusterCreatorAdminPermissions: false` at create time (eksctl `accessConfig`);
  make sure another admin entry exists.
- Self-managed Linux node roles need an access entry of type `EC2_LINUX` (creating it needs
  `iam:PassRole`). Managed node groups and Fargate profiles get their entries from EKS; don't
  remove EKS-created aws-auth entries for them unless the equivalent access entries exist.

## AKS equivalent
Entra ID integration plus Azure RBAC (`--enable-azure-rbac`): role assignments such as
"Azure Kubernetes Service RBAC Cluster Admin" scoped to the cluster, or RBAC Reader/Writer
scoped to a namespace. Local accounts are enabled by default even with Entra integration;
disable them (`--disable-local-accounts`) so the `--admin` credentials cannot be used.

## Verify
```bash
aws eks list-access-entries --cluster-name prod
kubectl auth whoami
```

## Checked
Checked 2026-10-27 against the Amazon EKS User Guide source (awsdocs/amazon-eks-user-guide:
setting up access entries, creating access entries, access policies, migrating from aws-auth,
aws-auth ConfigMap), the eksctl access entries page and MicrosoftDocs/azure-aks-docs (Entra ID
authorization roles, local accounts): authentication modes and the one-way switch, access-entry
precedence, `--access-scope type=namespace,namespaces=...`, policy ARNs, immutable principal and
type, `EC2_LINUX` and `iam:PassRole`, automatic entries for managed node groups and Fargate,
no path in aws-auth role ARNs, AKS RBAC role names and local accounts. Removed the unconfirmed
"malformed aws-auth locks everyone out" and "assumed-role session ARN" claims.

Method: documentation only; no commands were run.
