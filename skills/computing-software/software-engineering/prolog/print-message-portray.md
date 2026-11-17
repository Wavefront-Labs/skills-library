---
id: computing-software.software-engineering.prolog.print-message-portray
name: print-message-portray
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, print-message-portray, prolog-message]
level: advanced
status: docs-checked
description: "Report through print_message/2 with prolog:message//1, intercept with message_hook/3 and customise printing with portray/1."
sources:
  - https://www.swi-prolog.org/pldoc/man?predicate=print_message/2
  - https://www.swi-prolog.org/pldoc/man?predicate=portray/1
  - https://www.swi-prolog.org/pldoc/man?predicate=print/1
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Messages and portray
```prolog
:- multifile prolog:message//1.
prolog:message(my_error(X)) --> [ 'Bad value: ~w'-[X] ].
?- print_message(error, my_error(7)).
:- multifile user:portray/1.
user:portray(secret(_)) :- write('<hidden>').
```
- Message kinds: `silent`, `informational`, `warning`, `error`, `banner`, `debug(Topic)`. `silent` messages are normally not printed.
- `message_hook(+Term, +Kind, +Lines)` intercepts messages: if it succeeds the message counts as printed (use it to show silent messages, suppress or redirect messages).
- Libraries should report through `print_message/2` with a message term, not `format/3`; translate the term with `prolog:message//1`.
- `portray/1` is called by `print/1` for each non-variable subterm; if it succeeds the term is considered written. `print/1` defaults to `[portray(true), numbervars(true), quoted(true)]` (or the flag `print_write_options`), and `~p` in `format/2` calls `print/1`.
## Gotchas
- `write/1` does not call `portray/1`; `print/1` does.
- `informational` messages and the banner are suppressed by setting the flag `verbose` to `silent` (`swipl -q`).
- Lists are passed to `portray/1` only as a whole.
## Self-check
Define a custom message, print it with `print_message(error, ...)` and confirm it appears on `user_error`; then intercept it with `message_hook/3`.

## Checked

2026-11-03. SWI-Prolog manual section 4.11 "Printing messages" (kinds, message_hook/3, prolog:message//1 example, verbose=silent, -q), portray/1 and print/1 and write_term/2 default options, format/2 `~p`. Removed: message_to_codes (not documented), the claim that portray affects the toplevel (not in the pages read) and the "error: prefix" self-check.

Method: documentation only; no commands were run.
