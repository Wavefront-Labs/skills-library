---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-upgrade-strategy
name: opentelemetry-operator-upgrade-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, upgrades, upgradestrategy, managementstate, custom-image, automatic-upgrade]
level: practitioner
status: docs-checked
description: "Control whether the operator upgrades an OpenTelemetryCollector resource with spec.upgradeStrategy, and use managementState to stop reconciliation."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/getting-started/upgrading.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/api/opentelemetrycollectors.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Upgrades and spec.upgradeStrategy

The Collector configuration format keeps evolving, so on a new operator release the operator makes a best-effort attempt to upgrade every managed `OpenTelemetryCollector` resource.

You can opt a resource out with the property `.spec.upgradeStrategy`:
- `automatic` is the default: the operator runs its upgrade routine for the instance.
- `none`: the operator skips the instance during the upgrade routine. These are the only two accepted values.

The documented reason for `none` is a resource with a custom `.spec.image`, where the owner wants to manage the configuration themselves rather than have the operator rewrite it. 
Related controls in the API reference:
- `spec.managementState` accepts `managed` (default) or `unmanaged`, deciding whether the operator manages the resource.
- `spec.configVersions` (default 3, minimum 1) sets how many versions of the Collector config are kept, each stored in its own ConfigMap.

## Checked

Method: docs-checked 2026-11-09 against the Upgrades page (read in full) and the upgradeStrategy, managementState and configVersions entries of the OpenTelemetryCollector API reference. Dropped the compatibility-doc, OpAMPBridge/TargetAllocator and CRD-changelog stored-version claims, which were not confirmed.
