---
id: computing-software.software-engineering.concurrency.string-building-and-parsing-performance
name: string-building-and-parsing-performance
category: computing-software
field: software-engineering
product: concurrency
tags: [performance, string-performance, string-builder, parsing, allocations, regex-performance]
level: practitioner
status: gated
description: "Make string-heavy code fast: avoid quadratic concatenation, use builders and joins, reduce copies with spans and views, precompile regexes, and parse without intermediate strings."
sources: ["https://learn.microsoft.com/en-us/dotnet/standard/base-types/stringbuilder", "https://docs.python.org/3/faq/programming.html#what-is-the-most-efficient-way-to-concatenate-many-strings-together", "https://learn.microsoft.com/en-us/dotnet/standard/memory-and-spans/", "https://docs.rs/regex/latest/regex/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String building and parsing efficiency

## Concatenation in loops is quadratic
Strings are immutable in Java, C#, Python, JS, Go: `s += piece` in a loop copies the whole string
each time.
| Language | Use |
|---|---|
| Java (not run (gated: unconfirmed, source is paywalled or blocked)) | `StringBuilder` (presize: `new StringBuilder(expectedLen)`), `String.join`, `Collectors.joining` |
| C# (not run (gated: unconfirmed, source is paywalled or blocked)) | `StringBuilder`, `string.Join`, `string.Create` / interpolated string handlers for formatting |
| Python | collect pieces in a list, `"".join(parts)`; `io.StringIO` for streaming |
| Go | `strings.Builder` (with `Grow(n)`), `bytes.Buffer` |
| JS | array `.join("")` or template literals; V8 (Node 20) optimises `+=` with ropes: 1.6M appends of 10 chars took 95 ms with `+=`, 37 ms with `join`, and growth was sub-quadratic (measured) |
| Rust | `String::with_capacity`, `push_str`, `write!` into a `String` |
CPython has a refcount-1 `+=` optimisation that sometimes hides this; don't rely on it. Measured on Python 3.14 (Windows): `s += piece` took 11, 121, 573 and 2654 ms for 100k to 800k pieces versus 2 to 34 ms for `"".join`, and with a second reference to the old string it hit 25 s at 160k pieces. Go `s +=` for 2k to 16k pieces: 5.9, 30, 93, 405 ms (21 MB to 1.3 GB allocated per op) versus a presized `strings.Builder` at 18 to 83 us and 1 allocation.

## Avoid intermediate strings
- Slice without copying: C# `ReadOnlySpan<char>` / `AsSpan()`, Rust `&str`, Go substrings share
  memory (verified with `unsafe.StringData`: offset equals the slice start), C++ `std::string_view`, Java has no zero-copy substring (since 7u6 `substring` copies (gated: unconfirmed, source is paywalled or blocked)).
- Parse numbers from spans directly (`int.Parse(span)`, `Utf8Parser`, Rust `str::parse` on slices,
  `strconv.Atoi` on substrings).
- `split()` allocates an array of strings; for hot paths iterate with `indexOf`/`IndexOf`,
  `str::split` iterators (lazy in Rust), `MemoryExtensions.Split` into ranges (.NET 8+).
- Work in bytes when input is UTF-8 and you only need ASCII delimiters (avoid decode/encode cycles):
  .NET `Utf8JsonReader`, Go `bytes` package, Python `bytes` methods.
- Logging: use parameterised logging (`log.debug("x={}", x)`) so strings aren't built when disabled.

## Regex
- Compile once (`static final Pattern`, `RegexOptions.Compiled` or .NET source-generated `[GeneratedRegex]`,
  module-level `re.compile` (measured: 200k `re.match` calls took 77 ms versus 28 ms with a precompiled pattern, since `re` keeps an internal cache), Rust `LazyLock<Regex>`). Compiling per call dominates cost.
- Prefer simple string methods (`startsWith`, `contains`) when no pattern is needed.
- Catastrophic backtracking (`(a+)+$`, nested quantifiers) is a performance and ReDoS risk; use
  linear-time engines (RE2, Rust `regex`, Go `regexp` took 5.5 ms for `(a+)+$` against 80,000 characters in a run, .NET `RegexOptions.NonBacktracking` (gated: unconfirmed, source is paywalled or blocked)) for
  untrusted input, and set timeouts (`Regex.MatchTimeout`).

## Formatting and conversion
- Repeated `format`/`String.format` in hot loops is slow (parsing format strings); prefer builders
  or precompiled formatters.
- Case-insensitive compares: `equalsIgnoreCase`, `StringComparison.OrdinalIgnoreCase` instead of
  lowercasing both sides (allocations + culture bugs).
- Interning/caching repeated strings (`String.intern`, `sys.intern`, a dictionary) can cut memory for
  many duplicates (CSV columns, JSON keys).

## Measure
Allocation profilers (JFR, dotnet-counters/`dotnet-trace` alloc events, `tracemalloc`, Go `-benchmem`)
show string churn; microbenchmark changes with JMH/BenchmarkDotNet/`testing.B`.
