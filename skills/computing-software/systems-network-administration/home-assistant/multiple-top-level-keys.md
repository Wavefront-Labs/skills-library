---
id: computing-software.systems-network-administration.home-assistant.multiple-top-level-keys
name: multiple-top-level-keys
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [top-level-keys, labelled-keys, light-groups]
level: practitioner
status: docs-checked
description: "Spread one integration across several files using labelled top-level keys such as light groups, and fall back to packages when unsupported."
sources:
  - https://www.home-assistant.io/docs/configuration/splitting_configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure one integration in several places by giving each top-level key a different label.

Some integrations accept multiple top-level keys. This covers IoT domains such as `light`, `switch` and `sensor`, plus `automation`, `script` and `template`. Each key needs a distinct label after the integration name.

Example in configuration.yaml: the first key keeps entries inline, the labelled key pulls in a file.

```yaml
light:
  - platform: group
    name: "Bedside Lights"
    entities:
      - light.left_bedside_light
      - light.right_bedside_light
# More light groups in a separate file
light groups: !include light-groups.yaml
```

The label (`groups` here) must differ for each key. The same approach lets you keep UI-managed automations apart from hand-written ones:

```yaml
# Automations for public transport notifications
automation public transport: !include public-transport-automation.yaml
```

Steps:

1. Pick a unique label for each extra block: `<integration> <label>:`.
2. Put the block inline or add `!include <file>.yaml`.
3. In the included file, write only the content that belongs under the key (for `light`, a list starting with `- platform:`).
4. Check the configuration before restarting.

If an integration does not support multiple top-level keys, use packages instead (see the packages skill).

## Checked

2026-11-04. Confirmed against the Splitting configuration page and the Packages page. Extended the list of keys to automation, script and template; replaced the claim that the label is arbitrary with the page wording that each key needs a different label.

Method: documentation only; no commands were run.
