---
id: computing-software.software-engineering.refactoring.rename-variable
name: rename-variable
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, rename-variable, naming, first-set-refactorings, encapsulate-variable]
level: practitioner
status: draft
description: "Rename a variable safely by scope: local, parameter, field or widely published variable, with IDE rename, encapsulation first for wide scopes, and good naming rules."
sources: ["https://refactoring.com/catalog/renameVariable.html", "https://martinfowler.com/books/refactoring.html", "https://www.jetbrains.com/help/idea/rename-refactorings.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rename Variable

Fowler: "naming things well is the heart of clear programming." Rename as soon as you understand
a variable better than its name says.

## By scope
- **Local or lambda parameter**: IDE rename (Shift+F6 IntelliJ, F2 VS Code, Ctrl+R,R Visual Studio,
  `:LspRename`). Run tests. Commit.
- **Function parameter**: rename is local to the function, but check for keyword-argument callers
  (Python `f(old_name=...)`, C# named args, Kotlin named args); those are part of the signature, so
  use Change Function Declaration with a deprecation period for public APIs.
- **Field / module-level variable used widely**: first **Encapsulate Variable** (getter/setter or
  property), rename the backing variable, then rename the accessor in stages.
- **Published (other teams, serialized, config keys)**: add the new name, read both, write new,
  migrate, remove old. Renaming a serialized field without this breaks stored data and clients.
- Constants: you can rename by copying `NEW = OLD`, migrating references, then deleting `OLD`.

## Naming checklist
- Name says what it holds in domain terms: `remaining_seats`, not `n` or `data2`.
- Short names fine for tiny scopes (`i` in a 3-line loop); longer for wider scopes.
- Units or kind where ambiguous: `timeout_ms`, `price_pence`, `user_ids` (plural for collections).
- Booleans read as predicates: `is_overdue`, `has_access`.
- Don't encode types (`strName`) or meaningless suffixes (`Info`, `Data`, `Obj`).

## Safety notes
- Dynamic languages: IDE rename can miss string-based access (`getattr`, `obj["name"]`, templates,
  reflection, ORM field names in strings). Grep after renaming: `rg -w old_name`.
- Renaming in a merge-heavy area: do it as its own commit/PR so reviewers see pure rename noise
  separately from behaviour changes (`git log --follow`, `git blame -w -C` still work).
