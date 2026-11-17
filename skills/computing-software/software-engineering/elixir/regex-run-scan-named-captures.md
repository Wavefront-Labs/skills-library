---
id: computing-software.software-engineering.elixir.regex-run-scan-named-captures
name: regex-run-scan-named-captures
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, regex, regex-run, regex-scan, named-captures, pcre, regex-replace, regex-usage]
level: practitioner
status: docs-checked
description: "Use ~r sigils with Regex.run/scan/replace/named_captures, anchors and flags; it is PCRE and nested quantifiers can hit backtracking limits."
sources: ["https://hexdocs.pm/elixir/Regex.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regex: run, scan, named captures

**Goal:** extract and rewrite text with regexes safely.

```elixir
Regex.match?(~r/^\d+$/, "123")
Regex.run(~r/(\d+)-(\d+)/, "10-20")         #=> ["10-20", "10", "20"]
Regex.scan(~r/\d+/, "a1b22")                 #=> [["1"], ["22"]]
Regex.named_captures(~r/(?<y>\d{4})-(?<m>\d\d)/, "2026-11")  #=> %{"y" => "2026", "m" => "11"}
Regex.replace(~r/(\w+)@(\w+)/, "me@host", "\\2:\\1")   #=> "host:me"
Regex.split(~r/[,;]\s*/, "a, b;c")
Regex.compile!("a" <> Regex.escape(user_input))
~r/foo/iu    # i caseless, u unicode, m multiline, s dotall, x extended, U ungreedy
```

## Rules
- `Regex` is based on PCRE and built on Erlang's `:re`. With the `m` flag `^` and `$` match at each line; use `\A` and `\z` for the start and end of the string.
- The `u` flag enables Unicode patterns like `\p` and makes classes such as `\w` and `\s` match Unicode characters.
- Use `Regex.escape/1` when embedding a literal string in a pattern.
- Nested quantifiers such as `~r/(a+)+$/` can hit the engine's backtracking limit (catastrophic backtracking); the Regex docs say the functions then raise `SystemLimitError` (since Elixir v1.21) instead of returning no match.
- In `Regex.replace/4` string replacements, `\\N` or `\\g{N}` insert capture N and `\\0` the whole match.

## Self-check
`Regex.run(~r/\d+/, "abc")` returns `nil`.

## Checked
2026-11-03: confirmed against the Elixir Regex docs (PCRE over `:re`, flags i u m s x U, `\A` and `\z`, `escape/1`, `run`, `scan`, `named_captures`, `replace` with `\\N`, `split`, `compile!`, backtracking limit and `SystemLimitError`). Removed: the claims that `$` allows a trailing newline, that `\d` becomes Unicode-aware, that `~r` is compiled with the module, and the NimbleParsec advice.
Method: documentation only; no commands were run.
