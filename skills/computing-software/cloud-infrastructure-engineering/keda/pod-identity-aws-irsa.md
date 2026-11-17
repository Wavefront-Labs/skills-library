---
id: computing-software.cloud-infrastructure-engineering.keda.pod-identity-aws-irsa
name: pod-identity-aws-irsa
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [aws-pod-identity, irsa, rolearn, identityowner, aws-eks, podidentity]
level: advanced
status: docs-checked
description: "Use the aws podIdentity provider with roleArn and identityOwner for IAM Roles for Service Accounts, and know that aws-eks is deprecated."
sources:
  - https://keda.sh/docs/2.17/concepts/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The podIdentity block lists the providers KEDA supports:

```yaml
podIdentity:
  provider: none | azure-workload | aws | aws-eks | gcp
  identityId: <identity-id>
  roleArn: <role-arn>
  identityOwner: keda|workload
```

The default provider is `none`. `identityId` is only used by Azure providers; `roleArn` and `identityOwner` are only used by the `aws` provider.

The `aws` provider relies on the AWS IAM Roles for Service Accounts pod identity webhook, which supplies the role name through an annotation on the service account associated with the pod:

```yaml
podIdentity:
  provider: aws
  roleArn: <role-arn>
  identityOwner: keda|workload
```

Both `roleArn` and `identityOwner` are optional. The page does not spell out the semantics of `identityOwner` in this section beyond the two allowed values `keda` and `workload`; consult the AWS authentication provider page for the exact behaviour before relying on it.

The older `aws-eks` provider is marked deprecated and will be removed in KEDA v3, so plan to move off `provider: aws-eks`; `aws` is the IRSA provider.

## Checked

2026-11-03. Confirmed on the 2.17 Authentication page: podIdentity fields, aws provider, aws-eks deprecated and removed in v3. Removed: a migration instruction the page does not give.

Method: documentation only; no commands were run.
