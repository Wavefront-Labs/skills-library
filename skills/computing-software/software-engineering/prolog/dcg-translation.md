---
id: computing-software.software-engineering.prolog.dcg-translation
name: dcg-translation
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-dcg, dcg-translation, phrase-3]
level: practitioner
status: draft
description: "Write DCG rules with -->, terminals, pushback and {}/1, call phrase/2,3 and inspect the translation with listing."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DCG basics
```prolog
greeting --> [hello], name.
name --> [world].
name --> [prolog].
digits([D|T]) --> digit(D), digits(T).
digits([D]) --> digit(D).
digit(D) --> [D], { code_type(D, digit) }.
?- phrase(greeting, [hello, world]).
?- phrase(digits(Ds), `123`, Rest).    % Rest = []
```
- Each nonterminal gets two extra arguments (difference list in, rest out). `{}` embeds Prolog goals; `\+` negates; `!` cuts; `call//N`.
- Translation: `a --> b, [x].` becomes `a(S0,S) :- b(S0,S1), S1 = [x|S].`
## Gotchas
- Left recursion loops; restructure or use tabling.
- Use code lists (backquote) with `phrase/2`, not strings.
## Self-check
Run `listing(greeting)` to see the translated clause.
