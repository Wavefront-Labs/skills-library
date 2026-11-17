---
id: computing-software.software-engineering.erlang.try-catch
name: try-catch
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-errors, try-catch]
level: practitioner
status: docs-checked
description: "Erlang exception classes error, exit and throw: try-of-catch-after syntax, raising, re-raising and stacktraces."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# try, catch, throw, error and exit
**Goal:** handle failures narrowly and keep the stacktrace.

```erlang
try parse(X) of
    {ok, V} -> V
catch
    throw:{bad, Why} -> {error, Why};          % non-local return by convention
    error:badarg -> {error, badarg};
    Class:Reason:Stack ->
        logger:error("failed: ~p ~p", [Reason, Stack]),
        erlang:raise(Class, Reason, Stack)
after
    cleanup()
end.
```
- Classes: `error` (run-time errors, `error/1`), `exit` (`exit/1`), `throw` (`throw/1`, for non-local returns).
- `Class:Reason:Stack` binds the stacktrace in the catch clause; `erlang:get_stacktrace/0` has been removed.
- `catch Expr` is deprecated. It returns `{'EXIT', {Reason, Stack}}` for errors, `{'EXIT', Term}` for exits and `Term` for throws, so the class is lost.
- Only exceptions in the `Exprs` part are caught; exceptions in the `of` bodies are not.
- `after` runs for cleanup after either path; its value is discarded. An exception raised inside `after` is not caught and masks any earlier one.

## Gotchas
- Catching everything (`_:_`) turns bugs into silent returns; match specific reasons.

## Self-check
Trigger each class and print `Class`, `Reason` and the top stack frame.

## Checked
2026-11-02. Reference Manual "Expressions" (Try, Catch and Throw), ERTS `erlang` module (get_stacktrace listed as removed, raise/3). Removed: nothing factual contradicted; "recent releases" hedge replaced by the removal fact.
Method: documentation only; no commands were run.
