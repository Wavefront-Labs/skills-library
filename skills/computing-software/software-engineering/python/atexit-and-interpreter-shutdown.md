---
id: computing-software.software-engineering.python.atexit-and-interpreter-shutdown
name: atexit-and-interpreter-shutdown
category: computing-software
field: software-engineering
product: python
tags: [python, py-process-control, atexit-shutdown-hooks, atexit, weakref-finalize, interpreter-shutdown, del, cleanup]
level: practitioner
status: docs-checked
description: "Register cleanup with atexit and weakref.finalize, understand what runs on exit, signals, os._exit and crashes, and prefer finalizers over __del__."
sources: ["https://docs.python.org/3/library/atexit.html", "https://docs.python.org/3/library/weakref.html#weakref.finalize"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# atexit and interpreter shutdown

```python
import atexit, weakref, tempfile, shutil

tmp = tempfile.mkdtemp()
atexit.register(shutil.rmtree, tmp, ignore_errors=True)    # LIFO order, runs at normal exit

class Conn:
    def __init__(self):
        self._fin = weakref.finalize(self, self._close_raw, self.handle)   # runs on GC or at exit
    @staticmethod
    def _close_raw(handle): handle.close()                  # must not reference self
    def close(self): self._fin()                            # idempotent explicit close
```

## When atexit runs
Normal program termination: `sys.exit()` or the main module finishing, and more generally interpreter shutdown.
It does **not** run when the program is killed by a signal Python does not handle, on a fatal internal error, or on `os._exit()`.
Handlers run last-registered first; if one raises, a traceback is printed and the remaining handlers still run, then the last exception is re-raised. `atexit.unregister(fn)` removes one. Each interpreter has its own handler stack.

## Choosing
- Process-wide singleton cleanup (flush a log, remove a pid file): `atexit`.
- Per-object resources: context managers first, `weakref.finalize` as safety net.
- `__del__`: avoid for resources. `weakref.finalize` never runs its callback in the late part of shutdown when module globals may already be `None`, and exceptions in finalizers are only printed to stderr.

## Gotchas
- Since 3.12, starting a new thread or calling `os.fork` inside an exit handler raises `RuntimeError`.
- Registering or unregistering handlers from within a cleanup function is undefined.
- A finalizer created in a daemonic thread just as the program exits may not be called; neither `atexit.register` nor `try/finally` guarantees cleanup there.
- `weakref.finalize` objects still alive at exit are called in reverse order of creation unless their `atexit` attribute is false.

## Verify
- [ ] A subprocess test: run script, assert the cleanup effect (file removed) after normal exit and after `sys.exit(1)`.
- [ ] Document what is lost when the process is killed by a signal (stale pid files) and handle at next start-up.

## Checked

- 2026-11-03: checked against the CPython docs `library/atexit.rst` and `library/weakref.rst` (`finalize`): LIFO order, exception handling, cases where handlers do not run, 3.12 RuntimeError, per-interpreter stacks, `finalize` exit behaviour and `atexit` attribute, daemon thread caveat.
- Removed: non-daemon thread join order, fork/multiprocessing behaviour, `logging.shutdown` ordering, the KeyboardInterrupt and unhandled-exception claims and the exact RuntimeError text (not stated in the docs read).

Method: documentation only; no commands were run.
