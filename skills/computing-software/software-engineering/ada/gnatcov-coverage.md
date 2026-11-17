---
id: computing-software.software-engineering.ada.gnatcov-coverage
name: gnatcov-coverage
category: computing-software
field: software-engineering
product: ada
tags: [ada, gnatcov-coverage]
level: advanced
status: docs-checked
description: "Measure statement, decision and MC/DC coverage of Ada with gnatcov instrument, a gprbuild of the instrumented sources, and gnatcov coverage."
sources:
  - https://raw.githubusercontent.com/AdaCore/gnatcoverage/master/doc/gnatcov/src_traces.rst
  - https://raw.githubusercontent.com/AdaCore/gnatcoverage/master/doc/gnatcov/cov_source.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Coverage with GNATcoverage (source instrumentation)
Flow for a native program, from the GNATcoverage manual (source-trace chapters):
```
gnatcov instrument -P app.gpr --level=stmt+decision --dump-trigger=atexit
gprbuild -P app.gpr --src-subdirs=gnatcov-instr --implicit-with=gnatcov_rts
./main
gnatcov coverage --level=stmt+decision -P app.gpr --annotate=html <trace>.srctrace
```
- `gnatcov instrument --level=<> <units-of-interest>`: `--level` is the strictest criterion you can assess later; units of interest come from the project file. Projects marked `Externally_Built` are not instrumented. Use `gnatcov instrument --help` for your release's options.
- The build step passes `--src-subdirs=gnatcov-instr` and `--implicit-with=<runtime project>` to gprbuild. The default coverage runtime project is `gnatcov_rts`; `gnatcov setup --install-name=...` installs it under another name (then name that project in `--implicit-with`).
- `--dump-trigger` chooses where the trace is written: `manual`, `atexit`, `main-end` or `ravenscar-task-termination`; the default depends on the installed runtime. `--dump-channel` is `bin-file` (default; creates a `.srctrace` file) or `base64-stdout`. `atexit` with `bin-file` is the natural choice for a native program with a full Ada runtime. `main-end` can miss data if the program exits abruptly or tasks are still running when the main subprogram ends.
- Trace files are named `<ename>-<istamp>-<pid>-<estamp>.srctrace` by default; the `--dump-filename-*` switches change that.
- `gnatcov coverage --level=<criterion> --annotate=<format>`: levels are `stmt`, `stmt+decision` and `stmt+mcdc` and `stmt+uc_mcdc`; formats include `report`, `html`, `xcov`, `xcov+`, `xml`, `cobertura` and `sarif`. `--output-dir` places the output.
- `-jN` parallelises instrumentation within one `gnatcov instrument` run. Concurrent `gnatcov instrument` commands are not supported when their project closures share projects (write races); run those in sequence.
## Gotchas
- Flags change between gnatcov releases; the manual lists the options of the current release and `gnatcov instrument --help` shows yours.
- Instrument and coverage must use the same or compatible `--level` (a `stmt` instrumentation cannot answer a `stmt+mcdc` query).
## Self-check
Run a test and open the HTML report for uncovered lines.

## Checked
Checked against the GNATcoverage manual sources (src_traces.rst and cov_source.rst in the AdaCore/gnatcoverage repository: instrumentation command line, dump triggers and channels, gprbuild options, coverage levels and report formats).
Removed: the `-gnata` Pre/Post advice, the DO-178C remark, the `*.srctrace` glob (the manual passes trace files or a `@file` list) and the original learn.adacore.com source (not read).
Method: docs-only read of cited pages, 2026-11-08
