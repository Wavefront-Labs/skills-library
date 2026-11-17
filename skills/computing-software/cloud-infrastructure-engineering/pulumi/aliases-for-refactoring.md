---
id: computing-software.cloud-infrastructure-engineering.pulumi.aliases-for-refactoring
name: aliases-for-refactoring
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, aliases, rename-resource, refactor-urn, alias-option]
level: practitioner
status: docs-checked
description: "Rename or re-parent Pulumi resources without replacing them using the aliases resource option, plus component and type aliases."
sources:
  - https://www.pulumi.com/docs/iac/concepts/resources/options/aliases/
  - https://www.pulumi.com/docs/iac/operations/stack-management/refactoring-with-aliases/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_state_rename/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Aliases for refactoring

A resource's identity is its URN, which encodes the name, type and parent path. Changing the name, parent, or type looks like delete+create unless you alias the old identity.

```typescript
// renamed "web-bucket" -> "site-bucket"
new aws.s3.Bucket("site-bucket", {}, { aliases: [{ name: "web-bucket" }] });
// moved under a component
new aws.s3.Bucket("site-bucket", {}, { parent: comp, aliases: [{ parent: pulumi.rootStackResource }] });
// changed type token
{ aliases: [{ type: "aws:rds/database:Database" }] }
```
```python
opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(name="web-bucket")])
```

## Gotchas
- Wrapping existing resources in a new component changes every child's parent: alias each child with `parent: pulumi.rootStackResource` (or its old parent).
- Aliases are inherited from a parent, so if a component is renamed or re-parented you do not repeat the alias on each child.
- An alias is only needed until every stack of the project has run `pulumi up` (or another operation that writes state) with it in place; removing it earlier replaces the resource in stacks that missed the rename.
- Alternative that edits state instead of code: `pulumi state rename [resource-urn] [new-name]`.

## Verify
`pulumi preview --diff` shows the renamed resource updated in place or unchanged, never a `+-` replace.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the aliases resource option page (name/type/parent aliases, in-place update, `Alias(name=...)`), the "Refactoring with aliases" operations page (`pulumi.rootStackResource`, `{ type: ... }`, inheritance, when an alias can be removed), the parent option page (aliases inherited) and the `pulumi state rename` CLI reference. Removed the invented type token `aws:s3/bucketV2:BucketV2` and the unconfirmed `~ update (alias)` preview text.
Method: documentation only; no commands were run.
