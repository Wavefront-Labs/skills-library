---
id: computing-software.messaging-and-integration.apache-pulsar.load-balancing-and-shedding
name: load-balancing-and-shedding
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [load-balancing, bundle-split, load-shedding, unload, avg-shedder, load-manager]
level: advanced
status: docs-checked
description: "Tune Pulsar broker load balancing: bundle assignment, split algorithms and thresholds, load shedding strategies, and manual unload commands."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/administration-load-balance.md
  - https://github.com/apache/pulsar-site/blob/main/docs/administration-namespace-bundles.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep traffic evenly spread over brokers and know the manual levers.

Assignment is per bundle, not per topic. A namespace is sharded into bundles, each covering part of the hash range; a topic maps to a bundle by hashing its name. New topics trigger broker selection by load; an overloaded or crashed owner leads to reassignment. Two load managers exist: modular (`loadManagerClassName=...`) and extensible. A load manager that cannot be instantiated makes broker startup fail.

Bundle counts: `defaultNumberOfNamespaceBundles=32` in broker.conf, or `bin/pulsar-admin namespaces create my-tenant/my-namespace --clusters us-west --bundles 64`. Start with more bundles than brokers.

Splitting: `defaultNamespaceBundleSplitAlgorithm` is one of `range_equally_divide` (default), `topic_count_equally_divide`, `specified_positions_divide` (admin API only), `flow_or_qps_equally_divide`. Enable with `loadBalancerAutoBundleSplitEnabled=true` and `loadBalancerAutoUnloadSplitBundlesEnabled=true`. Thresholds: `loadBalancerNamespaceBundleMaxTopics=1000`, `loadBalancerNamespaceBundleMaxSessions=1000`, `loadBalancerNamespaceBundleMaxMsgRate=30000`, `loadBalancerNamespaceBundleMaxBandwidthMbytes=100`, `loadBalancerNamespaceMaximumBundles=128`. Splits are permanent; bundles cannot be merged.

Load shedding: on by default (`loadBalancerSheddingEnabled`, dynamic); `loadBalancerSheddingIntervalMinutes=1`, `loadBalancerSheddingGracePeriodMinutes=30`. Strategy via `loadBalancerLoadSheddingStrategy`: AvgShedder (default for the modular manager, which must also be the placement strategy via `loadBalancerLoadPlacementStrategy`), ThresholdShedder, OverloadShedder, UniformLoadShedder; the extensible manager uses TransferShedder. Gotcha: changing the shedding strategy dynamically needs a broker restart; pairing another shedder with the default placement strategy falls back to LeastLongTermMessageRate with a warning.

Manual unload (clients see a blip of tens of milliseconds):
```shell
pulsar-admin topics unload persistent://tenant/namespace/topic
pulsar-admin namespaces unload tenant/namespace
pulsar-admin namespaces unload tenant/namespace --bundle 0x00000000_0x08000000 --destinationBroker broker-2.example.com:8080
```

Verify: list bundles with `pulsar-admin namespaces bundles <ns>` before and after a split or unload.

## Checked

2026-11-03. Confirmed against the Pulsar load balancing page (bundle-level assignment, 32 default bundles, split algorithms and thresholds, permanent splits, shedding defaults and interval/grace values, AvgShedder default and placement pairing, restart on strategy change, unload commands, tens-of-milliseconds blip) and the namespace bundles page (`namespaces bundles`). Removed: abbreviated `...Max*` setting names, replaced with the full names the page shows.

Method: documentation only; no commands were run.
