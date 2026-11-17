---
id: computing-software.firmware-embedded-development.zephyr.west-manifest-groups-and-filters
name: west-manifest-groups-and-filters
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [west-group-filter, manifest-group-filter, west-groups, project-filter, west, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Trim a west workspace with manifest groups and group-filter: mark optional projects, enable groups per workspace, and avoid cloning every HAL on west update."
sources:
  - https://docs.zephyrproject.org/latest/develop/west/manifest.html#project-groups
  - https://docs.zephyrproject.org/latest/develop/west/config.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/west.yml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manifest groups and project filters

A full `zephyr/west.yml` pulls dozens of HAL and library repos. Groups let a workspace fetch only
what it needs.

## Assign groups in the manifest
```yaml
manifest:
  group-filter: [-optional, -vendor-sdk]     # disabled by default for this manifest
  projects:
    - name: hal_stm32
      revision: <sha>
      groups: [hal]
    - name: my-dsp-lib
      revision: v2.1.0
      groups: [optional]
    - name: vendor-blob-sdk
      url: https://git.example.com/sdk
      revision: main
      groups: [vendor-sdk]
```
Rules:
- A project is **inactive** only if **all** of its groups are disabled. Projects with no
  `groups` are always active.
- Group names cannot contain commas, colons or whitespace, and cannot start with `-` or `+`.
- `group-filter` entries: `-name` disables, `+name` enables.
- A project cannot use both `import:` and `groups:`.
- `manifest.project-filter` (regexes on project names) takes priority: a project it activates or
  deactivates ignores its groups. It is the only way to deactivate a project that has no groups.

## Enable per workspace (no manifest edit)
```bash
west config manifest.group-filter -- +optional
west update
```
The `--` stops west treating `+optional` as an option. The local config filter is applied after
the manifest's filter, so it can re-enable groups disabled upstream.

## Combining with imports
With `import: {name-allowlist: [...]}` you restrict which upstream Zephyr projects are pulled at
all (preferred for product manifests). If you import one manifest, groups it disables in its
`group-filter` stay disabled in yours (west 0.10.0 and later); override them in your manifest's
`group-filter`, in the `manifest.group-filter` config option, or both.

## Inspecting
```bash
west list                       # active projects only
west list --all                 # including inactive, with groups column via -f
west list -f "{name:20} {groups} {revision}"
```
`west update` skips inactive projects; `west forall` and `west diff` also skip them unless `--all`.

## Gotchas
- A project already cloned stays on disk when its group gets disabled; west just ignores it.
- CI must set the same `manifest.group-filter` (or pass `--group-filter` to `west update`)
  as developers, or builds differ.
- Zephyr's own west.yml sets `group-filter: [-babblesim, -optional, -testing]`; enable a group
  (for example `+babblesim`) to fetch its projects.

## Verify
- [ ] `west list` on a fresh workspace shows only the intended projects.
- [ ] CI script sets the group filter explicitly.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed group naming rules, group-filter semantics (inactive only when all groups disabled), config-over-manifest ordering, import behaviour from west 0.10.0, the project-filter option (west manifest and config pages), update --group-filter and list/forall/diff --all (west/app/project.py), and the group-filter in Zephyr west.yml. Added the missing import-plus-groups restriction and project-filter priority.
Method: documentation only; no commands were run.
