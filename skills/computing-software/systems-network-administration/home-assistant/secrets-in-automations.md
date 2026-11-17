---
id: computing-software.systems-network-administration.home-assistant.secrets-in-automations
name: secrets-in-automations
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [read-only, automations-secret, ui-editor]
level: advanced
status: docs-checked
description: "Use !secret with automations safely: keep it out of automations.yaml and scripts.yaml or the UI editor breaks; use a separate read-only file."
sources:
  - https://www.home-assistant.io/docs/configuration/secrets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use `!secret` inside an automation or script without losing the UI editor.

The trap: the UI YAML editor for automations and scripts does not support `!secret`. If `!secret` appears in `automations.yaml` or `scripts.yaml`, you can no longer edit or view any YAML automations or scripts in the UI.

The fix is to put secret-bearing automations in their own file, loaded under a different labelled key. Those automations become read-only in the frontend and the rest stay editable.

configuration.yaml:

```yaml
# The main automations editable in the UI
automation ui: !include automations.yaml
# These automations may contain secrets, and will be read-only in the UI
automation secret: !include automations-secret.yaml
```

Do the same for scripts by splitting them into a separate file (see the splitting-configuration skill, top-level keys).

Warning from the docs: secrets used in automations expose their value to administrators when viewed in the UI, in the YAML source viewer and in the trace viewer. So only put values there that every administrator may see.

Steps:

1. Move the automation that needs the secret into automations-secret.yaml.
2. Reference it with `!secret name`, defined in secrets.yaml.
3. Reload automations or restart, then confirm the remaining automations still open in the editor.

## Checked

2026-11-04. Confirmed against the Secrets page. Nothing removed.

Method: documentation only; no commands were run.
