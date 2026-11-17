---
id: computing-software.cloud-infrastructure-engineering.pulumi.stack-references
name: stack-references
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, stack-reference, cross-stack, stack-outputs, getoutput]
level: practitioner
status: docs-checked
description: "Read another Pulumi stack's exported outputs with StackReference, using fully qualified stack names, in TypeScript and Python."
sources:
  - https://www.pulumi.com/docs/iac/concepts/stacks/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_stack_output/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stack references

Export values from one stack, read them from another.

```typescript
// producer stack
export const vpcId = vpc.id;

// consumer stack
const infra = new pulumi.StackReference("myorg/network/prod");
const vpcId = infra.getOutput("vpcId");   // Output<any>
```
```python
infra = pulumi.StackReference("myorg/network/prod")
vpc_id = infra.get_output("vpcId")
```

The name is fully qualified: `<organization>/<project>/<stack>`. On a DIY backend the organization is always the constant `organization`.

Inspect from the CLI:
```bash
pulumi stack output vpcId --stack myorg/network/prod
```

## Gotchas
- Only values the producer exports (`export const` / `pulumi.export`) can be read; the producer stack must have been updated at least once with that export.
- `getOutput` / `get_output` returns an `Output`, so use `apply` or `interpolate` to build strings from it.

## Verify
`pulumi stack output --stack <org>/<project>/<stack>` on the producer lists the exports the consumer can read.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the Stacks page "Stack references" section (fully qualified name, DIY `organization`, `getOutput` / `get_output`, exports) and the `pulumi stack output` reference (`--stack`). Removed: `requireOutput` / `require_output`, and the unconfirmed claims about secrets staying secret, deployment ordering and rename behaviour.
Method: documentation only; no commands were run.
