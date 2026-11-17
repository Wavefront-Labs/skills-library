---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-aws-assume-role
name: external-secrets-operator-aws-assume-role
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [aws, assumerole, externalid, cross-account]
level: advanced
status: docs-checked
description: "Scope an ESO AWS store with role, additionalRoles for cross-account chaining and externalID."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/provider/aws-access.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The optional `spec.provider.aws.role` makes ESO call `sts:AssumeRole` before reading secrets and is the recommended way to scope access per store, so users of the store can only access the secrets that role allows.

```yaml
spec:
  provider:
    aws:
      service: SecretsManager
      region: eu-central-1
      role: arn:aws:iam::222222222222:role/team-b
      additionalRoles:
        - arn:aws:iam::111111111111:role/hop
      externalID: my-external-id
```

- `additionalRoles`: a chained list of role ARNs assumed in order before `role`, for cross-account hops.
- `externalID`: passed when assuming `role` for third-party trust policies.

For EKS Pod Identity Agent, the docs show creating an IAM role whose trust policy allows the `pods.eks.amazonaws.com` service principal.

## Checked

2026-11-03. Claims were read against provider/aws-access.md in the external-secrets docs source. Removed: an unsupported statement about trust policies of the base identity.

Method: documentation only; no commands were run.
