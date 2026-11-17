---
id: computing-software.web-development.rails.scopes-and-enums
name: scopes-and-enums
category: computing-software
field: web-development
product: rails
tags: [activerecord-scopes, activerecord-enum, default-scope, rails-enum, active-record, rails]
level: practitioner
status: docs-checked
description: "Active Record scopes and enums: chainable scopes vs class methods, default_scope pitfalls, enum declaration options, generated methods, safe value mapping and Postgres enums."
sources:
  - https://guides.rubyonrails.org/active_record_querying.html#scopes
  - https://api.rubyonrails.org/classes/ActiveRecord/Enum.html
  - https://guides.rubyonrails.org/active_record_postgresql.html#enumerated-types
  - https://github.com/rails/rails/blob/v8.1.4/activerecord/lib/active_record/enum.rb
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scopes and enums

## 1. Scopes
```ruby
class Post < ApplicationRecord
  scope :published, -> { where(published_at: ..Time.current) }
  scope :by_author, ->(user) { where(author: user) if user.present? }    # nil -> returns all, still chainable
  scope :recent, -> { order(published_at: :desc).limit(20) }
end
Post.published.by_author(current_user).recent
```
A scope always returns an `ActiveRecord::Relation`, even when its conditional is false, whereas a class method returns `nil` and can raise `NoMethodError` when chained; to make a class method behave like a scope, return `self` in the false branch. Scopes can be called on associations too: `user.posts.published`.

## 2. default_scope: avoid
`default_scope { where(deleted_at: nil) }` applies to every query on the model. The guide notes it is also applied when creating/building a record with hash arguments (so `Post.new` gets `deleted_at: nil`) but not when updating, and `unscoped` removes it. Prefer explicit named scopes (such as `kept`) unless you really want it everywhere.

## 3. Enums
```ruby
class Order < ApplicationRecord
  enum :status, { pending: 0, paid: 1, shipped: 2, cancelled: 3 }, default: :pending, validate: true
  enum :channel, { web: "web", app: "app" }, prefix: true        # string-backed, methods channel_web?, Order.channel_web
end
order.paid?        order.shipped!        Order.paid        Order.not_cancelled
Order.statuses     # the mapping, exposed through the pluralized class method
Order.where(status: [:paid, :shipped])
```
- Prefer the explicit hash: with the array form the integer is the element's position, so existing values must keep their positions and new values go at the end; the explicit hash syntax is how to remove unused values.
- By default assigning an invalid value raises `ArgumentError`; `validate: true` (or `validate: { allow_nil: true }`) validates the value before saving instead, which matters for params.
- `prefix:`/`suffix:` (`true` or a custom value) avoid method clashes when two enums share value names; with `suffix: true` the methods are `active_status!`, `archived_status?`.
- Postgres native enums: `create_enum :order_status, %w[pending paid shipped]` in a migration and `t.enum :status, enum_type: :order_status`, then declare the enum with string values.

## Gotchas
- Enum scopes can collide with other scopes/methods (`Order.web` vs a `web` scope); prefixes help.
- Exposing enum values in APIs: return the string key, accept keys, never the integer.

## Verify
- [ ] Assigning an unknown status from params yields a validation error, not a 500; `Post.published.to_sql` shows the expected conditions.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 Active Record querying and PostgreSQL guides and the v8.1.4 enum source documentation. Confirmed: scope definition and the always-a-relation caveat for class methods, `default_scope` behaviour on create and `unscoped`, `enum :name, {...}` with `default:`, `prefix:`/`suffix:`, generated predicate, bang and `not_` scopes, the pluralized mapping method, array-position mapping caveat, `ArgumentError` versus `validate: true`, and `create_enum`/`t.enum enum_type:` for PostgreSQL. Removed the Rails 7.1 version gate and the `discard` gem suggestion, which the checked pages do not state.

Method: documentation only; no commands were run.
