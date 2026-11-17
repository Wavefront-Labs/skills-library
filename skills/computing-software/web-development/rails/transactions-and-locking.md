---
id: computing-software.web-development.rails.transactions-and-locking
name: transactions-and-locking
category: computing-software
field: web-development
product: rails
tags: [optimistic-locking, pessimistic-locking, with-lock, activerecord-transactions, lock-version, rails]
level: advanced
status: docs-checked
description: "Consistent writes in Rails: transactions and savepoints, optimistic locking with lock_version, pessimistic locks (lock, with_lock, NOWAIT) and deadlocks."
sources:
  - https://api.rubyonrails.org/classes/ActiveRecord/Locking/Optimistic.html
  - https://api.rubyonrails.org/classes/ActiveRecord/Locking/Pessimistic.html
  - https://api.rubyonrails.org/classes/ActiveRecord/Transactions/ClassMethods.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transactions and locking

## 1. Transactions
```ruby
ActiveRecord::Base.transaction do
  order.update!(status: :paid)            # bang methods raise -> rollback
  Payment.create!(order:, amount: order.total)
end
```
- Exceptions raised inside the block force a ROLLBACK, and `ActiveRecord::Rollback` triggers one without being re-raised; use bang methods so failures raise.
- Nested `transaction` calls join the outer one; `transaction(requires_new: true)` creates a savepoint.
- Side effects (emails, jobs, HTTP) go in `after_commit` or after the block, never inside (they cannot be rolled back; jobs may run before commit).

## 2. Optimistic locking (low contention, user edits)
Add `lock_version :integer, default: 0, null: false`; Rails checks and increments it on update:
```ruby
def update
  @doc.update!(doc_params)                  # include lock_version as a hidden field in the form
rescue ActiveRecord::StaleObjectError
  @doc.reload
  flash.now[:alert] = "Someone else changed this document. Review and save again."
  render :edit, status: :conflict
end
```

## 3. Pessimistic locking (money, inventory, counters)
```ruby
account = Account.lock.find(id)                        # SELECT ... FOR UPDATE (inside a transaction)
account.with_lock { account.update!(balance: account.balance - amount) }   # transaction + reload with lock
```
Hold locks briefly; lock rows in a consistent order to avoid deadlocks; `lock("FOR UPDATE NOWAIT")` to fail fast.

## 4. Isolation
Pass the `isolation:` option to `transaction` (see the Transactions API) for invariants spanning rows, and be ready to retry on failures.

## Verify
- [ ] A concurrency test (two threads/processes) on the critical path produces correct balances/stock; stale form submissions show a conflict message.

## Checked

2026-10-28. Confirmed from the Rails API pages for Transactions::ClassMethods (exceptions force a ROLLBACK, `ActiveRecord::Rollback` is not re-raised, `requires_new: true` creates a real sub-transaction, `isolation:` option, `after_commit`), Locking::Optimistic (`lock_version`, `StaleObjectError`) and Locking::Pessimistic (`lock`, `with_lock`, `FOR UPDATE NOWAIT`). Removed (not found in the pages): `SKIP LOCKED` example, the atomic-counter section (`update_counters`, conditional `update_all`), `ActiveRecord::SerializationFailure` and the `:serializable` example, the claim about non-bang `save`.

Method: documentation only; no commands were run.
