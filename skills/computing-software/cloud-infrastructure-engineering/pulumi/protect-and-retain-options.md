---
id: computing-software.cloud-infrastructure-engineering.pulumi.protect-and-retain-options
name: protect-and-retain-options
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, retain-on-delete, protect-option, pulumi-state-unprotect, resource-options]
level: practitioner
status: docs-checked
description: "Guard Pulumi resources with the protect and retainOnDelete options, how destroy behaves, and unprotecting with pulumi state unprotect."
sources:
  - https://www.pulumi.com/docs/iac/concepts/resources/options/protect/
  - https://www.pulumi.com/docs/iac/concepts/resources/options/retainondelete/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_state_unprotect/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# protect and retainOnDelete

```typescript
const db = new aws.rds.Instance("db", {...}, { protect: true });
const bucket = new aws.s3.Bucket("data", {}, { retainOnDelete: true });
```
```python
db = aws.rds.Instance("db", opts=pulumi.ResourceOptions(protect=True))
bucket = aws.s3.Bucket("data", opts=pulumi.ResourceOptions(retain_on_delete=True))
```

- `protect: true`: a protected resource cannot be deleted directly; a deployment that tries to delete it for any reason is an error. Children inherit `protect` from their parent; set `protect: false` on a child to override.
- `retainOnDelete: true`: Pulumi does not call the provider's `Delete` when deleting or replacing the resource, so it is removed from state but stays in the cloud.

Remove protection:
```bash
pulumi state unprotect 'urn:pulumi:prod::app::aws:rds/instance:Instance::db'
pulumi state unprotect --all
```
(or set `protect: false` and run `pulumi up`). Once unprotected, the resource can be deleted in a following update.

## Gotchas
- A protected resource makes `pulumi destroy` fail until it is unprotected. `pulumi stack rm --force` removes the stack and leaves its resources behind.
- `retainOnDelete` on a replaced resource leaves the old instance in the cloud.
- There is no built-in flag to protect every resource in a stack; use a stack transform to apply `protect: true` to all of them.

## Verify
On a scratch stack, run `pulumi destroy` and confirm it reports the protection error for the protected resource.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the protect and retainOnDelete option pages (semantics, inheritance, two ways to unprotect, stack transforms), the `pulumi state unprotect` reference (`--all`) and the `pulumi stack rm` reference (`--force`). Removed: the unconfirmed claims that protect does not stop in-place updates and that a retained replaced instance keeps billing or conflicts on names.
Method: documentation only; no commands were run.
