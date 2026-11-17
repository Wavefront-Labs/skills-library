---
id: computing-software.software-engineering.go.strings-bytes-and-runes
name: strings-bytes-and-runes
category: computing-software
field: software-engineering
product: go
tags: [go, go-strings, runes, utf-8, strings-builder, bytes-package, effective-go, go-strings-text, go-strings-builder]
level: practitioner
status: verified
description: "Handle text in Go correctly: strings as immutable UTF-8 bytes, runes and range iteration, byte vs rune indexing, strings.Builder, bytes vs strings packages and conversion costs."
sources: ["https://go.dev/blog/strings", "https://go.dev/ref/spec#String_types", "https://pkg.go.dev/strings", "https://pkg.go.dev/unicode/utf8"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Strings, bytes and runes

**Goal:** text code that is correct for non-ASCII input and doesn't allocate needlessly.

## The model
- A `string` is an immutable sequence of **bytes**, conventionally UTF-8. `len(s)` is bytes.
- A `rune` is an `int32` Unicode code point. `[]rune(s)` decodes; `string(r)` encodes.
- `s[i]` is a byte; slicing `s[a:b]` is by byte offsets (can cut a multi-byte character).

```go
s := "héllo, 世界"
len(s)                          // 14 bytes
utf8.RuneCountInString(s)       // 9 runes
for i, r := range s {           // range decodes UTF-8: i = byte offset, r = rune
    fmt.Println(i, string(r))
}
s[1]                            // 0xc3: first byte of 'é', not a character
```
Invalid UTF-8 bytes decode as `utf8.RuneError` (U+FFFD) in range loops; validate external
input with `utf8.ValidString`.

## Truncation and width
Truncate on rune boundaries:
```go
func truncate(s string, n int) string {
    if utf8.RuneCountInString(s) <= n { return s }
    i := 0
    for j := range s { if i == n { return s[:j] }; i++ }
    return s
}
```
User-perceived characters (grapheme clusters like emoji with modifiers) need
`github.com/rivo/uniseg`. Case-insensitive comparison: `strings.EqualFold`, not `ToLower` both sides (`EqualFold("ς", "Σ")` is true, `ToLower("ς") == ToLower("Σ")` is false).

## Building strings
```go
var b strings.Builder
b.Grow(64)
for _, item := range items {
    fmt.Fprintf(&b, "%s=%d;", item.Key, item.N)
}
out := b.String()          // no copy
```
`+=` in a loop is O(n^2). `strings.Join` for slices. `bytes.Buffer` when you need an
`io.Reader`/`io.Writer` over bytes.

## strings vs bytes
The `bytes` package mirrors `strings` (`Contains`, `Split`, `Fields`, `TrimSpace`, `Cut`) for
`[]byte`. Stay in one type through a pipeline: each `string(b)`/`[]byte(s)` conversion copies
(the compiler elides some cases, e.g. map lookups `m[string(b)]` and comparisons).

## Handy functions
`strings.Cut(s, "=")` (split once, returns found bool), `strings.Fields` (split on whitespace),
`strings.NewReplacer` (many replacements in one pass), `strings.Lines`/`SplitSeq` (Go 1.24
iterators), `strconv.Quote` for safe display, `unicode.IsLetter`.

## Verify
- [ ] Code that indexes or slices strings is either byte-oriented by design or rune-safe.
- [ ] Tests include multi-byte input (accents, CJK, emoji).

## Checked
- Go 1.25.1: the 14-byte/9-rune example and per-index output, `s[1]` is `0xc3`, invalid UTF-8 ranges as `U+FFFD` (`[97 65533 98]`) and fails `utf8.ValidString`, the `truncate` helper and a mid-character slice, `strings.Builder` with `Fprintf`, `Cut`, `Fields`, `NewReplacer`, `Lines` and `SplitSeq` (1.24 notes), `string(rune)`; `strings.EqualFold("ς", "Σ")` is true while comparing `ToLower` of both is false. `uniseg` was not run.
