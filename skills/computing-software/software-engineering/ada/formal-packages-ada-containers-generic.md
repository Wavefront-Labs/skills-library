---
id: computing-software.software-engineering.ada.formal-packages-ada-containers-generic
name: formal-packages-ada-containers-generic
category: computing-software
field: software-engineering
product: ada
tags: [ada, formal-packages-ada-containers-generic]
level: advanced
status: draft
description: "Ada generic formal packages, signature packages and nested generic instantiation patterns."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/advanced-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Formal packages and generic constraints
```ada
generic
   with package P is new Ada.Containers.Vectors (<>);
package Helper is ... end Helper;
```
- `(<>)` after `new` accepts any instance of that generic.
- Pass a whole instance instead of many type parameters: it keeps related types consistent.
- Ada 2022 adds formal container aspects and more flexible `<>` rules (version support in GNAT: unconfirmed).
## Gotchas
- Deeply nested generics inflate compile time and code size.
## Self-check
Pass a vectors instance to Helper and call P.Append inside it.
