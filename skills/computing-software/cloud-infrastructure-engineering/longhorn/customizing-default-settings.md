---
id: computing-software.cloud-infrastructure-engineering.longhorn.customizing-default-settings
name: customizing-default-settings
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [default-settings, configmap, helm-values, settings-crd, kebab-case]
level: practitioner
status: docs-checked
description: "Set Longhorn default settings via Helm defaultSettings, the longhorn-default-setting ConfigMap or Rancher, and change existing settings with the UI, kubectl or helm upgrade."
sources:
  - https://longhorn.io/docs/1.13.0/advanced-resources/deploy/customizing-default-settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose the right way to set Longhorn settings.

At installation:
- Helm: `--set defaultSettings.<name>=<value>` or a `defaultSettings:` block in `values.yaml`.
- Deployment YAML: edit the `longhorn-default-setting` ConfigMap in `longhorn/deploy/longhorn.yaml`.
- Rancher UI: Apps and Marketplace, Longhorn, Install, Edit Options, Longhorn Default Settings.
- Helm Controller: `defaultSettings.<name>` entries under `spec.set`.

Updating existing settings:
- Longhorn UI (recommended; the change is persistent).
- `kubectl edit settings.longhorn.io <SETTING-NAME> -n longhorn-system`
- Helm: edit `values.yaml`, then `helm upgrade`.
- Rancher UI: the same Edit Options path while upgrading.

Key format:
- ConfigMap keys are kebab-case inside `default-setting.yaml`:

```yaml
default-data-path: /var/lib/longhorn-example/
```

- Helm keys are camelCase under `defaultSettings`:

```yaml
defaultSettings:
  defaultReplicaCount: 2
```

Notes:
- An empty string is cleaned up if valid for that setting; invalid values are ignored and the default is not updated.
- Use Helm 3; Helm 2 is no longer supported.
- Available since v1.3.0.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/advanced-resources/deploy/customizing-default-settings/

No claim needed changing.

Method: documentation only; no commands were run.
