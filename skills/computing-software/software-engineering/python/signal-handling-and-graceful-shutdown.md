---
id: computing-software.software-engineering.python.signal-handling-and-graceful-shutdown
name: signal-handling-and-graceful-shutdown
category: computing-software
field: software-engineering
product: python
tags: [python, py-process-control, signal-handling, sigterm, sigint, graceful-shutdown, add-signal-handler, windows]
level: practitioner
status: docs-checked
description: "Handle SIGINT and SIGTERM for clean shutdown in scripts, threads and asyncio: main-thread rule, add_signal_handler, flags vs exceptions and Windows limits."
sources: ["https://docs.python.org/3/library/signal.html", "https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.add_signal_handler"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signal handling and graceful shutdown

Handle SIGTERM so in-flight work finishes.

## Plain script
```python
import signal, threading
stop = threading.Event()

def on_signal(signum, frame):
    stop.set()                          # do almost nothing here: set a flag

signal.signal(signal.SIGTERM, on_signal)
signal.signal(signal.SIGINT, on_signal)

while not stop.is_set():
    do_unit_of_work()
    stop.wait(1.0)                      # wakes immediately when set
cleanup()
```
Ctrl-C already raises `KeyboardInterrupt` in the main thread; catching SIGTERM and turning it into the same path keeps one cleanup route.

## asyncio
```python
import asyncio, signal
async def main():
    loop = asyncio.get_running_loop()
    stop = asyncio.Event()
    for s in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(s, stop.set)        # must be called from the main thread
    task = asyncio.create_task(serve())
    await stop.wait()
    task.cancel(); await asyncio.gather(task, return_exceptions=True)
```
Python 3.11+ `asyncio.Runner` installs its own SIGINT handler that cancels the main task on Ctrl-C, then `Runner.run` raises `KeyboardInterrupt`; a second Ctrl-C raises it immediately.

## Rules
- Python handlers run in the **main thread**, at a later point (for example the next bytecode instruction), not inside the C-level handler; `signal.signal` and `set_wakeup_fd` called from other threads raise `ValueError`.
- A long C call may delay handlers; use timeouts. `time.sleep` is restarted after a handler returns (PEP 475, 3.5).
- Do almost nothing in handlers: set a flag, or use `signal.set_wakeup_fd`.
- Reset: `signal.signal(sig, signal.SIG_DFL)` restores the default action.

## Windows
`signal.signal` can only be called with SIGABRT, SIGFPE, SIGILL, SIGINT, SIGSEGV, SIGTERM or SIGBREAK; any other signal raises `ValueError`. `loop.remove_signal_handler` is documented as Unix-only, so on Windows use `signal.signal` with `loop.call_soon_threadsafe`.

## Gotchas
- Catching synchronous faults such as SIGSEGV or SIGFPE in Python handlers makes little sense (Python may return to the faulting C code and appear to hang); use `faulthandler` to report them.

## Verify
- [ ] `kill -TERM <pid>` (or `docker stop`) completes in-flight work and exits 0 within the grace period.
- [ ] A test sends the signal via `os.kill` to a subprocess and asserts the cleanup marker file.

## Checked

- 2026-11-03: checked against the CPython docs `library/signal.rst`, `library/asyncio-eventloop.rst` and `library/asyncio-runner.rst`: deferred execution of Python handlers, main-thread restrictions, Windows signal list, `SIG_DFL`, `set_wakeup_fd`, `loop.add_signal_handler` main-thread rule, `Runner` SIGINT handling (3.11), PEP 475 sleep retry.
- Removed: container PID 1, tini/`--init`, shell `exec` and child-process forwarding advice, the claim that `add_signal_handler` is unimplemented on Windows (the docs read mark only `remove_signal_handler` as Unix).

Method: documentation only; no commands were run.
