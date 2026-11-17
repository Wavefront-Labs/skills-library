---
id: computing-software.cloud-infrastructure-engineering.pulumi.explicit-providers
name: explicit-providers
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, explicit-provider, provider-option, multi-region, provider-config]
level: practitioner
status: docs-checked
description: "Use explicit Pulumi provider instances for multi-region, multi-account or multi-cluster deployments via the provider and providers options."
sources:
  - https://www.pulumi.com/docs/iac/concepts/providers/
  - https://www.pulumi.com/docs/iac/concepts/resources/options/provider/
  - https://www.pulumi.com/docs/iac/concepts/resources/options/providers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Explicit providers

The default provider uses stack config (`aws:region`). Create explicit provider instances to target several regions or accounts.

```typescript
const west = new aws.Provider("west", { region: "us-west-2" });
const eu = new aws.Provider("eu", { region: "eu-west-1" });
const b = new aws.s3.Bucket("b", {}, { provider: west });
const comp = new MyComponent("c", {}, { providers: { aws: eu } }); // children use eu
```
```python
west = aws.Provider("west", region="us-west-2")
b = aws.s3.Bucket("b", opts=pulumi.ResourceOptions(provider=west))
```

## Gotchas
- `provider` sets the provider for one resource; the default is to inherit it from the parent resource, and to use the ambient provider from stack configuration when there is no parent.
- `providers` (a map keyed by package name) is supported only on component resources; it flows to every child through parent inheritance, and a matching provider inherited from the parent's `providers` map is used for children. To pass an explicit provider to a single custom resource, use `provider`.
- If a component is itself a child of another component, it inherits its providers from that parent in turn.

## Verify
`pulumi stack --show-urns` lists the provider resource (URN type `pulumi:providers:aws`, here named `west`) and the resources that use it; the cloud console shows them in the chosen region.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the Providers concept page (explicit `aws.Provider("useast1", { region })` pattern), the `provider` option page (inheritance default, ambient provider, `Provider("provider", region=...)`) and the `providers` option page (components only, map keyed by package, first-match resolution, inheritance). Removed: `assumeRoles`, the Kubernetes `kubeconfig` provider line, and the unconfirmed claims about provider config changes forcing replacement, secrets in provider args, and provider replacement moving resources.
Method: documentation only; no commands were run.
