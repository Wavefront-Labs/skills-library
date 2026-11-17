---
id: computing-software.software-engineering.go.strconv-parsing-and-formatting
name: strconv-parsing-and-formatting
category: computing-software
field: software-engineering
product: go
tags: [go, go-strings-text, go-strconv-parsing, strconv, parsing]
level: practitioner
status: docs-checked
description: "Parse and format numbers and booleans with strconv, handle *NumError, bit sizes and base prefixes."
sources:
  - https://pkg.go.dev/strconv
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# strconv parsing and formatting

**Goal:** turn text into numbers with explicit range and error handling.

```go
n, err := strconv.ParseInt("0x1f", 0, 32) // base 0 honours 0x, 0o, 0b prefixes
var ne *strconv.NumError
if errors.As(err, &ne) {
    switch {
    case errors.Is(ne.Err, strconv.ErrRange):  // not representable; n is the max-magnitude value for the size and sign
    case errors.Is(ne.Err, strconv.ErrSyntax): // not a number
    }
}
u, _ := strconv.ParseUint("300", 10, 8) // ErrRange; value is the maximum for the bit size
f, _ := strconv.ParseFloat("1e-3", 64)
s := strconv.FormatInt(-42, 2)   // "-101010"
q := strconv.Quote("a\tb")       // quoted with escapes
buf = strconv.AppendInt(buf[:0], 7, 10) // append form: writes into an existing []byte
```

`Atoi(s)` is equivalent to `ParseInt(s, 10, 0)` converted to `int`; `Itoa(i)` is `FormatInt(int64(i), 10)`. `ParseBool` accepts `1, t, T, TRUE, true, True, 0, f, F, FALSE, false, False`; any other value is an error. For base 0 only, underscores are permitted as in Go integer literals. Syntax errors (empty string or invalid digits) return 0 with `ErrSyntax`.

## Gotchas
- On `ErrRange` from `ParseInt` the returned value is the maximum magnitude for the bit size and sign, not zero; do not use it. `ParseFloat` returns `plus or minus Inf` with `ErrRange`.
- `ParseFloat(..., 32)` returns a float64 that converts to float32 without changing its value; convert explicitly.

## Verify
Table-test `""` (ErrSyntax), `"1_000"` with base 10 (not base 0, so underscores are not permitted), `"9223372036854775808"` (range) and assert the error kind with `errors.Is`.

## Checked
2026-11-03. Confirmed on pkg.go.dev/strconv: ParseInt base 0 prefixes and underscores, ErrSyntax/ErrRange return values, NumError and Unwrap (go1.14), Atoi and Itoa equivalences, ParseBool accepted values, ParseFloat bitSize 32 and ErrRange, Append* family. Removed: Itoa-vs-Sprintf speed claim, "zero-allocation" wording, the `+1` test case, and the hot-path claim in the description.
Method: documentation only; no commands were run.
