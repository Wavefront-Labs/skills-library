---
id: computing-software.firmware-embedded-development.zephyr.west-manifest-files
name: west-manifest-files
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [west, west-manifest, west-yml, name-allowlist, manifest-import, west-update, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Write and maintain a west.yml manifest for a Zephyr product: remotes, pinned revisions, importing Zephyr with a module allowlist, and freezing for releases."
sources:
  - https://docs.zephyrproject.org/latest/develop/west/manifest.html
  - https://docs.zephyrproject.org/latest/develop/west/built-in.html
  - https://github.com/zephyrproject-rtos/west/blob/main/src/west/app/project.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# West manifest files

The manifest (`west.yml`) lists every git repository in the workspace and the exact revision
of each. It is the single place that defines what "build version X" means.

## Product manifest that imports Zephyr
```yaml
manifest:
  version: "1.2"
  remotes:
    - name: zephyrproject
      url-base: https://github.com/zephyrproject-rtos
    - name: acme
      url-base: https://git.acme.example/fw
  defaults:
    remote: acme
  projects:
    - name: zephyr
      remote: zephyrproject
      revision: v4.1.0                 # tag or SHA, never a moving branch for products
      import:
        name-allowlist:                # only fetch the modules you use
          - cmsis
          - hal_stm32
          - mcuboot
          - littlefs
    - name: acme-drivers
      revision: 3f2c1a9e0b7d...         # pin by SHA
      path: modules/acme-drivers
  self:
    path: app                          # where this manifest repo is checked out
```
- `import: true` pulls in **all** projects from Zephyr's own `west.yml` (many HAL and library
  repos). `name-allowlist` keeps the workspace small and the CI clone fast.
- The `import` map also takes `file:`, `path-allowlist:`, `name-blocklist:`, `path-blocklist:`
  and `path-prefix:`; allowlists override blocklists if both match.
- Projects listed in your manifest override same-named imported ones, which is how you
  substitute a forked HAL: add `- name: hal_stm32, remote: acme, revision: my-fix`.

## Daily commands
```bash
west update                     # sync all projects to manifest revisions
west update --narrow -o=--depth=1   # CI: narrow fetch; -o passes git fetch options
west list                       # name, path, revision of each project
west manifest --resolve         # flattened manifest after imports
west manifest --validate
west diff / west status         # across all repos
```

## Releases
```bash
west manifest --freeze -o release-1.4.0.yml   # every project pinned to its current SHA
```
Commit the frozen file (or tag the manifest repo with all revisions as SHAs). A tag in a
third-party repo can move; a SHA can't.

## Groups
`group-filter: [-optional]` in the manifest plus `groups: [optional]` on projects lets users
opt in with `west config manifest.group-filter -- +optional` (see west-manifest-groups-and-filters). Use it for large test-only repos.

## Gotchas
- `west update` checks out a detached HEAD at the manifest revision in each project. Local
  commits added on top of a previously detached HEAD can be garbage-collected, so keep a local
  branch checked out before running it (`west update --rebase` rebases checked-out branches).
- Editing the manifest has no effect until `west update`.
- After bumping Zephyr, re-run `west update` and also `pip install -r zephyr/scripts/requirements.txt`.

## Verify
- [ ] Every project revision is a tag or SHA; `west manifest --freeze` matches the committed release manifest.
- [ ] Fresh `west init -m <url> --mr <tag> && west update` builds the product in CI.
- [ ] Allowlist contains only modules actually used; build a clean workspace to catch a missing one.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2) and west 1.5.0 source. Confirmed manifest version values and the import map keys including allow/blocklist precedence, project-over-import precedence, --resolve, --freeze -o and --validate (west manifest page), west update detached-HEAD behaviour and --rebase (west built-in page), and the update --narrow / -o / list --all options (west/app/project.py). Corrected the detached-HEAD gotcha and the import map keys; removed the unconfirmed size claim.
Method: documentation only; no commands were run.
