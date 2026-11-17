---
id: computing-software.software-engineering.elixir.mix-tasks-custom-aliases
name: mix-tasks-custom-aliases
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, mix-task, mix-alias, use-mix-task, shortdoc, app-start, mix-run, mix-tasks]
level: practitioner
status: docs-checked
description: "Write custom Mix tasks with Mix.Task, start the app only when needed, and compose aliases such as setup and ci."
sources: ["https://hexdocs.pm/mix/Mix.Task.html", "https://hexdocs.pm/mix/Mix.html", "https://hexdocs.pm/mix/Mix.Tasks.App.Start.html", "https://hexdocs.pm/mix/Mix.Tasks.App.Config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom Mix tasks and aliases

**Goal:** automate repeatable project commands.

```elixir
# lib/mix/tasks/greet.ex  ->  mix greet NAME
defmodule Mix.Tasks.Greet do
  use Mix.Task
  @shortdoc "Greets someone"
  @moduledoc "Usage: mix greet NAME"
  @impl Mix.Task
  def run([name | _]) do
    Mix.Task.run("app.start")          # start the app + deps if the task needs them
    IO.puts("Hello, #{name}")
  end
  def run(_), do: Mix.raise("usage: mix greet NAME")
end

# mix.exs
defp aliases do
  [setup: ["deps.get", "compile"],
   seed: ["run priv/seeds.exs"],
   ci: ["format --check-formatted", "test"]]
end
```

## Rules
- A task is a module named `Mix.Tasks.<Name>` that does `use Mix.Task` and implements `run/1`, which receives the list of command-line arguments; the command name is the part after `Mix.Tasks.` (`Mix.Tasks.Deps.Clean` is `deps.clean`). Files usually live in `lib/mix/tasks/`.
- `@shortdoc` makes the task visible in `mix help`; `mix help my_task` shows the `@moduledoc`. Use `Mix.shell().info/1` for output: the shell is swappable (`Mix.Shell.Process` sends messages instead of printing), which helps tests. `Mix.raise/1` raises a formatted Mix error (exit status 1 by default).
- Declare what a task needs with `@requirements`: `"loadpaths"` (dependencies available and compiled; recommended for library tasks that do not touch user code), `"app.config"` (also compiles and loads runtime configuration, the minimum for tasks that interact with your code) or `"app.start"` (also starts the supervision tree). Calling `Mix.Task.run("app.start")` inside `run/1` is the manual equivalent.
- Tasks run only once per invocation: a second `Mix.Task.run/2` returns `:noop` unless you call `Mix.Task.reenable/1` or `Mix.Task.rerun/2`. `mix cmd`, `mix do` and `mix xref` are re-enabled automatically; `mix run` too.
- Aliases may be a string, a function, or a list run consecutively. An alias with the name of an existing task overrides it and forwards its arguments to the original task; otherwise arguments are appended to the last task in the list. `Mix.Task.run/2` runs the alias, not the original, when one exists.
- Aliases defined in your project do not affect dependencies, and aliases in dependencies are not available to you (umbrella children are the exception).
- The default environment is `dev`. Set the environment for a task or alias in `mix.exs` with `def cli, do: [preferred_envs: [ci: :test]]` (the per-task `@preferred_cli_env` attribute is documented, but `Mix.Task.preferred_cli_env/1` is deprecated in favour of `def cli`).

## Self-check
Run `mix help greet` and confirm the shortdoc shows in `mix help`.

## Checked

Checked 2026-11-08 against the Mix.Task behaviour page (attributes, requirements, run/reenable semantics), the Mix module page (aliases, `def cli`, Mix.shell, Mix.raise), and the `mix app.start` and `mix app.config` pages. Removed: the Ecto-based aliases, the Credo alias and the `OptionParser.parse/2` advice, which the cited pages do not cover.

Method: docs-only read of cited pages, 2026-11-08
