---
id: computing-software.cloud-infrastructure-engineering.external-dns.aws-route53-iam-and-credentials
name: aws-route53-iam-and-credentials
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, aws-provider, route53-iam-policy, irsa, aws-profile, abac-policy]
level: practitioner
status: docs-checked
description: "Route53 IAM policy for ExternalDNS (plain and ABAC), credential method hierarchy (IRSA, Pod Identity, node role, static) and multi-profile support."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/tutorials/aws.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS: IAM policy and credentials

**Minimum policy:** on `arn:aws:route53:::hostedzone/*` allow `route53:ChangeResourceRecordSets`, `route53:ListResourceRecordSets`, `route53:ListTagsForResources`; on `*` allow `route53:ListHostedZones`. Replace `*` with an explicit zone list to cut the blast radius.

**ABAC variant:** add a `Condition` with `ForAllValues:StringLike` on `route53:ChangeResourceRecordSetsNormalizedRecordNames` (for example `*example.com`, `marketing.example.com`), `route53:ChangeResourceRecordSetsActions` (`CREATE`, `UPSERT`, `DELETE`) and `route53:ChangeResourceRecordSetsRecordTypes` (`A`, `AAAA`, `CNAME`, `MX`, `TXT`).

**Credential hierarchy (docs, best first)**
1. IRSA: map an IAM role to the Kubernetes service account, no static credentials in the pod.
2. EKS Pod Identity: native alternative to IRSA through the Pod Identity Agent.
3. Node IAM role: every pod on the node inherits Route53 write access, so test environments only. Detach the policy (`aws iam detach-role-policy`) before deleting the cluster or role deletion fails.
4. Mounted credentials file, then 5. environment variables: minimise privileges, avoid long-lived keys.

Static credentials leak through `kubectl describe pod`, `exec` plus `env`, logs and crash dumps, and are hard to rotate. Use them mainly for non-AWS clusters.

Credentials resolve through the AWS SDK for Go v2 default chain, so env vars, shared files, instance profile, ECS credentials and Pod Identity all work without extra config.

**Profiles:** default profile is `default`. Choose with `EXTERNAL_DNS_AWS_PROFILE` or `--aws-profile`. Several profiles (space separated, or the flag repeated) make ExternalDNS look for zones in all of them and keep a zone-to-profile map.

Create the policy: `aws iam create-policy --policy-name AllowExternalDNSUpdates --policy-document file://policy.json`.

## Checked

2026-11-04. Read the AWS tutorial (IAM Policy, ABAC, Further improvements, Static credentials, Node IAM Role, credential chain note, profile tips). Confirmed the policy actions and resources, the three ABAC condition keys and values, the five-step credential hierarchy, the Node role detach warning, the static credential risks, the SDK default chain note and the multi-profile behaviour. Removed nothing.

Method: documentation only; no commands were run.
