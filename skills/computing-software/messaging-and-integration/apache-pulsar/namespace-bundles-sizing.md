---
id: computing-software.messaging-and-integration.apache-pulsar.namespace-bundles-sizing
name: namespace-bundles-sizing
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [namespace-bundles, bundle-range, split-bundle, default-number-of-namespace-bundles, bundle-cost]
level: advanced
status: docs-checked
description: "Size Pulsar namespace bundles: where bundle counts come from, what an owned bundle costs, finding a topic's bundle, and splitting (permanent, no merge)."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/administration-namespace-bundles.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick a bundle count that lets a namespace spread across brokers without waste.

A bundle owns a range of the namespace 32-bit hash space and is the unit the load manager assigns to a broker. The count is fixed at namespace creation and can only grow through splits.

Where counts come from:
- Namespaces made with `pulsar-admin namespaces create` (or REST/Java admin) without a count: `defaultNumberOfNamespaceBundles` in broker.conf, 32 by default; with `--bundles N` the value N.
- `public/default` from `pulsar initialize-cluster-metadata`: `--default-namespace-bundle-number`, 32 by default; `pulsar/system`: `--system-namespace-bundle-number`, 64 by default; `defaultNumberOfSystemNamespaceBundles` also 64 in broker.conf when the broker creates it.
- Namespaces created with `pulsar initialize-namespace`: 32.
- Per-broker heartbeat namespaces: 1.
Existing namespaces keep their counts when defaults change.

Inspect:
```shell
pulsar-admin namespaces bundles my-tenant/my-namespace
pulsar-admin topics bundle-range persistent://my-tenant/my-namespace/my-topic
```

Cost: a bundle costs something only after a topic in it is looked up. Ownership is acquired lazily; each owned bundle has an ownership entry in the metadata store (ephemeral node with the modular manager, ownership system topic entry with the extensible one), an entry in the owning broker load report, and one unload step when the broker shuts down or the bundle moves. Unlooked-up bundles are just policy boundaries, so a generous default is cheap for small namespaces.

Sizing rule: have more bundles than brokers; with fewer, some brokers never receive the namespace, and a count close to the broker count balances poorly.

Splitting: `pulsar-admin namespaces split-bundle my-tenant/my-namespace --bundle 0x00000000_0x08000000`. Splits are permanent; there is no merge, so avoid over-splitting by choosing the initial count well.

## Checked

2026-11-03. Confirmed against the pulsar-site page administration-namespace-bundles: the defaults table, inspect commands, bundle cost, sizing rule and split command. Removed the invented Verify step.

Method: documentation only; no commands were run.
