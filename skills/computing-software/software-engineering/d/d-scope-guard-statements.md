---
id: computing-software.software-engineering.d.d-scope-guard-statements
name: d-scope-guard-statements
category: computing-software
field: software-engineering
product: d
tags: [d-scope-guard-statements, statements, scope-exit, scope-failure, scope-success, scope-guard, raii, finally, cleanup, d]
level: practitioner
status: docs-checked
description: "Pair acquire and release with scope(exit)/scope(failure)/scope(success) statements, plus try/catch/finally ordering and with-statements."
sources:
  - https://dlang.org/spec/statement.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# scope(exit), scope(success), scope(failure)

Goal: keep cleanup next to acquisition.

```d
auto f = File("out.txt", "w");
scope(exit) f.close();          // always
scope(failure) remove("out.txt"); // only on exception
scope(success) writeln("done");  // only on normal exit
```
- Guards run in reverse order of declaration, at scope end (block, function, loop iteration).
- `scope(failure)` runs only on exception unwinding; `scope(exit)` runs on both normal exit and unwinding; `scope(success)` only on normal exit.
- `with (obj) { field = 1; }` opens a scope (also for enums: `with (Color) x = red;`).
- `try { } catch (SpecificEx e) { } catch (Exception e) { } finally { }`; order specific to general.

Gotchas:
- A guard runs at the close of its enclosing scope, not where it is written, so a guard in a loop body runs each iteration.

Verify: write a unittest recording call order in an array and assert it is the reverse of registration.

## Checked

Date 2026-11-02. Confirmed scope(exit), scope(success), scope(failure) semantics (Statements spec). Removed unconfirmed @nogc and captured-variable remarks.

Method: documentation only; no commands were run.
