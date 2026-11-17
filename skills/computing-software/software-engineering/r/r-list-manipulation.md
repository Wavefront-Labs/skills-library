---
id: computing-software.software-engineering.r.r-list-manipulation
name: r-list-manipulation
category: computing-software
field: software-engineering
product: r
tags: [r, r-lists, list-manipulation]
level: practitioner
status: draft
description: "Create, append, flatten and traverse nested lists with base R and purrr."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building, flattening and traversing lists
- Append with `lst[[length(lst) + 1]] <- x` or `c(lst, list(x))`; growing in a loop is O(n^2), preallocate with `vector("list", n)`.
- `unlist()` flattens, coerces to a common type and creates dotted names; `purrr::list_flatten()` flattens one level.
- `rapply()` applies to leaves; `purrr::pluck(lst, "a", 2, "b")` digs into nested structures, returning NULL if absent.
- `modifyList(defaults, user)` merges settings recursively.
Verify: `str(lst, max.level = 2)` to inspect the shape.
