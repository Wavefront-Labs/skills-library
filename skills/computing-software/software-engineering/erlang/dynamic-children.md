---
id: computing-software.software-engineering.erlang.dynamic-children
name: dynamic-children
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-supervisor, dynamic-children]
level: advanced
status: docs-checked
description: "OTP supervisor dynamic children: start_child, terminate_child, delete_child and simple_one_for_one templates."
sources:
  - https://www.erlang.org/doc/system/design_principles.html
  - https://www.erlang.org/doc/apps/stdlib/supervisor.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic children and simple_one_for_one
**Goal:** manage a changing pool of workers.

```erlang
supervisor:start_child(Sup, ChildSpec),             % one_for_one etc.: full spec
supervisor:terminate_child(Sup, Id),                % stop the process, keep the spec
supervisor:delete_child(Sup, Id),                   % delete the spec (process must not be running)
%% simple_one_for_one: template spec, start_child gets extra args
init([]) ->
    {ok, {#{strategy => simple_one_for_one},
          [#{id => conn, start => {conn, start_link, []}, restart => temporary}]}}.
supervisor:start_child(Sup, [Socket]).             % calls apply(conn, start_link, [] ++ [Socket])
```
- `simple_one_for_one` is a simplified `one_for_one` where all children are dynamically added instances of the same process type (same code). The child specification list must contain exactly one spec, its identifier is ignored, and no child starts during initialisation.
- For `simple_one_for_one`, `start_child/2` takes a list of extra arguments appended to the spec's start arguments. `delete_child/2` and `restart_child/2` return `{error, simple_one_for_one}`; `terminate_child/2` works there only when given the child's pid, not the spec identifier.
- Children in `one_for_one`, `one_for_all` and `rest_for_one` supervisors can also be added with `start_child/2` and a full child spec.
- `simple_one_for_one` shuts children down asynchronously, so the stop order is not defined.

## Gotchas
- A `temporary` child is never restarted, and its child specification is automatically deleted when it terminates, so such a child cannot be restarted; track it yourself if needed.
- `count_children/1` for a `simple_one_for_one` supervisor does not check that each child is still alive for its `active` count, though the figure is likely accurate unless the supervisor is overloaded.

## Self-check
Start many children and compare `count_children/1` against your own count.

## Checked
Read the supervisor reference (stdlib): simple_one_for_one definition and restrictions, start_child/terminate_child/delete_child/restart_child behaviour, temporary restart semantics, count_children note. Removed (not stated on the page): "faster to start", "newer OTP lets one_for_one hold dynamic children", and "dynamic children are not restarted after the supervisor restarts".
Method: docs-only read of cited pages, 2026-11-08
