---
id: computing-software.software-engineering.elixir.task-supervisor-async-nolink
name: task-supervisor-async-nolink
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, task-supervisor, async-nolink, start-child, supervised-tasks]
level: advanced
status: docs-checked
description: "Start supervised dynamic tasks with Task.Supervisor, using async_nolink so a crashing task does not take down the caller."
sources: ["https://hexdocs.pm/elixir/Task.Supervisor.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task.Supervisor for fire-and-forget and isolated work

**Goal:** run unreliable background work that cannot crash the caller.

```elixir
# application.ex children
{Task.Supervisor, name: MyApp.TaskSup}

Task.Supervisor.start_child(MyApp.TaskSup, fn -> send_email(user) end)    # fire and forget

task = Task.Supervisor.async_nolink(MyApp.TaskSup, fn -> risky() end)
case Task.yield(task, 5_000) || Task.shutdown(task) do
  {:ok, result} -> result
  {:exit, reason} -> {:error, reason}
  nil -> {:error, :timeout}
end
```

## Rules
- `start_child` tasks restart according to `:restart` (default `:temporary`, not restarted).
- `async_nolink` returns a task you await or yield; `Task.yield/2` returns `{:exit, reason}` on a crash instead of the caller dying. It needs the supervisor's `:restart` to be `:temporary` (the default).
- `Task.Supervisor` is a single process and can become a bottleneck; start several under a `PartitionSupervisor` with `child_spec: Task.Supervisor`.
- `restart:` (`:temporary`, `:transient`, `:permanent`) can be given to `start_child`.

## Self-check
Raise inside the function passed to `async_nolink` and confirm your process survives.

## Checked
2026-11-03: confirmed against the Elixir Task.Supervisor docs (`start_child/3` options and `:restart` default `:temporary`, `async_nolink` requirement, `terminate_child/2`, bottleneck note with `PartitionSupervisor`). Removed: the Oban job-library advice and the `{sup, node}` distributed call (not on the page read).
Method: documentation only; no commands were run.
