---
id: computing-software.software-engineering.prolog.iso-error-terms
name: iso-error-terms
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, iso-error-terms, type-error-domain-error]
level: practitioner
status: draft
description: "Raise standard error(Formal, Context) terms with type_error/2, domain_error/2, existence_error/2 and must_be/2."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ISO error terms
Standard shape: `error(Formal, Context)`. Formals: `instantiation_error`, `type_error(Type, Culprit)`, `domain_error(Dom, Culprit)`, `existence_error(Kind, What)`, `permission_error(Action, Type, Culprit)`, `representation_error(What)`, `evaluation_error(What)`, `resource_error(R)`, `syntax_error(M)`.
```prolog
:- use_module(library(error)).
pos(X) :- must_be(positive_integer, X).
fail_type(X) :- type_error(integer, X).
?- catch(nosuchpred(1), error(existence_error(procedure, PI), _), true).
```
## Gotchas
- Unknown procedure throws `existence_error(procedure, Name/Arity)` unless the `unknown` flag is changed or the predicate is declared dynamic.
- Always add a Context via the library helpers so messages localise.
## Self-check
Call an undefined predicate, catch the error, and print its indicator.
