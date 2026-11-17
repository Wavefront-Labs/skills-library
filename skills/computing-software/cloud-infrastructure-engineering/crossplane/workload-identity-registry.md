---
id: computing-software.cloud-infrastructure-engineering.crossplane.workload-identity-registry
name: workload-identity-registry
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [workload-identity, irsa, ecr, aks, gke, package-manager]
level: advanced
status: docs-checked
description: "Let the Crossplane package manager pull from private cloud registries using workload identity annotations on its service account."
sources:
  - https://docs.crossplane.io/latest/guides/crossplane-with-workload-identity/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pulling a package has two steps: the package manager extracts the package (this guide), then Kubernetes nodes pull runtime images (node permissions, such as ECR pull on the node role, AcrPull for the AKS kubelet identity, Artifact Registry reader for GKE). Without node access, pods fail with `ImagePullBackOff`.

Configure the `crossplane` service account via Helm at install.

AWS EKS (IRSA): enable the OIDC provider (`eksctl utils associate-iam-oidc-provider --cluster=<CLUSTER_NAME> --approve`), create an IAM role whose trust policy allows `system:serviceaccount:crossplane-system:crossplane` with `sts:AssumeRoleWithWebIdentity`, give it `ecr:GetAuthorizationToken`, `ecr:BatchCheckLayerAvailability`, `ecr:GetDownloadUrlForLayer` and `ecr:BatchGetImage`, then:

```shell
helm upgrade --install crossplane crossplane-stable/crossplane \
  --namespace crossplane-system --create-namespace \
  --set "serviceAccount.customAnnotations.eks\.amazonaws\.com/role-arn=arn:aws:iam::${AWS_ACCOUNT_ID}:role/CrossplaneECRRole"
```

Azure AKS: enable workload identity on the cluster, then set annotations `azure.workload.identity/client-id` and `azure.workload.identity/tenant-id` plus `--set-string 'customLabels.azure\.workload\.identity/use=true'`.

Verify with `kubectl get sa crossplane -n crossplane-system -o yaml`. Common errors: `AccessDeniedException` (check IAM permission and trust policy) and `InvalidIdentityToken` (check the OIDC provider and the service account name in the condition).

## Checked

Two-step pull model, node permissions, EKS OIDC and IAM steps, Helm annotation, AKS annotations and label, verification command and both error causes confirmed on the guide. The guide also covers GKE (annotation `iam.gke.io/gcp-service-account`), which this skill omits.

Method: docs-checked 2026-11-09 against the raw Crossplane with Workload Identity guide (docs repo, current content folder), read in full.
