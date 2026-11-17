---
id: computing-software.firmware-embedded-development.zephyr.west-workspace-topologies
name: west-workspace-topologies
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [west, west-workspace, west-init, manifest-repository, t2-star-topology, forest-topology, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Choose and set up a west workspace topology for Zephyr work: Zephyr-as-manifest (T1), application-as-manifest (T2) or a dedicated manifest repo (T3)."
sources:
  - https://docs.zephyrproject.org/latest/develop/west/workspaces.html
  - https://docs.zephyrproject.org/latest/develop/west/basics.html
  - https://github.com/zephyrproject-rtos/example-application
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# West workspace topologies

A west workspace is a directory containing `.west/config` plus the repos the manifest lists.
Which repo holds the manifest decides how versions are controlled.

## T1: star, Zephyr is the manifest repo
```bash
west init -m https://github.com/zephyrproject-rtos/zephyr --mr v4.1.0 zp
cd zp && west update
```
This is the default west topology (Zephyr names its modules in its own `west.yml`; the analogy is
git submodules with zephyr as the super-project). Fine for evaluating Zephyr and upstream
contributions. For a product it leaves your app's version untied from the Zephyr revision.

## T2: star, the application is the manifest repo (recommended for products)
```
workspace/
├── .west/config        # manifest.path = app
├── app/                # your repo: west.yml, CMakeLists.txt, src/, boards/, dts/
├── zephyr/
└── modules/hal/...
```
```bash
west init -m https://git.acme.example/fw/app --mr main workspace
cd workspace && west update
# or from an existing clone:
west init -l app
```
`app/west.yml` imports Zephyr with a `name-allowlist` (see west-manifest-files). One commit
of `app` pins everything, so `git checkout v1.4.0 && west update` rebuilds a release exactly.
The zephyrproject-rtos `example-application` repository is an example of this layout. Zephyr's
module revisions then follow the imported `zephyr/west.yml` revision instead of being copied.

## T3: forest, a dedicated manifest repo
A dedicated manifest repo containing no Zephyr source lists Zephyr plus several peer app and
library repos at the same level (analogy: Google `repo`). Use it for several independent
applications or downstream distributions with no central repository. A version bump means a
change in the manifest repo as well as the project repos.

## Choosing
| Situation | Topology |
|---|---|
| Learning, upstream patches | T1 |
| One product, one main repo | T2 |
| Many products and shared repos released as a set | T3 |

## Config and environment
- `west config -l` shows `manifest.path`, `manifest.file`, `zephyr.base`.
- `zephyr.base` is the default for `ZEPHYR_BASE` while west runs, but an already-set
  `ZEPHYR_BASE` overrides it unless `zephyr.base-prefer` is `configfile`. An exported value
  pointing elsewhere builds against a different tree; unset it unless intended.
- Several workspaces can share a git object cache: `west update --path-cache`, `--name-cache`
  or `--auto-cache` (or the `update.*-cache` config options) saves disk and CI time.
- West never changes the manifest repository's contents after `west init`; update it with
  ordinary git commands.

## Verify
- [ ] `west init` plus `west update` from a clean machine reproduces the build with no manual steps.
- [ ] `echo $ZEPHYR_BASE` is empty or points into this workspace.
- [ ] Release tags on the manifest repo resolve every project to a SHA.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed the T1/T2/T3 topology definitions and layouts (west workspaces page), west init -m/--mr/-l usage and that west does not change the manifest repository after init (basics and built-in pages), zephyr.base and zephyr.base-prefer semantics (west config page), update cache options (west/app/project.py), and that zephyrproject-rtos/example-application exists (active, not archived). Removed the unconfirmed per-workspace venv advice and corrected the ZEPHYR_BASE precedence.
Method: documentation only; no commands were run.
