---
id: computing-software.cybersecurity-defensive.cloud-security.eks-irsa-pod-identity
name: eks-irsa-pod-identity
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [irsa, eks-pod-identity, eks, kubernetes-service-accounts, workload-identity, oidc-provider, cloud-iam]
level: practitioner
status: docs-checked
description: "Give EKS pods least-privilege AWS access with IRSA or EKS Pod Identity instead of the node role: how each works, trust principal, associations, and hostNetwork caveat."
sources: ["https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html", "https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html", "https://docs.aws.amazon.com/eks/latest/userguide/pod-id-association.html", "https://docs.aws.amazon.com/eks/latest/userguide/pod-id-agent-setup.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EKS IRSA and Pod Identity

Goal: pods get their own narrowly scoped IAM role instead of sharing the node instance role.
Both mechanisms give credentials to the AWS SDKs and CLI in the pod.

## IRSA (IAM Roles for Service Accounts)
- Needs an IAM OIDC provider for the cluster, created once per cluster.
- Kubernetes issues a service account token (JWT) that IAM validates against the cluster's EKS-hosted
  OIDC discovery endpoint; the pod exchanges it with STS `AssumeRoleWithWebIdentity` for temporary credentials.
- In a VPC with no outbound internet, reaching the OIDC endpoint (for example when creating the provider
  with eksctl) needs a VPC interface endpoint for `oidc-eks` with private DNS.

## EKS Pod Identity (simpler)
- Does not use OIDC identity providers; configuration of associations lives in EKS and permissions in IAM,
  so cluster admins and IAM admins can work independently.
- Requires the EKS Pod Identity Agent add-on: a DaemonSet that serves credentials only to pods on the same
  node, using the node's hostNetwork, ports 80 and 2703 on link-local 169.254.170.23 (IPv4).
  The agent needs its permissions in the node role.
- Role trust policy principal is the service `pods.eks.amazonaws.com`, with actions `sts:AssumeRole`
  and `sts:TagSession`.
- Associate a role with a namespace and service account:
  `aws eks create-pod-identity-association --cluster-name <CLUSTER> --role-arn <ROLE_ARN> --namespace <NAMESPACE> --service-account <SERVICE_ACCOUNT>`
- Pod Identity adds default session tags when it assumes the role (they can be disabled per association,
  and a session policy can be applied only when session tags are disabled).

## Fallback to the node role
Pods with `hostNetwork: true` always have IMDS access, although the SDKs and CLI use IRSA or Pod Identity
credentials when those are configured. Keep the node role minimal.

## Gotchas
- Old SDK versions may not support the web identity or Pod Identity credential providers; check the
  docs' SDK version lists.

## Verify
- [ ] The pod's SDK calls run as the intended role (check the role in CloudTrail).
- [ ] An unrelated pod cannot assume the role.

## Checked
2026-11-01. Confirmed on the EKS User Guide pages for IRSA, Pod Identity, Pod Identity associations and the
Pod Identity Agent: OIDC provider requirement, AssumeRoleWithWebIdentity flow, private OIDC endpoint note,
Pod Identity benefits, agent DaemonSet ports and address, trust principal and actions, association command
(passes the CLI model check), session tags, hostNetwork IMDS note. Removed (not stated on those pages): the
IRSA trust-policy JSON and condition keys, eksctl command, service account annotation, IMDS hop limit setting,
Kyverno/Gatekeeper policy, the wildcard trust gotcha and the SDK-support statement as a fact.
Method: documentation only; no commands were run.
