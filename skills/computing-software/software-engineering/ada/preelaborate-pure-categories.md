---
id: computing-software.software-engineering.ada.preelaborate-pure-categories
name: preelaborate-pure-categories
category: computing-software
field: software-engineering
product: ada
tags: [ada, preelaborate-pure-categories, ada-elaboration]
level: advanced
status: draft
description: "Categorisation pragmas that simplify elaboration: Pure, Preelaborate, Elaborate_Body, and what they forbid."
sources:
  - https://www.ada-auth.org/standards/
  - https://docs.adacore.com/gnat_ugn-docs/html/gnat_ugn/gnat_ugn.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pure, Preelaborate and Elaborate_Body
```ada
package Consts with Pure is ... end Consts;       -- no state, no side effects
package Tables with Preelaborate is ... end Tables; -- no dynamic init needing run-time calls
package P with Elaborate_Body is ... end P;       -- body elaborates right after spec
```
- `Pure` units can only depend on Pure units.
- `Preelaborate` forbids calls elaborating non-static code in the spec.
- Prefer `Elaborate_Body` when the spec initialises through its body.
## Gotchas
- Pure packages can be elaborated once and shared across partitions.
## Self-check
Add a global variable to a Pure package and read the error.
