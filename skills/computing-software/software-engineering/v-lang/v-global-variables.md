---
id: computing-software.software-engineering.v-lang.v-global-variables
name: v-global-variables
category: computing-software
field: software-engineering
product: v-lang
tags: [v-global-variables, const-and-globals, global, __global, enable-globals, global variable, shared state, v-lang]
level: practitioner
status: docs-checked
description: "Declare module globals with __global and compile with -enable-globals, and prefer passing state or using shared objects."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Global variables and -enable-globals

Goal: use globals deliberately (they are off by default).

- By default V does not allow global variables; V only allows defining variables in functions. Usage is enabled with the compiler flag `-enable-globals`, intended for low-level applications.
- Declarations must be surrounded with `__global ( ... )`:

```v
import sync

__global (
	sem   sync.Semaphore // needs initialization in `init()`
	mtx   sync.RwMutex // needs initialization in `init()`
	f1    = f64(34.0625) // explicitly initialized
	shmap shared map[string]f64 // initialized as empty `shared` map
	f2    f64 // initialized to `0.0`
)

fn init() {
	sem.init(0)
	mtx.init()
}
```
- An initializer must be explicitly converted to the target type; with no initializer a default initialization is done. Option and result globals can be declared by type (`__global current ?int`, `__global status !int`).
- Semaphores and mutexes need in-place initialization; a separate `init()` function is called before `main()` for that.
- In multi-threaded programs access is subject to race conditions. Approaches: `shared` types with `lock` blocks (best for structs, arrays, maps); atomics for primitives; explicit synchronization primitives such as mutexes; or ignoring races when exact values do not matter (the `rand` module does this).
- A local variable may not reuse the name of a global; V reports `error: variable `devices` shadows a global variable`. Rename the local.
- For read-only data use a constant (`const`) instead.

Verify: build with and without `-enable-globals` to confirm the error and the fix.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Global Variables", "Shadowing a global", "Variables", "Constants"). Removed as not stated there: the single-line `__global counter = 0` form, exceptions for low-level modules and scripts, advice for library authors, the test-flag note, dependency-order initialization of globals.

Method: documentation only; no commands were run.
