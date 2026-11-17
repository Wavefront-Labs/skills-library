---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-section-mount-dependencies
name: quadlet-section-mount-dependencies
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, quadlet-section, setmountsdependency, requiresmountsfor, wantsmountsfor, automount, defaultdependencies]
level: advanced
status: docs-checked
description: "Use the [Quadlet] section's SetMountsDependency to choose Requires, Wants or None for mount-source dependencies, and recall DefaultDependencies."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tune what happens when a mount source disappears.

Settings shared across unit types live in a `[Quadlet]` section. Two keys exist: `DefaultDependencies=` and `SetMountsDependency=`.

`DefaultDependencies=` defaults to true and adds the `After=` and `Wants=` dependencies on `network-online.target` (or `podman-user-wait-network-online.service` for user units). Set false to omit them. It is distinct from the systemd `[Unit]` option of the same name.

`SetMountsDependency=` configures the systemd dependency generated for mount source paths and applies to all mount source paths in the file. Values:

- `Requires` (default): adds `RequiresMountsFor=`; the service is stopped if the mount becomes inactive.
- `Wants` (systemd 256 or later): adds `WantsMountsFor=`; the mount is started when the service starts but the service is not stopped if the mount becomes inactive.
- `None`: no mount dependency.

It does not change Quadlet's dependency on its container storage directory. The page's example for an automount share:

```
[Quadlet]
SetMountsDependency=Wants
```

Both keys are written under the `[Quadlet]` header, for example `DefaultDependencies=false`.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
