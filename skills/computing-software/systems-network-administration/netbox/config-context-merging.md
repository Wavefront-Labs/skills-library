---
id: computing-software.systems-network-administration.netbox.config-context-merging
name: config-context-merging
category: computing-software
field: systems-network-administration
product: netbox
tags: [config-context, weight, local-context]
level: advanced
status: docs-checked
description: "Assign JSON data by region, site, role and more and control precedence with weight."
sources: ["https://netboxlabs.com/docs/netbox/features/context-data/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Config contexts

Goal: deliver per-device JSON data without hand-editing each object.

A config context is arbitrary JSON that applies to devices and virtual machines by matching characteristics. It can be consumed by API clients or used to render configuration templates.

**Match criteria.** Both devices and VMs: region, site group, site, role, platform, tenant group, tenant, tag. Devices only: location, device type. VMs only: cluster type, cluster group, cluster.

**Merging.** Several contexts can apply; they are merged by **weight**. The docs example gives a regional context (weight 1000) with `ntp-servers` and `syslog-servers`, then a site-level context with higher weight setting only `syslog-servers` to `["192.168.43.107"]`. The result keeps the regional NTP list but takes the site syslog list: higher-weight data overwrites conflicting keys while non-conflicting data is preserved.

**Local context.** A device or VM can hold its own local context, which always takes precedence over assigned contexts. If you define it for many objects, a custom field may fit better.

**Checklist**

1. Give broad contexts low weight.
2. Give specific overrides higher weight.
3. Keep local context for exceptions.

## Checked

Method: docs-checked 2026-11-09 against https://netboxlabs.com/docs/netbox/features/context-data/ (downloaded; read the criteria table, the weight 1000/2000 merge example, and the local context paragraph).
