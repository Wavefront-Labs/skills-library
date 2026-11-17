---
id: computing-software.software-engineering.prolog.janus-python
name: janus-python
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, janus-python, py-call]
level: advanced
status: draft
description: "Call Python from Prolog and Prolog from Python with library(janus): py_call/2, py_call/3 and the janus Python module (SWI-Prolog 9.1.x+)."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Janus
```prolog
:- use_module(library(janus)).
?- py_call(math:sqrt(16), X).              % X = 4.0
?- py_call(os:getcwd(), D).
?- py_call(builtins:len([1,2,3]), N).
```
```python
import janus_swi as janus
janus.query_once("member(X, [1,2,3])")        # {'truth': True, 'X': 1}
for d in janus.query("member(X, [1,2])"): print(d["X"])
```
Install the Python side with `pip install janus-swi` (needs SWI-Prolog built with shared library). Minimum SWI version is 9.1.x (exact minor unconfirmed).
## Gotchas
- Dicts map to Python dicts; lists to lists; strings to str.
- The GIL: Janus holds it while Python code runs from Prolog.
## Self-check
Call a Python function from Prolog and a Prolog predicate from Python in one session.
