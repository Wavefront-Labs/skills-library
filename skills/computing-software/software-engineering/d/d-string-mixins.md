---
id: computing-software.software-engineering.d.d-string-mixins
name: d-string-mixins
category: computing-software
field: software-engineering
product: d
tags: [d-string-mixins, mixins, string-mixin, mixin, code-generation, ctfe-string, token-string, metaprogramming, d]
level: advanced
status: docs-checked
description: "Generate D code from compile-time strings with mixin(), build strings in CTFE with ~, token strings q{}, pragma(msg) and the -mixin switch."
sources:
  - https://dlang.org/spec/expression.html
  - https://dlang.org/spec/lex.html
  - https://dlang.org/dmd-linux.html
  - https://dlang.org/spec/pragma.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String mixins: mixin("...") and code generation

Goal: generate declarations and statements at compile time.

```d
string getter(string t, string n) {
    return t ~ " " ~ n ~ "() const { return _" ~ n ~ "; }";
}
struct P { private int _x; mixin(getter("int", "x")); }
```
- Each argument is evaluated at compile time and must be representable as a string; several arguments are concatenated, and the text must compile as a valid expression, e.g. `mixin("x +", 1) * 7`.
- A mixin can also be a statement or declaration depending on where it appears, e.g. `mixin("return x;")`.
- Print generated source while developing: `pragma(msg, getter("int","x"));` (a pragma argument is evaluated with CTFE).
- Token strings: `q{ int a = 1; }` must contain valid D tokens, and `{`/`}` inside nest.
- Compose with `static foreach` over `__traits(allMembers, T)` to generate wrappers/serialisers.

Gotchas:
- `-mixin=filename` expands and saves mixins to that file, so you can read the generated code.
- Prefer templates or `static if` when sufficient; mixin strings are hard to maintain.

Verify: `dmd -mixin=expanded.d m.d` and inspect the generated code.

## Checked
Checked 2026-11-03 against the D spec Expressions page (Mixin Expressions), the Lexical page (token strings), the pragma page (`pragma msg`) and the dmd command-line page (`-mixin`). Removed: the `std.format` remark and the claim that mixed-in code sees locals as written (not stated there).

Method: documentation only; no commands were run.
