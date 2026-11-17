---
id: computing-software.systems-network-administration.home-assistant.areas
name: areas
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [areas, aliases, rooms]
level: intro
status: docs-checked
description: "Create Home Assistant areas that match rooms, assign them to floors, add labels and voice aliases, and assign devices to areas from the Overview dashboard."
sources:
  - https://www.home-assistant.io/docs/organizing/areas/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: model your rooms so one action can target a whole room.

An area is a logical grouping of devices and entities that matches a room in your home. Example: the Living room area lets one action turn off all its lights. Areas can be assigned to floors and used to generate dashboard cards such as the Area card.

Create an area:

1. Go to Settings > Areas, labels & zones and select Add > Create area.
2. Enter a Name (required).
3. Optionally choose an Icon from the Material Design Icons.
4. Under Floor, assign a floor (create floors first if needed).
5. Under Add labels, add labels.
6. Optionally Add picture.
7. Under Aliases, add alternative names. Aliases are used by voice assistants to refer to an area, entity or floor.

Assign a device to an area:

1. In the sidebar, select Overview.
2. Select the Devices tile. It shows devices not assigned to an area and only appears when there are some.
3. For the device, select Assign area and choose the area.

Use areas as targets in automations and scripts. See the floors and labels skills for the other two grouping levels.

## Checked

2026-11-04. Confirmed against the Areas page. Removed the naming advice line, which is not on the Areas page.

Method: documentation only; no commands were run.
