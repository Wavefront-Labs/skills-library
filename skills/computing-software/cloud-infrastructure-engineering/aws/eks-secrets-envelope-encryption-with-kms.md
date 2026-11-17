---
id: computing-software.cloud-infrastructure-engineering.aws.eks-secrets-envelope-encryption-with-kms
name: eks-secrets-envelope-encryption-with-kms
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, eks, secrets-encryption-eks, kms-envelope-secrets, kubernetes-secrets, kms]
level: advanced
status: docs-checked
description: "Encrypt Kubernetes secrets in EKS with a customer managed KMS key (envelope encryption), re-encrypt existing secrets, and protect the key from deletion."
sources: ["https://docs.aws.amazon.com/eks/latest/userguide/enable-kms.html", "https://docs.aws.amazon.com/eks/latest/userguide/envelope-encryption.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Envelope encryption of Kubernetes secrets with KMS

## 1. What you get
Clusters on Kubernetes 1.28 or higher envelope-encrypt all Kubernetes API data by default with an AWS owned
key. Supplying your own KMS key makes that key the KEK, so you control the key policy and can see usage.
The `resources` field of the encryption config is deprecated and has no effect on scope (if set it must be `["secrets"]`).

## 2. Enable on an existing cluster
```bash
aws eks associate-encryption-config --cluster-name prod \
  --encryption-config '[{"resources":["secrets"],"provider":{"keyArn":"arn:aws:kms:<REGION>:<ACCOUNT_ID>:key/<KEY_ID>"}}]'
aws eks describe-update --name prod --update-id <UPDATE_ID>
```
- The key must be symmetric, able to encrypt and decrypt, and in the same Region as the cluster.
- The principal that calls create-cluster needs `kms:DescribeKey` and `kms:CreateGrant` on the key.
- Secrets encryption **cannot be disabled** after you enable it (irreversible). The older enable-on-existing-cluster
  procedure is deprecated and documented only for Kubernetes 1.27 or lower.
- The same key can be reused for several clusters in the same Region, but disabling it then degrades all of them.

## 3. Existing data
On 1.28 and higher EKS migrates previously unencrypted data itself (RBAC ClusterRole `eks:kms-storage-migrator`);
no manual re-write of secrets is needed. For 1.27 or lower, `eksctl utils enable-secrets-encryption` re-encrypts
existing secrets by default (`--encrypt-existing-secrets=false` opts out).

## 4. Protect the key
- Disabling the key puts the cluster in an unhealthy/degraded state; re-enable it within 30 days. Deleting the key
  degrades the cluster beyond recovery, as does a missing key (`KMS_KEY_NOT_FOUND`) or revoked grants (`KMS_GRANT_REVOKED`).
- Limit who can disable or delete the key with least-privilege IAM policies and set a CloudWatch alarm on the key state.

## Verify
- [ ] `aws eks describe-cluster --name prod --query cluster.encryptionConfig` shows the key.
- [ ] The cluster stays healthy and the key state is `Enabled`.

## Checked
2026-10-28: Confirmed against EKS User Guide enable-kms and envelope-encryption pages: default envelope encryption on 1.28+ (resources field deprecated and must be ["secrets"] if set), symmetric same-Region key, kms:DescribeKey and kms:CreateGrant for the create-cluster principal, irreversibility, automatic migration (eks:kms-storage-migrator), eksctl re-encrypt flag, disabled/deleted key behaviour and the 30-day window. Read end to end. Error fixed: the old kubectl replace re-encryption step and the claim that only secrets are encrypted by default. Removed: kms:Encrypt/Decrypt requirement, key rotation advice (not on these pages), CloudTrail Decrypt check, the --encryption-config create flag.

Method: documentation only; no commands were run.
