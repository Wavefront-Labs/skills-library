---
id: computing-software.web-development.rails.associations-through-polymorphic-dependent
name: associations-through-polymorphic-dependent
category: computing-software
field: web-development
product: rails
tags: [rails, rails-associations, polymorphic-associations, has-many-through, dependent-destroy, counter-cache, inverse-of, ruby, web-development]
level: practitioner
status: docs-checked
description: "Modelling Rails associations: has_many through vs HABTM, polymorphic associations and their trade-offs, dependent options, counter_cache, inverse_of and touch."
sources:
  - https://guides.rubyonrails.org/association_basics.html
  - https://guides.rubyonrails.org/configuring.html#config-active-record-belongs-to-required-by-default
  - https://api.rubyonrails.org/classes/ActiveRecord/Associations/ClassMethods.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Associations: through, polymorphic, dependent

**Goal:** associations that match the domain, keep referential integrity and don't explode on delete.

## 1. Many-to-many: use has_many :through
```ruby
class Membership < ApplicationRecord
  belongs_to :user
  belongs_to :team
  validates :role, inclusion: { in: %w[member admin] }
end
class Team < ApplicationRecord
  has_many :memberships, dependent: :destroy
  has_many :users, through: :memberships
end
```
A join **model** can hold attributes (role, joined_at), validations and callbacks. `has_and_belongs_to_many` has no model - you'll want one later. Add a unique index on `[:team_id, :user_id]`.

## 2. Polymorphic
```ruby
class Comment < ApplicationRecord
  belongs_to :commentable, polymorphic: true          # commentable_type + commentable_id
end
class Post < ApplicationRecord
  has_many :comments, as: :commentable, dependent: :destroy
end
```
```ruby
create_table :comments do |t|
  t.references :commentable, polymorphic: true, null: false   # creates commentable_type + commentable_id
  t.index [:commentable_type, :commentable_id]               # the guide's manual migration adds this index
end
```
Trade-offs: the type column stores class names, so a class rename needs a migration that updates the `_type` column (the guide's warning); one foreign key cannot point at several tables. An alternative for "one record of several kinds" is delegated types (`delegated_type :entryable, types: %w[Message Comment]`).

## 3. dependent options
| Option | Behaviour |
|---|---|
| `:destroy` | loads and destroys each child (callbacks run) - slow for thousands |
| `:destroy_async` | enqueues `ActiveRecord::DestroyAssociationAsyncJob` to destroy children; needs Active Job; do not use it when the association is backed by database foreign key constraints |
| `:delete_all` | one SQL DELETE, no callbacks |
| `:nullify` | sets FK to NULL (also the type column on polymorphic associations); no callbacks; not for NOT NULL columns |
| `:restrict_with_error` / `:restrict_with_exception` | blocks parent delete if children exist |
Do not put `dependent:` on a `belongs_to` that pairs with a `has_many` on the other class: the guide warns it can orphan records.

## 4. counter_cache, touch, inverse_of
```ruby
belongs_to :post, counter_cache: true, touch: true    # posts.comments_count column; post.updated_at bumped (cache keys)
has_many :comments, inverse_of: :post                  # needed when automatic detection cannot find the inverse
```
Fix stale counters with `Post.reset_counters(id, :comments)`.

## 5. Scoped associations
```ruby
has_many :published_posts, -> { where(published: true).order(published_at: :desc) }, class_name: "Post"
```
Preload scoped associations like any other (`includes(:published_posts)`).

## 6. Integrity
`belongs_to` is required by default (`config.active_record.belongs_to_required_by_default` is `true` with current defaults, so a missing parent gives "must exist"); back it with `null: false` and `foreign_key: true` in migrations.

## Verify
- [ ] Every `belongs_to` column has an index and a DB foreign key (except polymorphic).
- [ ] Deleting a parent with 10k children completes quickly (`destroy_async`/`delete_all`) and leaves no orphans.
- [ ] Pages listing associations load them with `includes`; `strict_loading` can enforce this.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 association basics and configuring guides. Confirmed: `dependent:` options and their notes (`destroy_async` job and foreign-key warning, `nullify` incl. polymorphic type column, `restrict_with_*`), the `dependent` on `belongs_to` warning, polymorphic columns and the manual `[type, id]` index, the class-rename warning, `delegated_type`, `counter_cache`/`touch`/`inverse_of`/`reset_counters`, `strict_loading` and `belongs_to_required_by_default`. Removed the claims that `t.references` adds a composite index, that `includes` issues one query per type, `store_full_class_name`/`polymorphic_name`, the check-constraint alternative, `on_delete: :cascade` advice, the Rails 6.1 gate and the Bullet reference, none of which the checked pages state.

Method: documentation only; no commands were run.
