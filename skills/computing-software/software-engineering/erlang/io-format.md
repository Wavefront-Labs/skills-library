---
id: computing-software.software-engineering.erlang.io-format
name: io-format
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-text, io-format]
level: intro
status: docs-checked
description: "Erlang io:format control sequences: ~p ~w ~s ~ts ~B ~f ~e ~c ~n, field width, ~P depth and io_lib:format."
sources:
  - https://www.erlang.org/doc/apps/stdlib/io.html
  - https://www.erlang.org/doc/apps/stdlib/io_lib.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# io:format directives and iolists
**Goal:** format output correctly.

```erlang
io:format("~p ~w ~s ~ts~n", [{a,"b"}, ok, "txt", "ünï"]),
io:format("~.2f ~e ~B ~.16B ~c~n", [3.14159, 1.5, 255, 255, $x]),
io:format("~10s|~-10s|~n", ["right", "left"]),
Bin = unicode:characters_to_binary(io_lib:format("~p", [Term])).
```
- `~p` writes like `~w` but breaks long terms over lines and indents them, and prints flat printable lists as strings. `~w` writes the standard syntax. `~s` prints a string (iolist, binary or atom); with the `t` modifier (`~ts`) it takes Unicode chardata. `~B` writes an integer in base 2-36 (default 10; the precision selects the base, `~.16B`). `~f` fixed float (default precision 6). `~e` scientific float. `~c` a character code. `~n` newline. `~~` writes a tilde.
- General form `~F.P.PadModC`: a negative field width `F` left-justifies; if the width is too small the field is filled with `*`. `*` takes the value from the next argument.
- `~P`, `~W` take an extra argument, the maximum depth, below which terms print as `...`.
- `io_lib:format/2` returns a character list (`chars()`, possibly deep) instead of printing.
- For logging use `logger`, not `io:format`.
- If an error occurs, `io:format` produces no output; for example `~s` with an integer argument raises a bad-argument error.

## Gotchas
- `~s` with a list containing integers above 255 is an error unless the `t` modifier is used.

## Self-check
Print a nested record-like term with `~p` and `~P` depth 2.

## Checked

2026-11-03. Confirmed in the `io` page (control sequences `~p ~w ~s ~B ~f ~e ~c ~n ~~ ~P ~W`, `t` modifier, field width, padding, `*`, error behaviour) and the `io_lib` page (`format/2`, `chars()`). Removed: the `badarg` wording for count mismatch and the `lists:flatten/1` advice. `unicode:characters_to_binary/1` is listed in the `unicode` module page.
Method: documentation only; no commands were run.
