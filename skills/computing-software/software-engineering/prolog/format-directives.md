---
id: computing-software.software-engineering.prolog.format-directives
name: format-directives
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-format, format-directives, format-column]
level: practitioner
status: docs-checked
description: "Format output with format/2,3 directives for text, numbers, column stops and sinks in SWI-Prolog."
sources:
  - https://www.swi-prolog.org/pldoc/man?predicate=format/2
  - https://www.swi-prolog.org/pldoc/man?predicate=format/3
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# format/2 directives
```prolog
?- format("~w and ~q~n", [a, 'B c']).
?- format("~a: ~d~n", [count, 1234567]).      % ~D prints 1,234,567; ~2d on 314 prints 3.14
?- format("~2f ~e ~g~n", [3.14159, 2.5, 1.0]).
?- format("~t~w~10||~n", [right]).            % column stops with ~t and ~|
?- format(atom(A), "~p", [foo]), format("~*c~n", [3, 0'x]).
```
- Text: `~w` write, `~q` writeq, `~p` print, `~a` atom, `~s` text as code list, char list or string, `~c` character code.
- Numbers: `~d` takes an integer (`~Nd` inserts a decimal point N digits from the right; `~D` adds commas), `~e`, `~f`, `~g` floats (default 6 digits), `~r` and `~R` radix.
- Layout: `~n` newline, `~N` newline unless at line start, `~t` fill, `~|` and `~+` column stops, `~i` ignore an argument, `~*` takes the numeric argument from the argument list, `~@` calls a goal.
- `format/3` output sinks (`atom(A)`, `string(S)`, `codes(C)`) behave like `with_output_to/2`.
## Gotchas
- `~d` expects an integer; use `~f` for floats.
- Arguments must match the directives in number; a non-list single argument is accepted but deprecated, so use a list.
## Self-check
`format("~2f", [1.5])` prints 1.50 and `format("~D", [1234567])` prints 1,234,567.

## Checked

2026-11-03. SWI-Prolog manual format/2 page: directive table (~w ~q ~p ~a ~d ~D ~e ~f ~g ~s ~c ~r ~R ~i ~k ~n ~N ~@ ~W ~t ~| ~+ ~* ~I ~h), column handling, format/3 sinks, single non-list argument note. Removed: the exact error message text and "~d throws on float" phrasing (replaced by the documented requirement that the argument be an integer).

Method: documentation only; no commands were run.
