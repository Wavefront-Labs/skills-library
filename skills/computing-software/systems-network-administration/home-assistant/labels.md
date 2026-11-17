---
id: computing-software.systems-network-administration.home-assistant.labels
name: labels
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [labels, grouping, filtering]
level: intro
status: docs-checked
description: "Create and apply Home Assistant labels to group areas, devices, entities, automations, scenes, scripts and helpers regardless of location."
sources:
  - https://www.home-assistant.io/docs/organizing/labels/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: group things across rooms and types, such as everything with heavy energy use.

Labels can be assigned to areas, devices, entities, automations, scenes, scripts and helpers. They can be used to filter lists and in automations and scripts, for example to turn off all devices with the label `heavy energy usage` when there is little solar energy.

Create a label:

1. Go to Settings > Areas, labels & zones and open the Labels tab.
2. Select Create label.
3. Enter a Name (required), an icon and a Color.
4. Select Create.

Apply a label:

- To an area: Settings > Areas, labels & zones, then on the area card select the edit button, and choose labels or Add new label.
- To a device, entity or helper: Settings > Devices & services, open the respective tab, and use the multi-select mode to pick items and apply labels.

Differences between the groupings:

- Areas are physical rooms, and floors group areas.
- Labels ignore location, so one label can span many rooms.

Use a label when the property you care about is not tied to a place. Filter lists by label to check what you tagged.

## Checked

2026-11-04. Confirmed against the Labels page. Removed the advice to name labels by purpose, which is not on the page.

Method: documentation only; no commands were run.
