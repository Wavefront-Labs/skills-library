---
id: computing-software.cloud-infrastructure-engineering.external-dns.aws-irsa-and-pod-identity-setup
name: aws-irsa-and-pod-identity-setup
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, irsa-setup, eks-pod-identity, oidc-provider, webidentityerr]
level: advanced
status: docs-checked
description: "Wire ExternalDNS to Route53 on EKS with IRSA (OIDC trust, role-arn annotation) or Pod Identity (agent add-on, association), plus the errors seen when misconfigured."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/tutorials/aws.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IRSA and EKS Pod Identity for ExternalDNS

**IRSA** (preferred; needs a service account and RBAC)
1. Check OIDC: `aws eks describe-cluster --name $CLUSTER --query "cluster.identity.oidc.issuer" --output text`.
2. Associate the provider: `eksctl utils associate-iam-oidc-provider --cluster $CLUSTER --approve`.
3. One-shot: `eksctl create iamserviceaccount --cluster $CLUSTER --name external-dns --namespace $NS --attach-policy-arn $POLICY_ARN --approve`.
4. Manual: role trust uses `sts:AssumeRoleWithWebIdentity` for `arn:aws:iam::$ACCOUNT_ID:oidc-provider/$OIDC_PROVIDER` with conditions `$OIDC_PROVIDER:sub` = `system:serviceaccount:<ns>:external-dns` and `$OIDC_PROVIDER:aud` = `sts.amazonaws.com`. Attach the policy, then annotate the ServiceAccount `eks.amazonaws.com/role-arn: <role arn>`.

On annotation the pod gets `AWS_ROLE_ARN`, `AWS_STS_REGIONAL_ENDPOINTS` and `AWS_WEB_IDENTITY_TOKEN_FILE` injected. Pods created earlier must be deleted to pick them up.

**Errors:** `WebIdentityErr: failed to retrieve credentials` means a wrong namespace in the trust, or the annotation points to the wrong role. `failed to list hosted zones: AccessDenied: User` means ExternalDNS started before the annotation; restart the pod.

Helm: the tutorial's values example sets `env` `AWS_DEFAULT_REGION`; the service account still needs the role annotation.

**EKS Pod Identity** (EKS only; no annotation)
1. Install the add-on: `eksctl create addon --cluster $CLUSTER --name eks-pod-identity-agent` (a DaemonSet on workers).
2. Create a role whose trust principal is Service `pods.eks.amazonaws.com` with actions `sts:AssumeRole` and `sts:TagSession`; attach the policy.
3. `aws eks create-pod-identity-association --cluster-name $CLUSTER --namespace $NS --service-account external-dns --role-arn $ROLE_ARN` (or `eksctl create podidentityassociation`).

The agent injects credentials at runtime. kiam and kube2iam are the alternatives for non-EKS clusters on AWS.

## Checked

2026-11-04. Read the AWS tutorial (IAM Roles for Service Accounts, EKS Pod Identity Associations, Using Helm with OIDC). Confirmed the OIDC check and association commands, eksctl create iamserviceaccount, the trust policy and conditions, the injected environment variables, both error messages, the Pod Identity agent add-on, the pods.eks.amazonaws.com trust and the create-pod-identity-association flags. Replaced the Helm serviceAccount.annotations claim, which the page does not show, with what the Helm example does show.

Method: documentation only; no commands were run.
