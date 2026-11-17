---
id: computing-software.software-engineering.elixir.sigils-builtin-custom
name: sigils-builtin-custom
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, sigil, r, w, s, d, t, u, n, sigil-custom, sigils]
level: practitioner
status: docs-checked
description: "Use built-in sigils for regex, word lists, dates and strings and define custom sigil_x functions."
sources: ["https://hexdocs.pm/elixir/sigils.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sigils and custom sigils

**Goal:** choose the right sigil and write your own, following the Elixir sigils guide.

```elixir
~r/foo|bar/i                      # regular expression (PCRE); `i` makes it case insensitive
~w(foo bar bat)a                  # [:foo, :bar, :bat]; modifiers c, s, a pick charlists, strings, atoms
~s(a string with "double" quotes) # string
~c(a charlist with "double" quotes)
~D[2019-10-31]  ~T[23:00:07.0]  ~N[2019-10-31 23:00:07]  ~U[2019-10-31 19:59:03Z]

defmodule MySigils do
  def sigil_i(string, []), do: String.to_integer(string)
  def sigil_i(string, [?n]), do: -String.to_integer(string)
end
import MySigils
~i(13)    #=> 13
~i(42)n   #=> -42
```

## Rules
- Sigils start with `~`, then a letter, then a delimited string, then optional modifiers. There are 8 delimiters: `/`, `|`, `"`, `'`, `(`, `[`, `{`, `<` (closing pair as expected); pick one that avoids escaping, such as `~r(^https?://)`. Heredoc delimiters (three double or single quotes) also work.
- Uppercase textual sigils (`~S`, `~C`, `~W`) do no interpolation or escaping; most lowercase sigils have an uppercase variant. `@doc ~S"""` avoids double escaping in documentation.
- Calendar sigils: `~D` (Date), `~T` (Time), `~N` (NaiveDateTime), `~U` (UTC DateTime).
- `~r/foo/i` is equivalent to calling `sigil_r(<<"foo">>, [?i])`. A custom sigil is a function following the `sigil_{character}` pattern that receives the string and a charlist of modifiers; import its module to use it.
- Custom sigil names may be a single lowercase character, or an uppercase character followed by more uppercase characters and digits.
- See the `Regex` module for the full list of regex modifiers.

## Self-check
`~w(foo bar)a` gives `[:foo, :bar]`.

## Checked
Date: 2026-11-02. Confirmed against the Elixir sigils guide (~r with PCRE and i modifier, 8 delimiters, ~s ~c ~w modifiers, uppercase variants, calendar sigils, sigil_ functions, custom naming). Removed: m s x u regex modifier list (see Regex docs), ~C interpolation detail beyond the guide, wrong ~w(a b)c self-check, date examples.
Method: documentation only; no commands were run.
