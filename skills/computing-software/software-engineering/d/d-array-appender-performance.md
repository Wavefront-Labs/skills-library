---
id: computing-software.software-engineering.d.d-array-appender-performance
name: d-array-appender-performance
category: computing-software
field: software-engineering
product: d
tags: [d-array-appender-performance, std-array, array-performance, reserve, appender, concatenation, assumesafeappend, profile-gc, stopwatch, allocation, d]
level: advanced
status: docs-checked
description: "Profile array building: reserve capacity, use Appender, avoid ~ in loops, reuse buffers with assumeSafeAppend, and measure with StopWatch and -profile=gc."
sources:
  - https://dlang.org/phobos/std_array.html
  - https://dlang.org/phobos/object.html
  - https://dlang.org/dmd-linux.html
  - https://dlang.org/phobos/std_datetime_stopwatch.html
  - https://dlang.org/phobos/std_outbuffer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Array performance: reserve, appender and avoiding repeated concatenation

Goal: cut GC allocations when building data.

1. Measure first: `dmd -O -inline -release -profile=gc app.d`, run, and read `profilegc.log`.
2. Preallocate when the size is known: `auto a = new int[](n);` or `Appender!(int[]) app; app.reserve(n);`.
3. Replace repeated `s ~= x` in hot loops with `appender` from `std.array`.
4. Reuse a buffer: `buf.length = 0; buf.assumeSafeAppend();` only when nothing else uses the memory beyond the slice (the page warns that elements in use beyond the array get overwritten).
5. Keep pipelines lazy until the last step; `copy` into an appender (an output range) instead of building temporary arrays.
6. Strings: `appender!string` with `formattedWrite`; `std.outbuffer.OutBuffer` for binary or text output.
7. Time sections with `std.datetime.stopwatch.StopWatch` (`sw.peek.total!"msecs"`) or `benchmark!f(n)` from the same module.

Gotchas:
- Benchmarks without the optimisation switches (`-O -inline -release`) mislead.
- `reserve` does nothing if the requested capacity is not larger than the current one.

Verify: compare `profilegc.log` totals before and after.

## Checked

2026-11-03. Confirmed against: std.array (Appender, reserve), object (`assumeSafeAppend`, `reserve`), the DMD switches page (`-profile=gc`, `-O`, `-inline`, `-release`), std.datetime.stopwatch and std.outbuffer.

Removed because the pages read did not confirm it: the single-expression `s ~ x ~ y ~ z` claim, `std.benchmark`-like wording, 'reserve returns capacity / may not extend shared slice' gotcha, `each!(a => app.put(a))`.

Method: documentation only; no commands were run.
