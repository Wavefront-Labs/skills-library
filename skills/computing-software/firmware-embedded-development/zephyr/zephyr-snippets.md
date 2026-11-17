---
id: computing-software.firmware-embedded-development.zephyr.zephyr-snippets
name: zephyr-snippets
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-build-system, zephyr-snippets, snippet-yml, west-build-s, cdc-acm-console, rtt-console, reusable-config, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use and write Zephyr snippets to apply reusable Kconfig + devicetree bundles (RTT console, CDC-ACM console, debug options) across boards with west build -S."
sources:
  - https://docs.zephyrproject.org/latest/build/snippets/index.html
  - https://docs.zephyrproject.org/latest/build/snippets/using.html
  - https://docs.zephyrproject.org/latest/build/snippets/writing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zephyr snippets

**Goal:** switch on a cross-cutting configuration (logging over RTT, console over USB,
extra debug) for any board without editing the app's `prj.conf` or adding per-board overlays.

## Using a snippet
```
west build -b nrf52840dk/nrf52840 -S rtt-console app/
west build -b <board> -S cdc-acm-console -S rtt-tracing app/   # several
```
With CMake directly, use the `SNIPPET` variable, a whitespace- or semicolon-separated list:
`cmake -Sapp -Bbuild -DSNIPPET="snippet1;snippet2"`. The docs have a "Built-in snippets" page listing what
Zephyr ships. Upstream examples (directories under `snippets/`): `rtt-console`, `cdc-acm-console`,
`rtt-tracing`, `xen-dom0`, and board-family ones such as `nordic/nordic-ppr`.

## Writing one
A `snippet.yml` file placed anywhere under a `snippets/` subdirectory of a directory listed in
`SNIPPET_ROOT` (the zephyr repository is always included; add more with `-DSNIPPET_ROOT=`), or under
`snippets/` of a module whose `module.yml` sets `settings: snippet_root: .`. Paths in the file are relative to
the directory containing `snippet.yml`:
```yaml
name: my-debug
append:
  EXTRA_CONF_FILE: debug.conf
  EXTRA_DTC_OVERLAY_FILE: debug.overlay
boards:
  nrf52840dk:                    # board name
    append:
      EXTRA_DTC_OVERLAY_FILE: nrf52840dk.overlay
  /stm32.*/:                     # regex in slashes; must match the whole board name
    append:
      EXTRA_CONF_FILE: stm32-debug.conf
```
`debug.conf`:
```
CONFIG_ASSERT=y
```
Board-specific settings apply in addition to the common ones, and a board entry can carry `revisions:`
(for example `"0.7.0":`) applied on top. `append:` also accepts `DTS_EXTRA_CPPFLAGS` and, for sysbuild,
`SB_EXTRA_CONF_FILE`. Multiple files can be given as a YAML list. In devicetree overlays prefix labels and
node names with `snippet_<name>` or `snippet-<name>` to avoid clashes.

## When to use what
| Mechanism | Scope |
|---|---|
| `prj.conf` / app overlay | the app on all boards |
| `boards/<board>.conf/.overlay` in the app | the app on one board |
| snippet | a reusable feature across apps and boards, opt-in at build time |
| shield | a physical add-on board |

## Gotchas
- Snippets are processed in the order of the `-S` arguments (or the `SNIPPET` list); when two set the same
  symbol, the one processed last wins, for both `.conf` fragments and overlays.
- Check the merged `.config` and `zephyr.dts` in the build directory to see what ended up in the build.

## Verify
- [ ] `build/zephyr/.config` contains the snippet's symbols.
- [ ] `build/zephyr/zephyr.dts` contains the snippet's overlay nodes (e.g. chosen console).

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- `west build -S`, `-DSNIPPET`, snippet search locations (`SNIPPET_ROOT`, `module.yml` `snippet_root`), `append:` keys,
  board-name and regex matching (whole name), revisions, namespacing and processing order (doc: build/snippets/using and
  /writing); snippet directory names (`snippets/` tree: `rtt-console`, `cdc-acm-console`, `rtt-tracing`, `xen-dom0`, `nordic/nordic-ppr`).
- Wrong or removed: `xen_dom0` (the directory is `xen-dom0`), the `set(SNIPPET ...)` in `CMakeLists.txt` recipe, the
  `west build -t snippets` listing command, `<app>/snippets/` as an automatic search path, the board key with a qualifier
  (`nrf52840dk/nrf52840`; the docs show plain board names), the duplicate-name error, the `prj.conf` ordering remark, the
  "needs `-p`" remark and the `CONFIG_DEBUG_OPTIMIZATIONS` / `CONFIG_LOG_DEFAULT_LEVEL` example lines (no source read).

Method: documentation only; no commands were run.
