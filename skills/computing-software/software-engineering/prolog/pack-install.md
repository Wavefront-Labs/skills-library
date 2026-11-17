---
id: computing-software.software-engineering.prolog.pack-install
name: pack-install
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-deploy, pack-install, pack-list]
level: practitioner
status: docs-checked
description: "Install, list, upgrade, remove and attach SWI-Prolog packs with library(prolog_pack) and the swipl pack command."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/library/prolog_pack.pl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packs
```prolog
?- pack_install(PackName).               % name looked up at swi-prolog.org
?- pack_install(PackName, [upgrade(true)]).
?- pack_list(Query).                     % case-insensitive match on name/title
?- pack_info(PackName).
?- pack_remove(PackName).
```
```bash
swipl pack install PackName
```
- `pack_install/1,2` accepts a pack name, an archive file, an http(s) URL (may contain `*`), an https git URL, a `file://` URL, or `.` which creates a symbolic link to the working directory.
- `pack_upgrade(Pack)` is `pack_install(Pack, [upgrade(true)])`. Options of `pack_install/2` include `interactive(Bool)`, `insecure(Bool)` and `rebuild(Condition)` for foreign components.
- `pack_remove/1,2` takes `interactive(false)` and dependency handling options.
- Attach installed packs with `attach_packs/1,2` or `pack_attach(+PackDir, +Options)`; PackDir holds `pack.pl` and a `prolog/` directory.
- `pack.pl` declares dependencies with `requires/1` and capabilities with `provides/1`.
## Gotchas
- A pack must be attached before `use_module(library(Name))` finds its files.
- Installing from an unverified URL runs build steps; prefer the pack list and review the source.
## Self-check
After installing, `pack_info(PackName)` shows the pack and `use_module(library(...))` loads from it.

## Checked

2026-11-03. SWI-Prolog library(prolog_pack) documentation and source (prolog_pack.pl): pack_install/1,2 accepted sources and options, pack_list/1, pack_info/1, pack_remove/1,2, pack_upgrade/1, attach_packs/1,2, pack_attach/2, pack.pl requires/provides, the command line `swipl pack install`. Removed: the specific third-party pack examples, "user pack directory" location, version-pinning advice and the `if_/3` self-check.

Method: documentation only; no commands were run.
