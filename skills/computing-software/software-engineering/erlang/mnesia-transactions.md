---
id: computing-software.software-engineering.erlang.mnesia-transactions
name: mnesia-transactions
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-mnesia, mnesia-transactions]
level: advanced
status: docs-checked
description: "Mnesia transactions: mnesia:transaction/1 with write/read/select, dirty_ operations, abort and restart semantics."
sources:
  - https://www.erlang.org/doc/apps/mnesia/mnesia.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transactions, dirty operations and queries
**Goal:** read and write Mnesia data safely.

```erlang
F = fun() ->
        mnesia:write(#user{id = 1, name = <<"ann">>}),
        mnesia:read(user, 1)
    end,
{atomic, [#user{}]} = mnesia:transaction(F).
mnesia:dirty_read(user, 1).
mnesia:transaction(fun() -> mnesia:select(user, [{#user{id='$1', _='_'}, [{'>', '$1', 0}], ['$_']}]) end).
```
- Mnesia detects deadlocks and can restart a transaction any number of times (`transaction/3` takes a `Retries` count, default `infinity`), so the fun must have no side effects such as waiting for messages, and must not catch `exit` exceptions with reason `{aborted, term()}`.
- Transactions return `{atomic, Value}` or `{aborted, Reason}`; `mnesia:abort(Reason)` makes the transaction return `{aborted, Reason}`. A user error inside the fun also yields `{aborted, Reason}`.
- Dirty operations such as `mnesia:dirty_read/2` can leave the database in an inconsistent state if used to update it; the manual says to use them only for performance reasons when absolutely necessary.
- Queries can also be written with list comprehension notation through the `qlc` module.

## Self-check
Run two competing transactions and observe one retry by counting executions of the fun.

## Checked

2026-11-03. Confirmed in the `mnesia` reference page: `transaction/1,3` restart text, `abort/1`, `{atomic, ...}` and `{aborted, ...}` results, `read/2`, `select/2`, `dirty_read/2` and the dirty-operations warning. Removed: "no isolation / weaker replication ordering" wording, the mixing dirty and transactional access gotcha, and the lock-duration advice.
Method: documentation only; no commands were run.
