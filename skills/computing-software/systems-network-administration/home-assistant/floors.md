---
id: computing-software.systems-network-administration.home-assistant.floors
name: floors
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [floors, level, targets]
level: intro
status: docs-checked
description: "Create Home Assistant floors with a level, icon, areas and aliases, and use a floor as an action target in automations and scripts."
sources:
  - https://www.home-assistant.io/docs/organizing/floors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: group areas into the physical floors of your home.

A floor is a logical grouping of areas. Devices and entities cannot be assigned to a floor directly, only to areas. Floors can be a target for actions in automations and scripts, for example to turn off all the lights on the downstairs floor.

Create a floor:

1. Go to Settings > Areas, labels & zones and select Add > Create floor.
2. Enter a Name (required).
3. Enter a Level. It can be negative, for example for underground floors. The level determines the default floor icon; it does not change the order of floors.
4. Choose an Icon from the Material Design Icons.
5. Under Areas, select Add area to add the areas on this floor.
6. Under Aliases, add alternative names. Voice assistants use aliases.
7. Save.

Reorder floors on the built-in dashboards through the reordering option described on the floors page, since the level does not do this.

Typical flow:

1. Create floors.
2. Create areas and set their Floor.
3. Assign devices to areas.
4. Target the floor in actions.

## Checked

2026-11-04. Confirmed against the Floors page. Removed the paragraph of naming practice that comes from another page, not Floors.

Method: documentation only; no commands were run.
