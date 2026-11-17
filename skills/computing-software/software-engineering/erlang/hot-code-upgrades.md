---
id: computing-software.software-engineering.erlang.hot-code-upgrades
name: hot-code-upgrades
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-releases, hot-code-upgrades]
level: sme
status: docs-checked
description: "Erlang hot upgrades: .appup instructions, code_change/3, relup generation and release_handler install and make_permanent."
sources:
  - https://www.erlang.org/doc/system/release_handling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Appup, relup and release_handler
**Goal:** understand the hot-upgrade workflow and when to avoid it.

```erlang
%% myapp.appup
{"1.1.0",
 [{"1.0.0", [{load_module, myapp_worker}]}],     % upgrade from
 [{"1.0.0", [{load_module, myapp_worker}]}]}.    % downgrade to
```
- The first element is the current application version, as in the `.app` file; then the list of versions to upgrade from, then the list to downgrade to. Version entries can also be regular expressions.
- `{load_module, M}` is simple code replacement for a functional module. `{update, M, {advanced, Extra}}` suspends the processes using M and makes behaviour processes call `code_change/3` with `Extra`. `{update, M, supervisor}` is for changing a supervisor's start specification.
- `{add_module, M}` loads a new module (required in embedded mode); `{delete_module, M}` unloads it and kills any process with M as residence module, so stop those processes first.
- Also available: `add_application`, `remove_application`, `restart_application`, `{apply, {M, F, A}}`, `restart_new_emulator` and `restart_emulator`.
- Generate the relup with `systools:make_relup/3,4` from the `.rel`, `.app` and `.appup` files; it normally needs no manual writing. The old and new `.app`, `.rel` and `.appup` and new `.beam` files must be in the code path (option `path`).
- Install on a running node: put the release package in the releases directory, then `release_handler:unpack_release(Name)` (returns `{ok, Vsn}`), `release_handler:install_release(Vsn)`, then `release_handler:make_permanent(Vsn)`. Until made permanent, a reboot returns to the old version. Downgrade by calling `install_release` with the older version.
- Requirements: the node runs as an embedded system with heart monitoring, uses a single `sys.config`, and every release except the first contains a `relup`.
- The manual recommends changing code in the smallest steps possible and keeping it backwards compatible.

## Gotchas
- Processes not affected keep running during the upgrade; new processes created between suspension and loading can run old code.
- The boot script in the package must be generated from the same `.rel` file as the package.
- Complex or circular dependencies between nodes, processes or modules can make upgrade order hard or impossible to get right.

## Self-check
Upgrade a test release from 1.0.0 to 1.1.0 and downgrade back before relying on it.

## Checked
Method: docs-checked 2026-11-09 against https://www.erlang.org/doc/system/release_handling.html (read in full). Dropped unconfirmed claims about rebar3 relup plugins and team preference for rolling restarts.
