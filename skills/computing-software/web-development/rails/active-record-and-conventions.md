---
id: computing-software.web-development.rails.active-record-and-conventions
name: active-record-and-conventions
category: computing-software
field: web-development
product: rails
tags: [rails, ruby-on-rails, ruby, active-record, activerecord, orm, generators, migrations, associations, has-many, belongs-to, validations, database-constraints, n-plus-one, n+1, includes, preload, eager-load, strict-loading, bullet, prosopite, scopes, callbacks, after-commit, find-each, in-batches, transactions, with-lock, convention-over-configuration, web-development, rails-n-plus-one, rails-scopes]
level: practitioner
status: docs-checked
description: "Rails Active Record: generators, migrations, associations, validations vs DB constraints, N+1 with includes/preload/eager_load, strict_loading, scopes, callbacks, find_each."
sources:
  - https://guides.rubyonrails.org/active_record_basics.html
  - https://guides.rubyonrails.org/active_record_querying.html
  - https://guides.rubyonrails.org/active_record_migrations.html
  - https://github.com/flyerhzm/bullet
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Active Record and Rails conventions — let the names do the wiring, let the DB enforce it

**Goal:** model data the Rails way so associations and routes "just work", while
keeping integrity in the database and queries free of N+1.

## 1. Conventions and generators
Model `LineItem` → table `line_items` → foreign key `line_item_id` → controller
`LineItemsController`. Fight the convention only with a reason.

```bash
bin/rails g model Order customer:references status:string total:decimal{10,2}
bin/rails g migration AddPaidAtToOrders paid_at:datetime:index
bin/rails db:migrate && bin/rails db:rollback   # roll back once to prove `change` is reversible
```
`references` adds the column, an index and a foreign-key constraint. Commit `db/schema.rb`
(or `structure.sql`) with the migration.

## 2. Validations are not enough — add constraints
```ruby
class User < ApplicationRecord
  validates :email, presence: true, uniqueness: { case_sensitive: false }
end
# migration
add_index :users, "lower(email)", unique: true      # PostgreSQL expression index
change_column_null :users, :email, false
```
`uniqueness` validation does a SELECT then INSERT — two concurrent requests both pass.
Only a unique index stops duplicates. Likewise pair
`presence` with `null: false` and `belongs_to` with a real foreign key.

On large tables an index build can block writes; check your database's online-index options and the Rails migrations guide (`disable_ddl_transaction!`) before running it in production.

## 3. Associations
```ruby
class Customer < ApplicationRecord
  has_many :orders
  has_many :line_items, through: :orders
end
class Order < ApplicationRecord
  belongs_to :customer
  has_many :line_items, dependent: :destroy
end
```
Choose a `dependent:` option deliberately and check the Active Record Associations guide for what each does.

## 4. N+1: includes vs preload vs eager_load
| Method | SQL | Use when |
|---|---|---|
| `preload(:customer)` | separate query per association | default, no filtering on the association |
| `eager_load(:customer)` | one LEFT OUTER JOIN | you filter/order by the association |
| `includes(:customer)` | picks one of the above | convenient; switches to JOIN if you `references` or `where` a hash on that table |

```ruby
Order.includes(:customer, line_items: :product).where(status: "paid")
```
Detect: the **Bullet** gem (its `raise` option makes specs fail on N+1). Prevent:
```ruby
# config/environments/development.rb and test.rb
config.active_record.strict_loading_by_default = true
# or per query / association
Order.strict_loading.all;  has_many :line_items, strict_loading: true
```
Lazy loading then raises `ActiveRecord::StrictLoadingViolationError`.

## 5. Scopes and querying
```ruby
scope :paid, -> { where.not(paid_at: nil) }
scope :recent, -> { order(created_at: :desc) }
Order.paid.recent.limit(20)
```
- `pluck(:id)` instead of `map(&:id)` for plain values.
- `exists?` over `present?` on relations.
- Avoid `default_scope` — it leaks into every query and association and is hard to escape (`unscoped` removes too much).
- Never interpolate into SQL: `where("name = ?", name)` or hash conditions.

## 6. Callbacks: keep them boring
Use callbacks for normalising the record itself, and prefer explicit service objects for
multi-model workflows with side effects. Check the Active Record Callbacks guide for when
callbacks and validations are skipped.

## 7. Batches and transactions
```ruby
User.where(active: true).find_each(batch_size: 1000) { |u| u.recalculate! }  # not .each
Order.where(stale: true).in_batches(of: 5000).update_all(archived: true)

ActiveRecord::Base.transaction do
  account.update!(balance: account.balance - amount)
  Ledger.create!(account:, amount: -amount)
end
```
Use bang methods inside transactions so a failure raises and rolls back. `find_each`
works on relations without an ordering, because it forces its own order internally.

## Verify
- [ ] Every uniqueness/presence validation has a matching unique index / `null: false`.
- [ ] Each migration rolls back cleanly; schema file committed.
- [ ] Bullet or `strict_loading_by_default` is on in dev/test and the suite is clean.
- [ ] No external side effects inside model callbacks that run before the transaction commits.
- [ ] Bulk jobs use `find_each`/`in_batches`; money moves inside a transaction.

## Checked

2026-11-02. Checked against the Rails Guides for Active Record Basics, Querying and Migrations and the Bullet README. Confirmed: references shorthand (columns, indexes, foreign keys), change_column_null, disable_ddl_transaction!, preload/eager_load/includes behaviour, strict_loading_by_default and StrictLoadingViolationError, find_each/in_batches, default_scope and unscoped, scopes with bound parameters, Bullet raise option. find_each wording corrected: the guide says it works on relations that have no ordering. Removed because the fetched guides do not state them: has_many dependent options detail (restrict_with_error), belongs_to required by default, RecordNotUnique rescue, algorithm: :concurrently and strong_migrations, the callback advice and list of callback-skipping methods, the lock!/transaction example and counter-update methods, and Prosopite.

Method: documentation only; no commands were run.
