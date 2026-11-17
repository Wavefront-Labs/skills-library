---
id: computing-software.software-engineering.go.integer-conversion-and-overflow
name: integer-conversion-and-overflow
category: computing-software
field: software-engineering
product: go
tags: [go, go-types-values, go-numeric-overflow, integer-overflow, conversion]
level: practitioner
status: docs-checked
description: "Convert between Go numeric types safely: wraparound, float to int truncation, and bounds checks before narrowing."
sources:
  - https://go.dev/ref/spec#Conversions
  - https://go.dev/ref/spec#Arithmetic_operators
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Integer conversion and overflow in Go

**Goal:** never silently truncate or wrap a value you got from outside your process.

Per the Go spec, integers are two's complement and overflow at run time does not panic: signed `+`, `-`, `*`, `/` and `<<` overflow to a deterministically defined value, and unsigned `+`, `-`, `*` and `<<` are computed modulo 2^n, so programs may rely on wrap-around. Converting between integer types sign-extends (signed) or zero-extends (unsigned) the value to infinite precision and then truncates it to the result size, and "there is no indication of overflow". Converting a float to an integer discards the fraction (truncation toward zero); if the result type cannot represent the value, the conversion succeeds but the result is implementation-dependent.

```go
func toInt32(n int64) (int32, error) {
    if n < math.MinInt32 || n > math.MaxInt32 {
        return 0, fmt.Errorf("value %d out of int32 range", n)
    }
    return int32(n), nil
}

// adding sizes from untrusted input
func safeAdd(a, b uint64) (uint64, bool) {
    c := a + b
    return c, c >= a // false means it wrapped
}
```

Example from the spec: with `v := uint16(0x10F0)`, `uint32(int8(v)) == 0xFFFFFFF0`: the narrowing to `int8` truncates, then the sign extension fills the high bits.

## Gotchas
- `len(x)` is `int`; converting it to `uint32` for a wire format needs a bounds check first, because the conversion never reports overflow.
- Integer division: if the dividend is the most negative value of its `int` type, `x / -1` equals `x` (two's-complement overflow) rather than panicking; a zero divisor at run time panics.
- Never convert an out-of-range float to an integer and rely on the value.

## Verify
Table-test boundaries (`MaxInt32`, `MaxInt32+1`, `-1` to unsigned) and confirm the helper returns an error, not a wrapped value.

## Checked
Checked 2026-11-08 against the Go specification (Conversions between numeric types, Arithmetic operators, Integer overflow, Integer operators) on the single-page spec.
Removed as not confirmed in the spec: `math/big` and `math/bits` carry helpers, `strconv.Atoi` versus `ParseInt` remarks, the gosec G115 rule, the untrusted `make` size note, shift-count behaviour, and the compile-time constant overflow sentence.
Method: documentation only; no commands were run.
