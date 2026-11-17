---
id: computing-software.systems-network-administration.home-assistant.dev-tools-reload
name: dev-tools-reload
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [reload, dev-tools, restart]
level: practitioner
status: docs-checked
description: "Apply configuration.yaml changes without a restart using the YAML developer tool reload list, and know which developer tool tabs exist."
sources:
  - https://www.home-assistant.io/docs/tools/dev-tools/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: apply YAML edits quickly and safely.

Most integrations that do not interact with devices or services can reload changes to their configuration.yaml entries without restarting Home Assistant.

Reload:

1. Go to Settings > Tools > YAML and scroll to YAML configuration reloading. Alternatively, press the C key anywhere in the UI to open the quick search command palette and search for `reload`.
2. You get a list of integrations, such as Automations or Conversation.
3. If the integration is listed, reload it. If it is not, a full restart is needed.

Always validate first: the same YAML tab has the configuration check, so run it before reloading or restarting.

Developer tool tabs:

- YAML: check configuration and reload.
- States: filter entities and set an entity state.
- Actions: perform an action, including in YAML mode.
- Template: test templates.
- Events: fire an event or listen to events (enter `*` to listen to all; only the latest 100 are kept).
- Statistics: fix a statistics issue, adjust a statistic, or delete statistics.
- Assist: test a sentence.

For shell validation, see the check-config-script skill.

## Checked

2026-11-04. Confirmed against the Developer tools page. Nothing removed.

Method: documentation only; no commands were run.
