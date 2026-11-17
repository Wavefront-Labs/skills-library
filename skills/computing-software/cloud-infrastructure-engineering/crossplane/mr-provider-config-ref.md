---
id: computing-software.cloud-infrastructure-engineering.crossplane.mr-provider-config-ref
name: mr-provider-config-ref
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [managed-resource, providerconfig, clusterproviderconfig, credentials]
level: practitioner
status: docs-checked
description: "Choose credentials per managed resource with providerConfigRef, ProviderConfig and ClusterProviderConfig."
sources:
  - https://docs.crossplane.io/latest/managed-resources/managed-resources/
  - https://docs.crossplane.io/latest/packages/providers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`spec.providerConfigRef` tells the provider which configuration (authentication settings) to use for a managed resource.

```yaml
spec:
  providerConfigRef:
    name: user-keys
    kind: ProviderConfig
```

The AWS provider has two kinds:

- `ProviderConfig`: namespaced; applies only to MRs in the same namespace.
- `ClusterProviderConfig`: cluster-wide; applies to MRs in every namespace.

When you reference one you must give both `name` and `kind`. If you omit `providerConfigRef` entirely it defaults to name `default`, kind `ClusterProviderConfig`.

Different MRs can reference different configs, so one provider can authenticate with different credentials per resource.

Connection details work separately: set `spec.writeConnectionSecretToRef.name` and the provider saves values such as endpoint, password, port and username in that Secret. The provider decides which keys it writes.

A ProviderConfig defines how the provider authenticates, for example with a Secret reference to credentials; the MR only names it. A single Provider can authenticate with multiple accounts: one ProviderConfig per account, attached to each MR by `name` and `kind`.

The provider determines the data written to the connection Secret; see its docs for the keys.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Managed Resources page and Providers page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: claims about misspelled config names and secret placement (not on the page).

Method: documentation only; no commands were run.
