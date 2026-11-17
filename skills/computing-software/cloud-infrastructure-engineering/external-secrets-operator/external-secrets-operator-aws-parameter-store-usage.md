---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-aws-parameter-store-usage
name: external-secrets-operator-aws-parameter-store-usage
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [aws-parameter-store, ssm, gjson, pricing]
level: practitioner
status: docs-checked
description: "Read and push AWS Systems Manager parameters with ESO, extract JSON with gjson, fetch tags and pin parameter versions."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/provider/aws-parameter-store.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `service: ParameterStore`. Fetching needs `ssm:GetParameter*` on the parameter ARN (for example `parameter/dev-*`); pushing adds `ssm:PutParameter*`, `ssm:AddTagsToResource` and `ssm:ListTagsForResource`.

Cost: the API is charged by throughput and tier, and cost depends on your ExternalSecrets' refresh intervals, so estimate before rollout.

A parameter may hold JSON; select nested values with gjson syntax in `property`:

```yaml
data:
- secretKey: my_name
  remoteRef: {key: friendslist, property: name.first}
- secretKey: first_friend
  remoteRef: {key: friendslist, property: friends.1.first}
- secretKey: tags
  remoteRef: {metadataPolicy: Fetch, key: database-credentials}
```

`metadataPolicy: Fetch` returns all tags as JSON, or one tag when `property` names it. Every update creates a new parameter version, selectable through the remoteRef `version` property.

## Checked

2026-11-03. Claims were read against provider/aws-parameter-store.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
