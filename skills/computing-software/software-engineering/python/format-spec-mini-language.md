---
id: computing-software.software-engineering.python.format-spec-mini-language
name: format-spec-mini-language
category: computing-software
field: software-engineering
product: python
tags: [python, py-text, format-spec-mini-language, f-strings, str-format, number-formatting, alignment]
level: practitioner
status: docs-checked
description: "Format numbers, widths, alignment, padding, signs, thousands separators, percentages and dates with the format-spec mini-language, f-strings and nested fields."
sources: ["https://docs.python.org/3/library/string.html#format-specification-mini-language", "https://docs.python.org/3/reference/lexical_analysis.html#f-strings"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Format spec mini-language

Grammar: `[[fill]align][sign][z][#][0][width][grouping][.precision][type]` (3.14 also allows `grouping` after the precision, for the fractional part).

```python
x, name = 1234567.891, "ada"
f"{x:,.2f}"        # '1,234,567.89'   grouping + fixed
f"{x:_.0f}"        # '1_234_568'      underscore grouping
f"{0.256:.1%}"     # '25.6%'
f"{42:08.3f}"      # '0042.000'
f"{42:+d}"         # '+42'
f"{255:#06x}"      # '0x00ff'   ; 'b' binary, 'o' octal, 'e' scientific, 'g' general
f"{name:>10}|{name:^10}|{name:*<10}"   # right, centre, left with '*' fill
f"{x:{12}.{3}f}"   # nested fields: width and precision from variables
f"{name!r:>8}"     # conversion (!r !s !a) runs before the spec
from datetime import datetime
f"{datetime(2026,11,3):%Y-%m-%d}"      # datetime defines its own spec: strftime codes
f"{x = }"          # '=' debug specifier (3.8+)
```

## Gotchas
- For strings, precision is the maximum field size: `f"{'abcdef':.3}" == 'abc'`; precision is not allowed for integer types.
- For `f` the result is correctly rounded to the given digits after the decimal point, using the same rounding mode as the `round` builtin for `float` (the current context's mode for `Decimal`).
- `z` (3.11+, PEP 682) coerces negative zero floats to positive zero after rounding, and is only valid for floating-point types.
- Literal braces are doubled in f-strings and `str.format`: `f"{{x}}"`.
- Python 3.12 removed many f-string restrictions: nested strings, comments and backslashes are now permitted in expressions.
- Format strings can reference attributes and items (`'{0.weight}'`, `'{0[0]}'`), so do not accept format strings from untrusted users.
- `,` and `_` give fixed separators; the `n` type gives a locale-aware one.

## Verify
- [ ] Doctest key cases (negative numbers, zero, large numbers).
- [ ] Locale-sensitive output uses `n` deliberately; otherwise `,`/`_` produce stable output.

## Checked

- 2026-11-03: checked against the CPython docs `library/string.rst` (format specification grammar, `z` 3.11, `_` 3.6, grouping on the fraction 3.14, precision, `%` type, rounding sentence, nested fields, attribute access examples), `library/datetime.rst` (`__format__` equals `strftime`) and `reference/lexical_analysis.rst` (f-strings, debug specifier 3.8, 3.12 changes).
- Removed: the `2.675` half-even claim, the exact `format(-0.0, 'z.1f')` result, the PEP 701 name and the 3.11 SyntaxError claim, the logging advice and the `Decimal`-for-money advice (not in these pages).

Method: documentation only; no commands were run.
