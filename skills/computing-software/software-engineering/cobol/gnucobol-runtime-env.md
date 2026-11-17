---
id: computing-software.software-engineering.cobol.gnucobol-runtime-env
name: gnucobol-runtime-env
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, gnucobol-runtime-env, cobol-compiler-gnucobol, cob-library-path, cob-file-path, runtime-config, cob-set-debug]
level: advanced
status: docs-checked
description: "Control the GnuCOBOL runtime with COB_ environment variables and the runtime.cfg file."
sources:
  - https://gnucobol.sourceforge.io/doc/gnucobol.html
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GnuCOBOL runtime environment variables (COB_*)
**Goal:** configure file paths, module paths and debugging without recompiling.

Run-time settings (runtime.cfg appendix of the GnuCOBOL manual):
- `COB_LIBRARY_PATH` paths for dynamically loadable modules; the default paths `.` and the install `extras` directory are always added.
- `COB_FILE_PATH` default location of data files (default: current directory).
- `COB_SET_TRACE` (boolean) enables the trace feature; `COB_TRACE_FILE` is where trace output goes (default stderr; a leading `+` opens it for append); `COB_TRACE_FORMAT` formats each line.
- `COB_SET_DEBUG` enables USE ON DEBUGGING procedures that were compiled in under WITH DEBUGGING MODE.
- `COB_RUNTIME_CONFIG` names a runtime configuration file; the initial runtime.cfg is read from `COB_CONFIG_DIR` (see `cobcrun --info` for the path).
- `COB_CORE_ON_ERROR` and `COB_CORE_FILENAME` control core dumps.
- In runtime.cfg, `${envvar:default}` expands environment variables, `setenv`/`unsetenv`/`include`/`includeif`/`reset` are directives, and real environment variables win over the file.

File name mapping: with `filename-mapping: yes` (the default in default.conf), `ASSIGN TO "DATAFILE"` is resolved from the environment variable `DD_DATAFILE`, then `dd_DATAFILE`, then `DATAFILE`, then the literal name.

Compile time (cobc): `COB_COPY_DIR` (copybook folder, also `COBCPY`), `COB_CONFIG_DIR`, `COB_CC`, `COB_CFLAGS`, `COB_LDFLAGS`, `COB_LIBS`, `COB_LDADD`.
```bash
export COB_LIBRARY_PATH=./modules
export DD_CUSTIN=data/customers.dat
./main
```

## Gotchas
- Relative paths resolve against the current directory.
- `cobcrun -r` (`--runtime-conf`) prints every current setting with its origin; `cobcrun -i` prints runtime information.

## Self-check
Run `cobcrun -r`, change a `DD_` mapping and rerun the program to see the other file used.

## Checked
2026-11-02. Checked against the GnuCOBOL manual and Programmer's Guide (runtime and compile-time environment variables, ASSIGN file location strings, cobcrun options) and config/runtime.cfg and default.conf from the GnuCOBOL source. Removed: `COB_COPY_EXT` (not in the docs), the claim that variable names are case sensitive or changed between 2.2 and 3.x, and the `--info` form for cobc runtime paths.

Method: documentation only; no commands were run.
