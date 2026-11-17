---
id: computing-software.web-development.rails.solid-queue-cache-and-cable
name: solid-queue-cache-and-cable
category: computing-software
field: web-development
product: rails
tags: [solid-queue, solid-cache, solid-cable, rails-8, database-backed-infrastructure]
level: practitioner
status: docs-checked
description: "Solid Queue, Solid Cache and Solid Cable: database-backed Active Job, cache and Action Cable without Redis, with configuration, Mission Control and when to keep Redis."
sources:
  - https://github.com/rails/solid_queue
  - https://github.com/rails/solid_cache
  - https://github.com/rails/solid_cable
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Solid Queue, Solid Cache and Solid Cable

Background jobs, caching and WebSocket pub/sub backed by the database (SQLite, PostgreSQL or MySQL) instead of Redis. Fewer moving parts for most apps.

## 1. Databases
Each gem can use its own database (`queue`, `cache`, `cable`) with its own schema file (`db/queue_schema.rb`, `db/cache_schema.rb`, `db/cable_schema.rb`). Add to an existing app with `bin/rails solid_queue:install` (and `solid_cache:install`, `solid_cable:install`).

## 2. Solid Queue
```ruby
config.active_job.queue_adapter = :solid_queue
config.solid_queue.connects_to = { database: { writing: :queue } }
```
```yaml
# config/queue.yml
production:
  dispatchers: [{ polling_interval: 1, batch_size: 500 }]
  workers:
    - { queues: "critical,default", threads: 5, processes: 2, polling_interval: 0.1 }   # illustrative values
    - { queues: "low", threads: 2 }
```
- Run with `bin/jobs` (supervisor) or in Puma via `plugin :solid_queue` (the README gates it on `ENV["SOLID_QUEUE_IN_PUMA"]`) for single-server setups.
- Recurring jobs go in `config/recurring.yml`.
- Uses `FOR UPDATE SKIP LOCKED` where available (MySQL 8+, MariaDB 10.6+, PostgreSQL 9.5+) to avoid lock waits when polling.
- Mission Control - Jobs (`mission_control-jobs` gem) is the web UI: mount behind admin authentication.
- Failed jobs are kept for inspection/retry; configure `retry_on`/`discard_on` in jobs.

## 3. Solid Cache
```ruby
config.cache_store = :solid_cache_store
```
- Stores entries in the database, so caches can be much larger than RAM-bound Redis; reads are slower than RAM.
- `config/cache.yml`: `max_age` (default 2 weeks), `max_size` (default no limit), optional encryption (`encrypt: true`) and sharding via `connects_to`.

## 4. Solid Cable
```yaml
# config/cable.yml
production:
  adapter: solid_cable
  connects_to: { database: { writing: :cable } }
  polling_interval: 0.1.seconds
  message_retention: 1.day
```
Polling-based pub/sub; fine for typical Turbo Streams broadcast volumes. For very high-throughput real-time apps, Redis or AnyCable may still fit better.

## 5. When to keep Redis
Very high job throughput with sub-millisecond latency, existing Sidekiq Pro/Enterprise features, or heavy pub/sub. Otherwise Solid trifecta removes a dependency.

## Checked
2026-10-31. Confirmed against the solid_queue, solid_cache and solid_cable READMEs: install tasks and schema files, `bin/jobs`, Puma plugin env gate, `config/queue.yml` and `config/recurring.yml`, `SKIP LOCKED` support versions, Mission Control, Solid Cache `max_age` default (2 weeks), `max_size` default (nil), `encrypt`, and Solid Cable `polling_interval`/`message_retention` (default 1.day). Removed: the `limits_concurrency` example, the Rails 8 new-app database.yml claim and the Active Job guide source.
Method: documentation only; no commands were run.

## Verify
- [ ] Jobs run from bin/jobs or Puma plugin; recurring tasks fire; Mission Control behind auth; cache hit ratio monitored; broadcasts reach clients across app servers.
