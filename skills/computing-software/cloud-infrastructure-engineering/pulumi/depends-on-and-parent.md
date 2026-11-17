---
id: computing-software.cloud-infrastructure-engineering.pulumi.depends-on-and-parent
name: depends-on-and-parent
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, depends-on, dependson, parent-option, dependency-graph]
level: practitioner
status: docs-checked
description: "Control Pulumi ordering with dependsOn and parent, and understand implicit dependencies from outputs and the options a child inherits from its parent."
sources:
  - https://www.pulumi.com/docs/iac/concepts/resources/options/dependson/
  - https://www.pulumi.com/docs/iac/concepts/resources/options/parent/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dependsOn and parent

Pulumi tracks dependencies automatically when one resource's input is another's output. Add `dependsOn` only for dependencies Pulumi cannot see (an ordering or eventual-consistency requirement, e.g. an IAM policy attached before a service starts).

```typescript
const policy = new aws.iam.RolePolicy("p", { role: role.id, policy: doc });
const fn = new aws.lambda.Function("f", { role: role.arn, /* ... */ },
  { dependsOn: [policy] });
const obj = new aws.s3.BucketObject("o", { bucket: b.id }, { parent: comp });
```
```python
fn = aws.lambda_.Function("f", role=role.arn, opts=pulumi.ResourceOptions(depends_on=[policy]))
```

`parent` shows the parent/child hierarchy in CLI output and makes the child inherit options from its parent. The parent page lists them as `provider`, `aliases`, `protect`, `retainOnDelete` and `deletedWith` (a child can set the option itself to override). By default a resource's parent is the root `pulumi:pulumi:Stack` resource; resources inside a component should be parented to the component.

## Gotchas
- Changing a resource's `parent` changes its URN, which looks like delete+create; add an alias (see aliases-for-refactoring).
- `dependsOn` orders create, update and delete operations; it is for hidden dependencies, so pass an output as an input when you can.

## Verify
`pulumi stack --show-urns` lists each resource's URN; a parented resource's URN carries the parent type before a `$`, as in the `pulumi state rename` reference example.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the dependsOn and parent resource option pages (explicit vs automatic dependencies, inherited option list, default root stack parent), the `pulumi stack` CLI reference (`--show-urns`) and the `pulumi state rename` reference (URN example with `$`). Removed: the unconfirmed claims that dependsOn on a component waits for all children, that cycles fail with a graph error, and that preview shows creation order top to bottom.
Method: documentation only; no commands were run.
