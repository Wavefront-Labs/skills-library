---
id: computing-software.software-engineering.go.zero-copy-strings-with-unsafe-string-and-slice
name: zero-copy-strings-with-unsafe-string-and-slice
category: computing-software
field: software-engineering
product: go
tags: [go, go-unsafe-reflect, go-unsafe-string, unsafe-string, unsafe-slice, zero-copy]
level: sme
status: docs-checked
description: "Convert between []byte and string without copying using unsafe.String, unsafe.StringData and unsafe.Slice, and know the immutability contract."
sources:
  - https://pkg.go.dev/unsafe#String
  - https://pkg.go.dev/unsafe#Slice
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zero-copy conversions with unsafe.String and unsafe.Slice

**Goal:** avoid a copy in a proven hot path while keeping Go's immutable-string guarantee.

```go
func BytesToString(b []byte) string {
    if len(b) == 0 { return "" }
    return unsafe.String(&b[0], len(b))              // Go 1.20+
}
func StringToBytes(s string) []byte {
    if len(s) == 0 { return nil }
    return unsafe.Slice(unsafe.StringData(s), len(s)) // read-only view!
}
```

Contract (from the `unsafe` package docs): since Go strings are immutable, the bytes passed to `unsafe.String` must not be modified as long as the
returned string exists, and the bytes returned by `unsafe.StringData` must not be modified. So after `BytesToString(b)`, never write to `b` while the
string is reachable, and never write to the slice from `StringToBytes`. `unsafe.String` and `unsafe.StringData` were added in Go 1.20; `unsafe.Slice` in Go 1.17.

Prefer the safe copy unless a benchmark shows the conversion matters.

## Gotchas
- Never apply to memory that will be reused (for example a pooled buffer) while the string is still alive.
- The string keeps the whole backing array reachable.
- Document the invariant at the function and add a benchmark proving the win; remove the unsafe code when it does not pay.

## Checked
2026-11-09. Confirmed on pkg.go.dev/unsafe: signatures of `String`, `StringData`, `Slice`, the do-not-modify rules for String and StringData, and the
"added in" versions (String and StringData go1.20, Slice go1.17). Removed claims the page does not state: compiler copy-elision cases, `strings.Builder`
internals, `bytes.Buffer.String()` copying, read-only-memory fault behaviour, map-corruption consequences, and the benchmark allocation expectation.
Method: documentation only; no commands were run.

## Verify
Benchmark with `-benchmem` and check that your API never lets the source buffer be mutated after conversion (you own the buffer and do not reuse it).
