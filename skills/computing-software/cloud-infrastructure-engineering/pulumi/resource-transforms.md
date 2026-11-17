---
id: computing-software.cloud-infrastructure-engineering.pulumi.resource-transforms
name: resource-transforms
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, transforms, resource-transforms, transformations, invoke-transforms]
level: practitioner
status: docs-checked
description: "Modify Pulumi resource arguments and options with transforms: the transforms option and stack transforms, in TypeScript and Python."
sources:
  - https://www.pulumi.com/docs/iac/concepts/resources/options/transforms/
  - https://www.pulumi.com/docs/iac/concepts/resources/options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource transforms

A transform changes a resource's properties or options before it is registered.

```typescript
// Component-level: applies to the resource and all of its children
new MyComponent("app", {}, {
  transforms: [args => {
    if (args.type === "aws:s3/bucket:Bucket") {
      return { props: { ...args.props, tags: { team: "web" } }, opts: args.opts };
    }
    return undefined;   // leave unchanged
  }],
});

// Stack-level: applies to every resource
pulumi.runtime.registerResourceTransform(args => { /* same shape */ return undefined; });
```
```python
def add_tags(args: pulumi.ResourceTransformArgs):
    if args.type_ == "aws:s3/bucket:Bucket":
        props = dict(args.props or {})
        props["tags"] = {"team": "web"}
        return pulumi.ResourceTransformResult(props=props, opts=args.opts)

pulumi.runtime.register_resource_transform(add_tags)
# or: opts=pulumi.ResourceOptions(transforms=[add_tags])
```

Return `ResourceTransformResult(props=..., opts=ResourceOptions.merge(args.opts, ...))` to change options; use keyword arguments. Transforms replace the older, deprecated transformations, support async functions, and also apply to children of packaged components.

## Gotchas
- A transform for a packaged component may be called twice for the same resource; keep it idempotent.
- Return nothing (`undefined` / `None`) to leave a resource unchanged.

## Verify
`pulumi preview --diff` shows the changed properties (for example the tags) on matching resources.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the Transforms resource option page (`transforms` option, stack transform registration in both languages, `ResourceTransformResult`, `args.type_`, returning `undefined`, async support, packaged components, called twice) and the resource options index. Removed: "confirm" markers and unsourced notes.
Method: documentation only; no commands were run.
