---
id: computing-software.software-engineering.elixir.application-start-callback-mod
name: application-start-callback-mod
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, application, mod-callback, start-stop, extra-applications, mix-exs-application, applications-boot, application-callback]
level: practitioner
status: docs-checked
description: "Define an Application callback module with start/2 returning the root supervisor and declare extra_applications in mix.exs."
sources: ["https://hexdocs.pm/elixir/Application.html", "https://hexdocs.pm/elixir/Supervisor.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application module and the supervision tree root

**Goal:** boot your app's processes in the right order.

```elixir
# mix.exs
def application, do: [mod: {MyApp.Application, []}, extra_applications: [:logger, :runtime_tools]]

# lib/my_app/application.ex
defmodule MyApp.Application do
  use Application
  @impl true
  def start(_type, _args) do
    children = [MyApp.Repo, {Phoenix.PubSub, name: MyApp.PubSub}, MyAppWeb.Endpoint]
    Supervisor.start_link(children, strategy: :one_for_one, name: MyApp.Supervisor)
  end
  @impl true
  def stop(_state), do: :ok
end
```

## Rules
- Order children so dependencies start first (Repo before Endpoint, PubSub before Endpoint).
- The `mod:` tuple is `{Module, start_arg}`; omit it for library-only apps with no processes.

## Failure modes

## Self-check
Remove a child that another depends on and read the startup error chain.

## Checked
2026-11-02: confirmed against Application module docs (mod: {Module, args}, start/2 callback) and Supervisor docs (start_link, :one_for_one, name:). Removed: dependency auto-start, extra_applications advice, mix run --no-start, error-chain text.
Method: documentation only; no commands were run.
