---
id: computing-software.database-administration.sqlite.loading-extensions
name: loading-extensions
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, load-extension, sqlite-extensions, sqlite3-shell, sqlite-security]
level: practitioner
status: verified
description: "Load SQLite run-time extensions (.load, load_extension(), sqlite3_load_extension) such as math, vector or spatial modules, and keep extension loading safe."
sources:
  - https://sqlite.org/loadext.html
  - https://sqlite.org/c3ref/enable_load_extension.html
  - https://sqlite.org/lang_corefunc.html#load_extension
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loading extensions

## In the shell
```text
.load ./vec0                -- file name without suffix works; platform suffix (.so/.dylib/.dll) added
.load ./spellfix1 sqlite3_spellfix_init   -- explicit entry point if non-standard
```

## From application code
Extension loading is disabled by default for security. Enable only the C API path, not the SQL function:
```c
sqlite3_db_config(db, SQLITE_DBCONFIG_ENABLE_LOAD_EXTENSION, 1, NULL);   /* C API only */
sqlite3_load_extension(db, "./vec0", NULL, &err);
```
Run through ctypes on 3.50.4: `sqlite3_load_extension` returned 1 with `not authorized` before enabling; after `sqlite3_db_config(db, SQLITE_DBCONFIG_ENABLE_LOAD_EXTENSION /* 1005 */, 1, NULL)` it returned 0 (SQLITE_OK) for the sqlite-vec DLL.
Python:
```python
import sqlite3
con = sqlite3.connect("app.db")
con.enable_load_extension(True)
con.load_extension("./vec0")
con.enable_load_extension(False)
```
(The Python docs say some platforms, notably macOS, ship Python with extension loading disabled by default; use a build that supports it.)

## The SQL function
`SELECT load_extension('./x')` works only when enabled with `sqlite3_enable_load_extension()`. Never enable that on connections that run user-supplied SQL: an attacker could load any shared library. In Python 3.14 (SQLite 3.50.4) the call failed with `not authorized` before `enable_load_extension(True)` and again after `enable_load_extension(False)`; the 3.54.1 sqlite3 shell allowed `select load_extension('./vec0')` directly (the shell enables extension loading itself).

## Common extensions
- Math functions (`sin`, `log`, `power`) are built in since 3.35 when compiled with `SQLITE_ENABLE_MATH_FUNCTIONS` (shell has them).
- Bundled in the source tree `ext/misc` (files `csv.c`, `series.c`, `uuid.c`, `regexp.c`, `fileio.c`, `decimal.c`, `spellfix.c` exist on GitHub; the spellfix module is `spellfix1`); `generate_series` worked in the 3.54.1 shell without loading anything.
- Third party: `sqlite-vec` (vector search), SpatiaLite (`mod_spatialite`), `sqlean` collection.

## Auto-loading
`sqlite3_auto_extension()` registers statically linked extensions for every new connection, better than file loading in production builds.

## Gotchas
- Pass an explicit path (`./vec0`) so the loader does not search elsewhere. Tested on Windows with the sqlite-vec 0.1.9 wheel: `.load ./vec0`, `.load ./vec0 sqlite3_vec_init` and `.load ./vec0.dll` all worked in the 3.54.1 shell, and `con.load_extension("./vec0")` worked in Python.
- The suffix is added automatically if omitted (loadext.html).

## Verify
After loading, a function from the extension works (`SELECT vec_version();`); with loading disabled, `SELECT load_extension('x')` returns `not authorized`.
