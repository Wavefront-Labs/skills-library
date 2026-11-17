---
id: computing-software.software-engineering.prolog.consult-load-files
name: consult-load-files
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-loading, consult-load-files, make-reload]
level: intro
status: draft
description: "Load source with consult/1, [file], load_files/2, ensure_loaded/1, reload with make/0 and find files with file_search_path."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Loading code
```prolog
?- [user].                     % type clauses, end with Ctrl-D
?- consult('family.pl').       % same as [family]
?- ensure_loaded(library(lists)).
?- make.                       % reload files modified on disk
?- prolog_load_context(directory, D).
user:file_search_path(app, '/opt/app').   % then use_module(app(util))
```
`swipl file.pl` starts the toplevel with the file loaded; `swipl -g main -t halt file.pl` runs main then exits.
## Gotchas
- Reconsulting a file replaces its clauses; clauses from another file for the same predicate cause "redefine" prompts unless multifile.
- `include/1` splices text; `load_files` with `if(not_loaded)` avoids reloading.
## Self-check
Edit a loaded file, run `make.`, and confirm the new definition is active.
