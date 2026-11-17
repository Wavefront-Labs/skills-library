---
id: computing-software.systems-network-administration.netbox.power-panels-and-feeds
name: power-panels-and-feeds
category: computing-software
field: systems-network-administration
product: netbox
tags: [power-tracking, power-panel, power-feed]
level: practitioner
status: docs-checked
description: "Document facility power from panel to device power port."
sources: ["https://netboxlabs.com/docs/netbox/features/power-tracking/", "https://netboxlabs.com/docs/netbox/features/tenancy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Power tracking

Goal: document power distribution from the facility to devices.

**Power panel.** The furthest upstream power element modeled, typically a distribution or breaker panel where facility power splits into discrete circuits, which are modeled as feeds. Each panel belongs to a site and may optionally be tied to a location within it. A single panel can supply any number of feeds.

**Power feed.** A discrete power circuit originating from an upstream panel. A feed has a name, an operational status and electrical characteristics such as supply (AC or DC), voltage and amperage.

**Connections.** A device power port connects to a feed by cable. Only one port can connect to a feed. When several devices draw from the same feed, model the power distribution unit as its own device, with its outlets feeding the downstream devices.

**Redundancy.** Each feed is typed primary or redundant, which lets you model redundant topologies. For a single, non-redundant supply, mark every feed as primary.

**Tenancy.** Power feeds can also be assigned to tenants.

**Checklist**

1. Create the panel under the correct site.
2. Add feeds with supply and voltage.
3. Model PDUs as devices.
4. Set primary or redundant type.

## Checked

Method: docs-checked 2026-11-09 against the NetBox Power Tracking and Tenancy feature pages (read in full).
