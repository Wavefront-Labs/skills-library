---
id: computing-software.software-engineering.refactoring.moving-code-between-modules
name: moving-code-between-modules
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, move-module, move-class, package-structure, imports, re-exports]
level: practitioner
status: draft
description: "Move classes, functions and files between modules and packages safely: IDE moves, re-export shims for callers, import cycles, and staged moves across repositories."
sources: ["https://refactoring.com/catalog/moveFunction.html", "https://www.jetbrains.com/help/idea/move-refactorings.html", "https://docs.python.org/3/reference/import.html", "https://martinfowler.com/bliki/BranchByAbstraction.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Moving code between modules and packages

## Why move
Code lives where it is used and changed together: a function used only by `billing/` but sitting
in `common/utils.py`, a class whose package depends on half the codebase, or splitting a module
that two teams fight over.

## Inside one codebase
1. Use the IDE move (IntelliJ F6, Rider "Move to namespace/folder", VS Code TS move file/symbol,
   rope/PyCharm for Python, `gopls` for Go file moves). It rewrites imports.
2. Leave a **re-export shim** at the old location when callers are numerous or external:
   ```python
   # old_pkg/utils.py
   from new_pkg.dates import parse_date  # noqa: F401  (moved; remove after 2026-12)
   import warnings; warnings.warn("old_pkg.utils moved to new_pkg.dates", DeprecationWarning, stacklevel=2)
   ```
   TS: `export { parseDate } from "../dates";`  Java: keep a deprecated delegating class.
   C#: `[TypeForwardedTo]` across assemblies.
3. Migrate callers in batches (a codemod for big counts), then delete the shim.
4. Move tests with the code.

## Import cycles
Moving code often creates cycles (`a` imports `b`, now `b` needs `a`). Fix by moving the shared
part lower, dependency inversion, or passing collaborators in. Check with `madge --circular`,
import-linter, ArchUnit before merging.

## Move = pure commit
Make the move a commit with no other changes so git detects renames (`git log --follow`,
`git diff -M`) and reviewers can skip it. Large moves: tell people before, merge fast (moves
conflict with every open branch).

## Across repositories / packages
Copy into the new package, publish it, switch callers, then delete from the old one (or make the
old module depend on and re-export the new package for a release). To keep history:
`git filter-repo --path src/dates/ --path-rename src/dates/:dates/` then merge into the target repo.

## Serialized names
Moving classes changes fully qualified names used by Java serialization, pickle, Jackson polymorphic
type ids, message type headers, DI registrations by name. Keep aliases or explicit type ids.
