---
id: computing-software.systems-network-administration.netbox.device-types-and-components
name: device-types-and-components
category: computing-software
field: systems-network-administration
product: netbox
tags: [device-type, component-templates, manufacturer]
level: practitioner
status: docs-checked
description: "Build device types once so every device inherits its components."
sources: ["https://netboxlabs.com/docs/netbox/features/devices-cabling/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Device types and component templates

Goal: model hardware makes once and instantiate many devices.

A **manufacturer** should represent a real organization. A **device type** is a unique manufacturer and model combination. Each device type has component templates that devices copy on creation. You may also draw from the community device type library rather than hand-building common models.

Components that can be modeled:

- Interfaces
- Console ports and console server ports
- Power ports and power outlets
- Front and rear pass-through ports
- Module bays (house modules)
- Device bays (house child devices)

Example from the docs for a Juniper EX4300-48T: one console port template, two power ports (`PSU0`, `PSU1`), 48 1GE interfaces (`ge-0/0/0` to `ge-0/0/47`) and four 10GE interfaces (`xe-0/2/0` to `xe-0/2/3`).

**Not retroactive.** Components are instantiated only when a device is created. Editing the device type later does not change existing devices, which protects their data.

A device has an operational status, a functional role and a software platform, and may be installed at a position in a rack.

**Checklist**

1. Create the manufacturer.
2. Define the device type and templates fully before creating devices.
3. Do not expect edits to propagate.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Devices and cabling page: manufacturer, device type, component templates, EX4300-48T example, non-retroactive templates. Removed: Nothing.

Method: documentation only; no commands were run.
