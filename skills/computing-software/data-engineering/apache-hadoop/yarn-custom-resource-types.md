---
id: computing-software.data-engineering.apache-hadoop.yarn-custom-resource-types
name: yarn-custom-resource-types
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, yarn, resource-types, resource-profiles, node-resources]
level: advanced
status: docs-checked
description: "Defining custom YARN resource types: yarn.resource-types and units, per-node yarn.nodemanager.resource-type values, MapReduce request keys, and resource profiles."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/ResourceModel.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom resource types

YARN tracks CPU and memory by default; the model can be extended to arbitrary countable resources (consumed while a container runs, released afterwards), such as GPUs or software licences.

ResourceManager side (`resource-types.xml` in the same directory as yarn-site.xml, or yarn-site.xml itself):
- `yarn.resource-types`: comma-separated additional resources; may not include `memory`, `memory-mb` or `vcores`.
- `yarn.resource-types.<resource>.units`: default unit. Valid: p, n, u, m, (none), k, M, G, T, P, and binary Ki, Mi, Gi, Ti, Pi.
- `yarn.resource-types.<resource>.minimum-allocation` and `.maximum-allocation`: optional.

Names must begin with a letter and contain only letters, digits, `.`, `_`, `-`; an optional namespace of period-separated groups followed by a slash is allowed (`com.acme/myresource` valid; `10myresource`, `my resource`, `com/acme/myresource` invalid).

NodeManager side (`node-resources.xml` or yarn-site.xml): `yarn.nodemanager.resource-type.<resource>` = amount that node offers, e.g. `5G` or `2m`. Units need not match the RM's; the RM converts.

MapReduce container requests (AM, map, reduce): `yarn.app.mapreduce.am.resource.memory-mb` (default 1536), `...am.resource.vcores` (1), `mapreduce.map.resource.memory-mb` and `mapreduce.reduce.resource.memory-mb` (1024), `mapreduce.map.resource.vcores` and `mapreduce.reduce.resource.vcores` (1). Older names such as `mapreduce.map.memory.mb` and `...cpu.vcores` are marked no longer preferred. Custom resources use `yarn.app.mapreduce.am.resource.<resource>`, `mapreduce.map.resource.<resource>` and `mapreduce.reduce.resource.<resource>`; with no unit, the resource's default unit applies.

YARN may adjust requests to the configured minimum and maximum or round to a multiple of the increment: `yarn.scheduler.minimum-allocation-mb`, `maximum-allocation-mb`, `increment-allocation-mb` and the `-vcores` equivalents (defaults not on this page).

Resource profiles: set `yarn.resourcemanager.resource-profiles.enabled` = true (default false) in the RM's yarn-site.xml; a JSON file defines profiles (for example small, default, large, compute) of `memory-mb`, `vcores` and custom resources such as `gpu`. Distributed shell is currently the only client that supports them, via `-container_resource_profile <name>`.

## Checked

Method: 2026-11-08, read the project's ResourceModel markdown source in full against this skill. Corrected the unit list (the page lists p through Pi, not the shorter list given earlier) and dropped the "case matters" claim and an unsupported "Verify" step (RM UI) that the page never states. Other keys and defaults were unchanged.
