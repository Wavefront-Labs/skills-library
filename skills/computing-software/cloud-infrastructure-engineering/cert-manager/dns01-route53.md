---
id: computing-software.cloud-infrastructure-engineering.cert-manager.dns01-route53
name: dns01-route53
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [route53, aws, dns01, irsa, pod-identity, ambient-credentials, assume-role]
level: advanced
status: docs-checked
description: "Configure cert-manager DNS01 with AWS Route 53: least-privilege IAM, ambient credentials via IRSA or Pod Identity, access keys, cross-account roles and region."
sources:
  - https://cert-manager.io/docs/configuration/acme/dns01/route53/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
IAM policy: `route53:GetChange` on `arn:aws:route53:::change/*`; `route53:ChangeResourceRecordSets` and `route53:ListResourceRecordSets` on `arn:aws:route53:::hostedzone/*` with `ForAllValues:StringEquals` on `route53:ChangeResourceRecordSetsRecordTypes` = `TXT`; `route53:ListHostedZonesByName` on `*` (unneeded if `hostedZoneID` is set).

Ambient credentials: set `route53: {}`. Sources include EKS Pod Identity, IRSA, EC2 IMDS, `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` and shared config files. By default ambient credentials apply only to ClusterIssuer; for Issuer add `--issuer-ambient-credentials=true` (not recommended).
- Pod Identity: associate the role with the cert-manager ServiceAccount and restart the Deployment.
- IRSA: trust policy with `sts:AssumeRoleWithWebIdentity` and condition `oidc.eks.<region>.amazonaws.com/id/<hash>:sub` = `system:serviceaccount:<ns>:<sa>`; annotate the SA `eks.amazonaws.com/role-arn` (Helm `serviceAccount.annotations`); restart the Deployment. `runAsUser`/`fsGroup: 1001` is only a workaround for token "permission denied" on older EKS or Fargate.

Per-Issuer credentials: either a dedicated ServiceAccount (`role` required, `auth.kubernetes.serviceAccountRef.name`, plus a Role allowing `create` on `serviceaccounts/token` for that name), or `accessKeyIDSecretRef` and `secretAccessKeySecretRef` (`name`, `key`) with an optional `role`. ClusterIssuer Secrets belong in `cert-manager` or `--cluster-resource-namespace`.

Cross-account: account Y holds the zone role trusting account X's cert-manager role for `sts:AssumeRole`.

If `region` is omitted, cert-manager reads the `AWS_REGION` and `AWS_DEFAULT_REGION` environment variables; for ambient credentials the env vars win; the field is ignored under Pod Identity and IRSA.

## Checked

2026-11-03. Confirmed on the cert-manager Route53 page (configuration/acme/dns01/route53): IAM policy statements, ambient credential sources and Issuer default, Pod Identity and IRSA steps, trust policy condition, 1001 workaround note, dedicated ServiceAccount RBAC, access key Secrets and role, cross-account roles, region rules. Reworded: the page does not state an order between AWS_REGION and AWS_DEFAULT_REGION.
Method: documentation only; no commands were run.
