---
id: computing-software.systems-network-administration.varnish-cache.vcl-load-use-discard
name: vcl-load-use-discard
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [vcl-load, vcl-use, vcl-discard, vcl-temperature]
level: practitioner
status: docs-checked
description: "Deploy VCL without downtime using varnishadm: vcl.load, vcl.inline, vcl.use, vcl.list status and temperature, vcl.show, vcl.state and vcl.discard."
sources:
  - https://www.varnish.org/docs/reference/varnish-cli/
  - https://www.varnish.org/docs/users-guide/run_cli/
  - https://www.varnish.org/docs/users-guide/vcl-backends/
  - https://www.varnish.org/docs/reference/varnishd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# vcl load use discard

```bash
varnishadm vcl.load v2 /path/to/new.vcl [auto|cold|warm]   # compile and load
varnishadm vcl.use v2                                      # make it active
varnishadm vcl.list
varnishadm vcl.show -v v2
varnishadm vcl.discard v1
```

`vcl.load` compiles the file under the given name; a compile error leaves the running VCL untouched. `vcl.inline` takes VCL via a here document (the `<<` needs a blank before the delimiter word). `vcl.use` accepts a config name or a label.

`vcl.list` columns: status (`active`, `available`, `discarded`), state (`label`, `cold`, `warm`, `auto`), temperature (`init`, `cold`, `warm`, `busy`, `cooling`), a busy reference count, and the name. `vcl.state` forces auto, cold or warm. `vcl.discard` accepts patterns and unloads labels and configs in dependency order; discarded VCLs cool after `vcl_cooldown` (default 600s) before being freed. `vcl.deps` shows dependencies and `vcl.symtab` dumps the symbol tables.

Probes keep running for every loaded VCL, so unload old ones.

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: the unsupported systemctl reload claim; added vcl-backends and varnishd sources.

Method: documentation only; no commands were run.
