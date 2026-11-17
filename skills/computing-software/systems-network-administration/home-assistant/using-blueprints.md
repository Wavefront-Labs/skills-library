---
id: computing-software.systems-network-administration.home-assistant.using-blueprints
name: using-blueprints
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [import-blueprint, take-control, reimport]
level: practitioner
status: draft
description: "Import, use, take control of and re-import Home Assistant blueprints from Settings > Automations & scenes > Blueprints, with the compatibility risk."
sources:
  - https://www.home-assistant.io/docs/automation/using_blueprints/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: reuse a community automation without writing it.

Import:

1. Find a blueprint. Home Assistant imports from the forums, GitHub, GitHub gists and the Home Assistant website. Other addresses work too, but Home Assistant asks you to continue only if you trust the source.
2. Go to Settings > Automations & scenes > Blueprints.
3. Select Import blueprint (bottom-right).
4. Enter the Blueprint address and select Preview, then import.

A practice address from the docs:

```text
https://github.com/home-assistant/core/blob/dev/homeassistant/components/automation/blueprints/motion_light.yaml
```

Create an automation from it by filling in the blueprint inputs.

Take control, when you need more than the inputs allow:

1. Open the automation that uses the blueprint.
2. Open the three-dots menu and select Take control.

The automation becomes a regular automation. The blueprint itself is unchanged and other automations keep using it. Take control is not available for automations you cannot edit in the UI, for example ones not stored in `automations.yaml`.

Re-import for updated versions: on the blueprint, open the three-dots menu and choose Re-import blueprint. This overwrites your copy. If the new version is not compatible, it can break your automations and you will need to adjust them manually.
