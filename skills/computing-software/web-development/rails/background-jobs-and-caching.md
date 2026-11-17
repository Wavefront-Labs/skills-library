---
id: computing-software.web-development.rails.background-jobs-and-caching
name: background-jobs-and-caching
category: computing-software
field: web-development
product: rails
tags: [rails, active-job, sidekiq, background-jobs, caching, russian-doll-caching, fragment-caching, redis, ruby, web-development]
level: advanced
status: docs-checked
description: "Rails background jobs (Active Job/Sidekiq idempotency and retry semantics) and the caching layers: fragment, Russian doll, and low-level Rails.cache."
sources:
  - https://guides.rubyonrails.org/active_job_basics.html
  - https://guides.rubyonrails.org/caching_with_rails.html
  - https://github.com/rails/rails/blob/v8.1.4/activejob/lib/active_job/exceptions.rb
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rails background jobs and caching

**Goal:** jobs that are safe to retry (because they will be retried) and a
caching strategy where expiry happens automatically from data changes, not
from a timer you have to remember to tune.

## 1. Active Job is an interface; the queue backend is the adapter
`ActiveJob::Base` subclasses are adapter-agnostic — the same job class runs on
any supported backend selected with `config.active_job.queue_adapter` (the
guide shows `:solid_queue`). The default `async` adapter is an in-process,
in-memory queue: if the process crashes or the machine is reset, outstanding
jobs are lost, which the guide calls acceptable only for non-critical jobs in
development. Test job behavior against the adapter you run in production.

## 2. Idempotency — assume every job runs more than once
A retried job runs again after a failure that may have happened part-way
through (for example a timeout after the work actually succeeded), so design
every job to be safe to re-run:
```ruby
class ChargeOrderJob < ApplicationJob
  def perform(order_id)
    order = Order.find(order_id)
    return if order.charged?          # idempotency guard
    Payments.charge!(order)
    order.update!(charged: true)
  end
end
```
Job arguments must be serialisable. Active Job serialises Active Record objects
with GlobalID and re-fetches the record when the job runs, so the job sees
current data (and fails with `ActiveJob::DeserializationError` if the record is
gone). Passing an id and loading the record yourself, as above, works equally
well.

## 3. Retry semantics — know the backoff, don't fight it with your own
```ruby
class ChargeOrderJob < ApplicationJob
  retry_on PaymentGateway::TimeoutError, wait: :polynomially_longer, attempts: 5
  discard_on ActiveRecord::RecordNotFound  # the order is gone; retrying won't help
end
```
`retry_on` defaults to a 3-second wait and 5 attempts (`wait: 3.seconds,
attempts: 5`); a longer backoff such as `:polynomially_longer` suits a
dependency that may be down for a while. Use `discard_on` for errors retrying
can never fix (bad input, missing record) instead of letting them exhaust
their retries.

## 4. Caching layers, outer to inner
- **Fragment caching**: `<% cache @order do %>...<% end %>` caches a view
  fragment keyed on the record's cache key including its version; a fragment
  becomes stale when the `updated_at` of a record it directly depends on
  changes, no manual expiry needed.
- **Russian doll caching**: nested fragment caches (`cache @order` wrapping
  `cache @order.line_items`) where touching a child **must** bubble up and
  invalidate the parent's cache key too — requires `touch: true` on the
  child's `belongs_to :order` association, or the parent fragment keeps
  serving a stale cached view of its children after a child changes.
```ruby
class LineItem < ApplicationRecord
  belongs_to :order, touch: true   # updates order.updated_at when a line item changes
end
```
Forgetting `touch: true` is the single most common Russian-doll-caching bug —
everything looks cached correctly until a nested child updates and the
outer fragment doesn't reflect it.

## 5. Low-level caching (`Rails.cache`) for non-view data
```ruby
Rails.cache.fetch("dashboard_stats/#{shop.id}", expires_in: 10.minutes) do
  ExpensiveStatsQuery.call(shop)
end
```
Use a time-based `expires_in` here since there's no natural "updated_at"-style
invalidation trigger for an aggregate computation. Record-based keys can use
`cache_key_with_version` (the guide's low-level example); where staleness
would actually mislead a user (financial totals, inventory counts), keep
`expires_in` short or put an explicit version in the key.

## Verify
- [ ] Every job is tested as safe to run twice (idempotency guard or naturally idempotent operation).
- [ ] Job arguments are ids or GlobalID-serialisable records, and the job handles a record that no longer exists.
- [ ] `discard_on` is set for errors retrying can't fix; `retry_on` wait and attempts are set deliberately.
- [ ] Every `belongs_to` inside a Russian-doll cache chain has `touch: true` so the parent fragment invalidates on child change.
- [ ] Low-level `Rails.cache` entries for frequently-changing/financial data use a short `expires_in` or an explicit version key, not an indefinite cache.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 Active Job and caching guides and the v8.1.4 `retry_on` source. Confirmed: `config.active_job.queue_adapter`, the in-memory `async` adapter losing jobs on crash, GlobalID argument serialisation, `retry_on` defaults (3 seconds, 5 attempts) and `:polynomially_longer`, `discard_on`, fragment caching keyed on `updated_at`, Russian doll caching with `belongs_to ..., touch: true`, and `Rails.cache.fetch` with `expires_in` and `cache_key_with_version`. Fixed: `retry_on` without `wait` does not retry immediately (default 3 seconds). Removed the Sidekiq at-least-once delivery claim, the dead-letter-queue remark and the page-caching remark, which the checked pages do not state.

Method: documentation only; no commands were run.
