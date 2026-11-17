---
id: computing-software.web-development.rails.callbacks-and-their-pitfalls
name: callbacks-and-their-pitfalls
category: computing-software
field: web-development
product: rails
tags: [rails, rails-callbacks, after-commit, before-validation, service-objects, active-record, ruby, web-development]
level: practitioner
status: docs-checked
description: "Using Active Record callbacks safely: lifecycle order, before_validation normalisation, after_commit for side effects, skipped callbacks, halting and alternatives."
sources:
  - https://guides.rubyonrails.org/active_record_callbacks.html
  - https://guides.rubyonrails.org/active_record_callbacks.html#transaction-callbacks
  - https://github.com/rails/solid_queue
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Callbacks and their pitfalls

**Goal:** callbacks only for logic about the record itself; side effects after commit; workflows explicit.

## 1. Order on save (create)
`before_validation` -> validate -> `after_validation` -> `before_save` -> `around_save` -> `before_create` -> INSERT -> `after_create` -> `after_save` -> (transaction commits) -> `after_commit`/`after_create_commit`.
All before/after_save callbacks run **inside** the transaction.

## 2. Good uses
```ruby
before_validation :normalize_phone             # shape own attributes (or declare `normalizes`)
before_save :compute_total, if: :line_items_changed?
after_create_commit :broadcast_append           # Turbo broadcasts, jobs, cache busting
after_destroy_commit { Rails.cache.delete(cache_key_for_list) }
```

## 3. Side effects after commit, never in after_save
```ruby
after_save :send_receipt              # bad: email sent even if the transaction rolls back; job may run before commit
after_create_commit :send_receipt     # good
def send_receipt = ReceiptMailer.with(order: self).receipt.deliver_later
```
Active Job can defer enqueueing inside a transaction until it commits when a job class sets `self.enqueue_after_transaction_commit = true` (the Solid Queue README says this is disabled by default), so do not assume it for jobs you have not configured, and never for non-job side effects (HTTP calls, emails sent now).

Gotcha: `after_create_commit` and `after_update_commit` both alias `after_commit`, so declaring them with the same method name keeps only the last one; use `after_save_commit` (the guide's alias for create and update) instead.

## 4. Halting
`throw :abort` in a `before_*` callback cancels the operation: `create`/`save` return false and `create!` raises `ActiveRecord::RecordNotSaved`; `destroy` returns false and `destroy!` raises `ActiveRecord::RecordNotDestroyed`. Any other exception raised in a callback rolls back and is re-raised (except `ActiveRecord::Rollback` and `RecordInvalid`).

## 5. What skips callbacks
The guide lists `decrement!`, `decrement_counter`, `delete`, `delete_all`, `delete_by`, `increment!`, `increment_counter`, `insert`, `insert!`, `insert_all`, `insert_all!`, `touch_all`, `update_column`, `update_columns`, `update_all`, `update_counters`, `upsert` and `upsert_all`. Bulk paths need explicit calls to whatever logic matters.

## 6. Smells
- Callbacks touching other models (`after_save :update_inventory`) create invisible coupling and cascades.
- Conditional webs (`if: :x, unless: :y`) that nobody can trace.
- Tests that need `skip_callback` to set up data.
Prefer a service/command object:
```ruby
class PlaceOrder
  def call(cart, user)
    Order.transaction { @order = Order.create!(...); Inventory.reserve!(@order) }
    OrderMailer.with(order: @order).confirmation.deliver_later
    @order
  end
end
```

## Verify
- [ ] No mailers/HTTP calls/job enqueues in `after_save` or `before_*` (grep).
- [ ] Callback logic only touches `self`; cross-model workflows in services.
- [ ] Rollback test: raise after save in a transaction, assert no email/job.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 Active Record callbacks guide and the solid_queue README. Confirmed: callback order for create/update, `after_commit` and the `*_commit` aliases including the same-method-name override, `throw :abort` results (`RecordNotSaved`, `RecordNotDestroyed`), exception handling in the callback chain and the list of methods that skip callbacks. Fixed: Active Job does not enqueue after commit by default; `enqueue_after_transaction_commit` is a per-job setting that is off unless enabled. Removed the Rails 7.1 and Rails 5 version gates and the `_save_callbacks` debugging tip, which the checked pages do not cover.

Method: documentation only; no commands were run.
