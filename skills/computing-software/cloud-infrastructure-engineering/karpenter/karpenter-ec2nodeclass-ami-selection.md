---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-ec2nodeclass-ami-selection
name: karpenter-ec2nodeclass-ami-selection
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [amiselectorterms, alias, ami, ssmparameter, owner, latest, pinning, bottlerocket, al2023]
level: advanced
status: docs-checked
description: "amiSelectorTerms options: alias family@version pinning, id, name, owner, tags, ssmParameter, multiple-AMI choice rules, listing versions with SSM, and why latest is risky."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeclasses.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EC2NodeClass amiSelectorTerms

`amiSelectorTerms` is required. Terms are ORed, conditions in a term ANDed.

```yaml
amiSelectorTerms:
  - alias: al2023@v20240807      # exclusive: cannot combine with other terms
  # - tags: {karpenter.sh/discovery: "${CLUSTER_NAME}"}
  # - name: my-ami
  #   owner: self
  # - id: ami-123
  # - ssmParameter: my-custom-parameter   # name or ARN
```

Alias is `family@version`, family one of `al2`, `al2023`, `bottlerocket`, `windows2019`, `windows2022`, `windows2025`. Version is `latest` or a pin: dates for AL2/AL2023 (`al2023@v20240703`), semver for Bottlerocket (`bottlerocket@v1.20.4`); Windows only supports `latest`. List versions:

```bash
aws ssm get-parameters-by-path --path "/aws/service/eks/optimized-ami/$K8S_VERSION/amazon-linux-2023/" --recursive | jq -cr '.Parameters[].Name' | grep -v recommended
```

Rules:
- `owner` defaults to `self,amazon` for name selection; accounts and aliases allowed. Tags need no owner.
- If several AMIs match, Karpenter picks by architecture compatibility and takes the latest. Except with an alias, it cannot detect other requirements (such as GPU), so use a separate EC2NodeClass for those.
- No usable AMI means no nodes.
- Custom `ssmParameter` needs `ssm:GetParameter` added to the Karpenter IAM role.

Warning: `latest` makes every new AMI release drift all nodes; avoid it in production and test AMIs in a lower environment first. `status.amis` shows resolved ids and a `deprecated` flag.

## Checked

2026-11-04. Confirmed against the NodeClasses concept page (v1.13) (identifiers, defaults, limits and prose). Nothing material removed.

Method: documentation only; no commands were run.
