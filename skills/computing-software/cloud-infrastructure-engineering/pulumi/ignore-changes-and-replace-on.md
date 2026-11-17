---
id: computing-software.cloud-infrastructure-engineering.pulumi.ignore-changes-and-replace-on
name: ignore-changes-and-replace-on
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, ignore-changes, replace-on-changes, delete-before-replace, resource-options]
level: practitioner
status: docs-checked
description: "Use ignoreChanges, replaceOnChanges and deleteBeforeReplace to tune how Pulumi diffs and replaces resources; property paths and gotchas."
sources:
  - https://www.pulumi.com/docs/iac/concepts/resources/options/ignorechanges/
  - https://www.pulumi.com/docs/iac/concepts/resources/options/replaceonchanges/
  - https://www.pulumi.com/docs/iac/concepts/resources/options/deletebeforereplace/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ignoreChanges, replaceOnChanges, deleteBeforeReplace

```typescript
new aws.autoscaling.Group("asg", { desiredCapacity: 2 /* ... */ },
  { ignoreChanges: ["desiredCapacity"] });            // autoscaler owns it
new aws.ecs.Service("svc", { /* ... */ },
  { ignoreChanges: ["taskDefinition", "tags.updatedAt"] });
new k8s.apiextensions.CustomResource("widget", { /* ... */ },
  { replaceOnChanges: ["spec.input"] });
new aws.ec2.SecurityGroup("sg", { /* ... */ }, { deleteBeforeReplace: true });
```
```python
opts = pulumi.ResourceOptions(replace_on_changes=["spec.input"])
```

- `ignoreChanges`: Pulumi uses the old value from state instead of the program value when deciding whether to update or replace. The program value is still used when there is no previous value in state (most commonly on create). It applies to inputs only, not outputs. Nested paths and array elements are allowed (see the property paths reference).
- `replaceOnChanges`: replace (not update) when listed paths change, for cases where the provider does not know a property needs replacement. The `*` wildcard can be used in any part of a path; `["*"]` means any property change.
- `deleteBeforeReplace`: delete the old resource first. By default Pulumi creates the replacement before deleting the old one to minimise downtime. Use it for resources that cannot exist side by side; it can cascade to dependents and cause more replacements and downtime.

## Gotchas
- `replaceOnChanges` paths should be the camelCase property names used by the core Pulumi resource model (HCL uses provider snake_case attribute names).
- After `ignoreChanges` is set, Pulumi keeps sending the state value on updates. Run `pulumi refresh` (or `pulumi up --refresh`) so state matches the live resource; skipping it can overwrite changes made by the external system.
- With `replaceOnChanges: ["*"]`, a resource left with initialization errors is replaced instead of updated.
- Eventual consistency in cloud APIs can corrupt dependent resources with `deleteBeforeReplace` if deletion has not fully propagated before creation starts.

## Verify
Change the ignored value in the program and run `pulumi preview --diff`; the resource should show no change.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the ignoreChanges, replaceOnChanges and deleteBeforeReplace option pages (state-value semantics, `["spec.input"]` and `replace_on_changes`, `*` wildcard, camelCase note, refresh warning, cascade and eventual-consistency warnings). Removed: the unconfirmed claims that wrong names are silently ignored and that Python uses snake_case in `ignoreChanges`, and the `aws.s3.Bucket` replaceOnChanges example.
Method: documentation only; no commands were run.
