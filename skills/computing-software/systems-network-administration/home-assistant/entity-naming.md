---
id: computing-software.systems-network-administration.home-assistant.entity-naming
name: entity-naming
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [entity-id, naming, rename]
level: practitioner
status: docs-checked
description: "Name Home Assistant devices, entities and areas for what they are, and change an entity ID from the entity settings dialog."
sources:
  - https://www.home-assistant.io/docs/configuration/customizing-entities/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep names short and consistent so entity IDs stay readable.

Definitions:

- Entity name: the function or data point, such as `Temperature` or `Power`.
- Entity ID: what automations and scripts use, such as `sensor.living_room_thermostat_temperature`.
- Changing an entity name does not change its entity ID.

Recommendations:

- Name items for what they are, not where they are. Area `Living room`, not `Ground floor living room`; device `Multi sensor`, not `Office multi sensor`.
- The device name identifies the physical device; the entity name identifies what it reports or controls.
- Give identical devices a distinguishing name, such as `Left window sensor` and `Right window sensor`.
- Assign an area to each device and a floor to each area; Home Assistant uses that when creating entity IDs.
- To change only a label on one dashboard, change the displayed name on the card.
- Existing names that already work do not need renaming.

Change an entity ID:

1. Go to Settings > Devices & services > Entities and select the entity.
2. Select Settings (cog) in the top-right.
3. Edit the entity ID, for example to `binary_sensor.lumi_sensor_aq2_opening`.

Rules: lowercase letters, numbers and underscores only; it must not start or end with an underscore. The restore icon reverts to the default.

To regenerate all entity IDs of a device, open the device and choose Menu > Recreate entity IDs. Entity names are not changed.

## Checked

2026-11-04. Confirmed against the Customizing entities page. Nothing removed.

Method: documentation only; no commands were run.
