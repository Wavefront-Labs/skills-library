---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-unit-dependencies-and-names
name: quadlet-unit-dependencies-and-names
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, dependencies, requires, after, resource-names, specifiers, relative-paths]
level: advanced
status: docs-checked
description: "Wire dependencies between Quadlet units by file name, translate Wants, Requires and After keys, set resource names and avoid specifier and percent-path traps."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make one Quadlet depend on another and name resources safely.

Quadlet translates the `[Unit]` keys `Wants`, `Requires`, `Requisite`, `BindsTo`, `PartOf`, `Upholds`, `Conflicts`, `Before` and `After` between Quadlet units. You reference the Quadlet file name, not the generated service. Example in `fedora.container`:

```
[Unit]
After=basic.container
Requires=basic.container

[Container]
Image=registry.fedoraproject.org/fedora:41
```

Resource names: units can set the names of created resources, such as `VolumeName` in a `.volume` or `PodName` in a `.pod`. Using systemd specifiers that reference the generated service unit (such as `$N`) breaks Quadlet's linking between resources, because each service translates them differently.

Relative paths: Quadlet does not resolve relative paths that start with `%`, so that systemd specifiers still work. Prepend `./` to resolve one: use `EnvironmentFile=./%n/env` instead of `EnvironmentFile=%n/env`. Without an explicit template instance, relative paths resolve relative to the template file.

Name keys by unit type: `VolumeName` for `.volume`, `NetworkName` for `.network`, `PodName` for `.pod`, `ContainerName` for `.container`, `ServiceName` for any unit. Default service names: the Quadlet name for containers and kube units, and `$name-volume.service`, `$name-network.service`, `$name-pod.service`, `$name-build.service` or `$name-image.service` for the other types.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
