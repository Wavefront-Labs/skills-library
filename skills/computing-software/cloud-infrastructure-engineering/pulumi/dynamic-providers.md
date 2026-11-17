---
id: computing-software.cloud-infrastructure-engineering.pulumi.dynamic-providers
name: dynamic-providers
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, dynamic-provider, dynamic-resource, pulumi-dynamic, custom-provider]
level: practitioner
status: docs-checked
description: "Write Pulumi dynamic providers in TypeScript or Python: check, create, diff, update, delete lifecycle, configure hook, and known limits."
sources:
  - https://www.pulumi.com/docs/iac/concepts/providers/dynamic-providers/
  - https://www.pulumi.com/docs/iac/guides/building-extending/providers/dynamic-providers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic providers

A dynamic provider implements a custom resource inside the Pulumi program. Supported languages: TypeScript and Python only.

```typescript
const provider: pulumi.dynamic.ResourceProvider = {
  async create(inputs) {
    // call your API here
    return { id: "abc123", outs: { ...inputs } };
  },
  async delete(id, props) { /* call your API */ },
};
class Thing extends pulumi.dynamic.Resource {
  constructor(name: string, args: { size: pulumi.Input<number> }, opts?: pulumi.CustomResourceOptions) {
    super(provider, name, args, opts);
  }
}
```
```python
from pulumi.dynamic import Resource, ResourceProvider, CreateResult

class ThingProvider(ResourceProvider):
    def create(self, props):
        return CreateResult(id_="abc123", outs=props)

class Thing(Resource):
    def __init__(self, name, props, opts=None):
        super().__init__(ThingProvider(), name, props, opts)
```

Lifecycle: `check` always runs first; a new resource gets `create`; an existing one gets `diff` (returns `changes`, `replaces` and so on). A replacement creates the new resource then deletes the old one; otherwise `update` runs. Only `create` is required.

Credentials: read Pulumi config in the `configure` hook (store with `--secret`), or read environment variables inside each method.

## Gotchas
- `read` is not implemented (not functional, pulumi/pulumi#16175), so `pulumi import` and the static `get` are not supported for dynamic resources.
- Dynamic providers are not supported on the Bun runtime. Program code is serialized, which limits what the provider functions can capture.
- All dynamic resources share one type (`pulumi-nodejs:dynamic:Resource` or `pulumi-python:dynamic:Resource`).
- To force an update after changing provider code, add a version input or have `diff` return `{ changes: true }`.

## Verify
`pulumi preview` shows the resource as a create; after `pulumi up` the second preview shows no changes unless `diff` reports some.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the Dynamic providers concept and guide pages (supported languages, lifecycle order, `configure`, `CreateResult`, shared resource type, serialization, `read` not functional, no Bun support). Fixed: the draft claimed `read` powers import and refresh and left Go, .NET and Java unconfirmed. Removed: the claim that `up` always calls update without `diff`.
Method: documentation only; no commands were run.
