---
id: computing-software.software-engineering.prolog.dict-basics
name: dict-basics
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-dicts, dict-basics, functional-notation]
level: practitioner
status: draft
description: "Create and read dicts with Tag{k: v}, get_dict/3, put_dict/4, dict_pairs/3 and the Dict.key functional notation."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dicts
```prolog
?- D = _{name: "Ana", age: 30}, X = D.name.            % functional notation in clause bodies
?- get_dict(age, _{age: 30}, A).
?- put_dict(city, _{a: 1}, "Oslo", D2).
?- D = point{x: 1, y: 2}, dict_pairs(D, Tag, Pairs).
?- X = _{a: 1}.put(b, 2).                              % built-in put method
```
- Dicts are ordered by key; tag may be unbound (`_`).
- Dot-call is expanded in clause bodies at compile time.
## Gotchas
- `.` functional notation does not work in directives that are not expanded, nor on unbound dicts; missing key throws `existence_error(key, ...)`.
- A trailing `.` after `D.name` may be misread: leave whitespace before the clause-ending period.
- Dicts are a SWI-Prolog 7+ extension, not portable to ISO systems.
## Self-check
Update a field in a nested dict with `put_dict` and read it back with `get_dict`.
