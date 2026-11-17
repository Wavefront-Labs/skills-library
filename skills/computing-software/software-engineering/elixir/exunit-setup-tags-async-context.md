---
id: computing-software.software-engineering.elixir.exunit-setup-tags-async-context
name: exunit-setup-tags-async-context
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, setup, setup-all, on-exit, tmp-dir, tag, capture-log, capture-io, exclude-tag, async-true, exunit-setup-tags]
level: practitioner
status: docs-checked
description: "Use setup/setup_all for context, on_exit and start_supervised for cleanup, @tag including tmp_dir and timeout, and when async is safe."
sources: ["https://hexdocs.pm/ex_unit/ExUnit.Callbacks.html", "https://hexdocs.pm/ex_unit/ExUnit.Case.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# setup, tags, async and context

**Goal:** isolated tests with shared setup and selective execution.

```elixir
use ExUnit.Case, async: true

setup do
  {:ok, pid} = start_supervised({MyServer, []})     # stopped automatically after the test
  on_exit(fn -> File.rm_rf!("tmp/x") end)
  %{pid: pid}
end
setup :create_user                                   # named setup function returning a map/keyword

@tag external: true
@tag timeout: 120_000
@tag :tmp_dir
test "files", %{tmp_dir: dir, pid: pid} do
  assert is_pid(pid)
  File.write!(Path.join(dir, "a.txt"), "x")
end
# run tagged tests with: mix test --include external:true
```

## Rules
- `start_supervised/2` starts processes under a supervisor linked to the test process; the supervisor and its children are guaranteed to terminate before any `on_exit/2` callback runs.
- `async: true` should be enabled only if tests do not change any global state; tests in one module never run concurrently.
- `setup_all` callbacks run once per module before any test; `setup` runs before each test. Both may return a map or keyword list that is merged into the context.
- `on_exit/2` callbacks always run and execute in a separate process.
- `@tag timeout:` sets the test timeout in ms (default 60_000, `:infinity` allowed); `@tag :tmp_dir` creates a unique directory per test and puts its path in the context as `tmp_dir`.

## Self-check
Check that a `@tag :tmp_dir` test sees an empty `tmp_dir` and that the `start_supervised` process is gone after the test.

## Checked
2026-11-03: confirmed against the ExUnit.Callbacks and ExUnit.Case docs (`setup`/`setup_all` forms and return values, `on_exit/2`, `start_supervised/2`, `@tag` and `tmp_dir`, `timeout` default 60_000, `async` caveats, `--include external:true`). Removed: `capture_io`/`capture_log` (their module pages were not read), `ExUnit.start(exclude: ...)`, and the advice on Application env and `Process.sleep`.
Method: documentation only; no commands were run.
