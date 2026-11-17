---
id: computing-software.software-engineering.elixir.oban-worker-queues-retries
name: oban-worker-queues-retries
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, oban, job-queue, worker, perform, retries, unique-jobs, cron, oban-testing, oban-jobs, elixir-background-jobs]
level: practitioner
status: draft
description: "Persist and run background jobs in PostgreSQL-backed Oban queues, with workers, retries/backoff, uniqueness, cron and testing helpers."
sources: ["https://hexdocs.pm/oban"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Oban background jobs

**Goal:** reliable, retryable async work.

```elixir
defmodule MyApp.Workers.Email do
  use Oban.Worker, queue: :mailers, max_attempts: 5, unique: [period: 300]
  @impl Oban.Worker
  def perform(%Oban.Job{args: %{"user_id" => id}}) do
    case Mailer.send(id) do
      :ok -> :ok
      {:error, :bounced} -> {:cancel, :bounced}      # stop retrying
      {:error, reason} -> {:error, reason}           # retried with backoff
    end
  end
end
%{user_id: 1} |> MyApp.Workers.Email.new(schedule_in: 60) |> Oban.insert()
# config: config :my_app, Oban, repo: MyApp.Repo, queues: [mailers: 10, default: 5], plugins: [Oban.Plugins.Pruner]
# test: use Oban.Testing, repo: MyApp.Repo ; assert_enqueued worker: MyApp.Workers.Email ; perform_job/3
```

## Rules
- Args are JSON: keys come back as strings; pass ids not structs.
- Insert jobs in the same transaction as the data change (`Oban.insert/3` in an `Ecto.Multi`) to avoid lost or orphan jobs.
- Make `perform/1` idempotent because at-least-once delivery means a job can run twice.
- Run migrations (`Oban.Migration`) as the docs describe; versions of the migration module matter on upgrades.
- Oban features such as cron/Pro workflows depend on the plan and version (check the docs).

## Self-check
Enqueue a failing job and watch it retry with growing delays.
