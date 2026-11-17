---
id: computing-software.software-engineering.v-lang.v-test-fixtures-and-benchmarks
name: v-test-fixtures-and-benchmarks
category: computing-software
field: software-engineering
product: v-lang
tags: [v-test-fixtures-and-benchmarks, testing, table test, fixture, testsuite_begin, benchmark, stopwatch, testing.bench, mock, tmpdir, v-lang]
level: practitioner
status: draft
description: "Set up and tear down test state, write table-driven tests with arrays of structs, and time code with time.StopWatch."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fixtures, table tests and benchmarking

Goal: scale tests beyond single asserts.

- Setup/teardown per file: `fn testsuite_begin() { ... }` and `fn testsuite_end() { ... }`.
- Table-driven: `cases := [Case{'a', 1}, Case{'b', 2}]; for c in cases { assert f(c.in) == c.want, 'case ${c.in}' }`.
- Temp files: `dir := os.join_path(os.temp_dir(), 'vtest_${os.getpid()}')`, `os.mkdir_all(dir)!`, `defer { os.rmdir_all(dir) or {} }`.
- Mocking: depend on interfaces and pass fakes.
- Benchmarks: `import time; sw := time.new_stopwatch(); ...; println(sw.elapsed().milliseconds())`; the `benchmark` module offers `benchmark.start()` / `.measure()` (confirm).
- Randomness: seed explicitly in tests (`rand.seed([u32(1), 2])`).

Gotchas:
- Tests run in one process per file; global state leaks between functions in a file.
- Benchmark only with `-prod` or you measure debug overhead.

Verify: run the table twice with `v test .` and see stable results.
