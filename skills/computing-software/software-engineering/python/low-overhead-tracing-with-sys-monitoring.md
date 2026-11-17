---
id: computing-software.software-engineering.python.low-overhead-tracing-with-sys-monitoring
name: low-overhead-tracing-with-sys-monitoring
category: computing-software
field: software-engineering
product: python
tags: [python, py-profiling, sys-monitoring, pep-669, python-312, coverage-tools, tracing, debugger-api]
level: advanced
status: docs-checked
description: "Build coverage, profilers or debuggers on sys.monitoring (PEP 669, Python 3.12+): tool ids, events, callbacks, DISABLE for per-location opt-out and 3.14 branch events."
sources: ["https://docs.python.org/3/library/sys.monitoring.html", "https://peps.python.org/pep-0669/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Low-overhead tracing with sys.monitoring

`sys.monitoring` (PEP 669) delivers callbacks when events of interest occur during execution.

```python
import sys
mon = sys.monitoring
TOOL = mon.PROFILER_ID                       # DEBUGGER_ID 0, COVERAGE_ID 1, PROFILER_ID 2, OPTIMIZER_ID 5
mon.use_tool_id(TOOL, "my-tracer")           # ValueError if the id is already in use
E = mon.events

seen = set()
def on_line(code, line_number):
    seen.add((code.co_filename, line_number))
    return mon.DISABLE                       # disable this event for this code location only

def on_call(code, instruction_offset, callable_, arg0):
    print("call", getattr(callable_, "__name__", callable_))

mon.register_callback(TOOL, E.LINE, on_line)
mon.register_callback(TOOL, E.CALL, on_call)
mon.set_events(TOOL, E.LINE | E.CALL)        # global activation
# per code object: mon.set_local_events(TOOL, some_function.__code__, E.LINE)

# ... run the code under observation ...

mon.set_events(TOOL, mon.events.NO_EVENTS)
mon.free_tool_id(TOOL)                       # 3.14 also calls clear_tool_id() first
```

## Rules from the docs
- Tool ids are 0 to 5 inclusive. Use `use_tool_id` before using an id; `get_tool(tool_id)` returns its name or None.
- To monitor an event, turn it on (`set_events` globally and/or `set_local_events` per code object) and register a callback. An event triggers once even if on both globally and locally.
- Events are bit flags: combine with `|`. `NO_EVENTS` (0) deactivates all.
- Returning any object other than `DISABLE` from a callback has no effect.
- `DISABLE` turns off a local event for the current code location only. The docs call this very important for high-performance monitoring, e.g. a debugger that disables everything except its breakpoints. `restart_events()` re-enables all events disabled this way, for all tools.
- `register_callback` returns any callback it replaces; passing `None` unregisters.

## Events and callback signatures
- Local events (can be disabled per location): `PY_START`, `PY_RESUME`, `PY_RETURN`, `PY_YIELD`, `CALL`, `LINE`, `INSTRUCTION`, `JUMP`, `BRANCH_LEFT`, `BRANCH_RIGHT`, `STOP_ITERATION`.
- `BRANCH` is deprecated in 3.14; `BRANCH_LEFT`/`BRANCH_RIGHT` perform better because they can be disabled independently.
- `C_RETURN` and `C_RAISE` are controlled by `CALL`: they are only seen if `CALL` is monitored.
- Other events, not disabled per location: `PY_THROW`, `PY_UNWIND`, `RAISE`, `EXCEPTION_HANDLED`, `RERAISE` (3.15 adds per code object disabling).
- `STOP_ITERATION` exists so tools can see real exceptions without slowing generators, since CPython 3.12+ does not raise an artificial StopIteration unless it would be visible.
- Signatures: `LINE` is `(code, line_number)`; `CALL`/`C_RETURN`/`C_RAISE` are `(code, instruction_offset, callable, arg0)` with `arg0` set to `sys.monitoring.MISSING` when there are no arguments; `PY_START`/`PY_RESUME`/`INSTRUCTION` are `(code, instruction_offset)`; `PY_RETURN`/`PY_YIELD` add `retval`; exception events add `exception`; `BRANCH_*`/`JUMP` add `destination_offset`.

## Verify
- [ ] `seen` includes the executed lines of a small fixture function after one call.

## Checked
Date: 2026-11-03. Confirmed against the `sys.monitoring` documentation (tool ids, `use_tool_id` ValueError, `free_tool_id` change in 3.14, events and categories, `DISABLE`, `restart_events`, `register_callback`, callback signatures). Removed as unconfirmed: coverage.py behaviour, settrace cost comparison, thread-safety and PyPy claims, `co_positions`/`dis` mapping, overhead benchmark, "RuntimeError" for taken ids.
Method: documentation only; no commands were run.
