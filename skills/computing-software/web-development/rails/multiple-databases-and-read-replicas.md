---
id: computing-software.web-development.rails.multiple-databases-and-read-replicas
name: multiple-databases-and-read-replicas
category: computing-software
field: web-development
product: rails
tags: [rails-multiple-databases, read-replicas, connects-to, horizontal-sharding, rails]
level: advanced
status: docs-checked
description: "Rails multiple databases: database.yml with primary and replica, connects_to, automatic role switching, replication lag delay, per-model databases and sharding."
sources:
  - https://guides.rubyonrails.org/active_record_multiple_databases.html
  - https://api.rubyonrails.org/classes/ActiveRecord/Middleware/DatabaseSelector.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple databases and read replicas

## 1. database.yml
```yaml
production:
  primary:
    database: my_primary_database
    adapter: mysql2
    username: root
  primary_replica:
    database: my_primary_database        # same database name as the writer
    adapter: mysql2
    username: root_readonly              # different user, read-only permissions
    replica: true                        # Rails does not run tasks such as migrations against replicas
  animals:
    database: my_animals_database
    adapter: mysql2
    migrations_paths: db/animals_migrate # required for each new writer database
  animals_replica:
    database: my_animals_database
    adapter: mysql2
    replica: true
```
An environment variable named `<CONNECTION>_DATABASE_URL` (for example `ANIMALS_DATABASE_URL`) is merged into that connection's configuration.

## 2. Models
```ruby
class ApplicationRecord < ActiveRecord::Base
  primary_abstract_class
  connects_to database: { writing: :primary, reading: :primary_replica }
end
class AnimalsRecord < ApplicationRecord
  self.abstract_class = true
  connects_to database: { writing: :animals, reading: :animals_replica }
end
class Dog < AnimalsRecord; end
```
Connect through abstract classes and have models inherit from them (`Dog < AnimalsRecord`). When there are several databases the guide uses `primary_abstract_class` on the primary class so Rails knows which class `ActiveRecord::Base` connections belong to. Default role names are `writing` and `reading`; `config.active_record.writing_role` and `reading_role` rename them.

## 3. Automatic role switching
```bash
bin/rails g active_record:multi_db     # generates config/initializers/multi_db.rb
```
```ruby
Rails.application.configure do
  config.active_record.database_selector = { delay: 2.seconds }
  config.active_record.database_resolver = ActiveRecord::Middleware::DatabaseSelector::Resolver
  config.active_record.database_resolver_context = ActiveRecord::Middleware::DatabaseSelector::Resolver::Session
end
```
POST, PUT, DELETE and PATCH requests use the writer; other requests use the replica unless the user recently wrote, in which case the writer is used (read-your-own-write within the `delay` window, 2 seconds by default). Rails does not guarantee reading another user's recent write inside that window.

Manual switching:
```ruby
ActiveRecord::Base.connected_to(role: :reading) { Report.heavy_query }
ActiveRecord::Base.connected_to(role: :writing) { order.reload }   # must-be-fresh read
ActiveRecord::Base.connected_to(role: :reading, prevent_writes: true) { ... }
```
`prevent_writes: true` makes Rails check each query and reject writes; also configure the replica itself as read-only. An unknown role raises `ActiveRecord::ConnectionNotEstablished`.

## 4. Migrations and tasks
- `bin/rails db:migrate` migrates the writer databases (not replicas); `db:migrate:animals` and `db:migrate:primary` migrate one.
- Generators take `--database`: `bin/rails g migration CreateDogs name:string --database animals`.
- Schema files are per database (`db/[name]_schema.rb`, e.g. `db/animals_schema.rb`); `schema_dump:` renames the file or `schema_dump: false` skips it.

## 5. Sharding
```ruby
class ShardRecord < ApplicationRecord
  self.abstract_class = true
  connects_to shards: {
    shard_one: { writing: :primary_shard_one, reading: :primary_shard_one_replica },
    shard_two: { writing: :primary_shard_two, reading: :primary_shard_two_replica }
  }
end
ShardRecord.connected_to(role: :writing, shard: :shard_one) { Person.create! }
```
With sharding both a `role` and a `shard` must be passed, and `migrations_paths` and `schema_dump` must stay the same for all shards. Automatic per-request selection uses the `ShardSelector` middleware: `config.active_record.shard_selector = { lock: true }` plus a `config.active_record.shard_resolver` lambda (`lock` defaults to true and should stay true for tenant sharding). Joins across databases are not possible; for `has_many :through` / `has_one :through` pass `disable_joins: true` so Rails runs separate queries.

## Verify
- [ ] GETs hit the replica and post-write reads hit the primary; migrations target only writer databases; writes inside `prevent_writes: true` blocks are rejected in tests.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 multiple databases guide. Confirmed: `replica: true` and the same-name and read-only-user requirements, `migrations_paths`, `primary_abstract_class`, `connects_to database:`/`shards:`, default roles, `rails g active_record:multi_db` and the `database_selector`/`database_resolver`/`database_resolver_context` settings, the 2-second default `delay`, verb-based switching, `connected_to` with `role:`, `shard:` and `prevent_writes: true`, `--database`, `db:migrate:<name>`, `ShardSelector` options and `disable_joins: true`. Fixed: a `reading` block raises on writes only when `prevent_writes: true` is passed (the guide does not say it is automatic); sharded `connected_to` needs both role and shard; the earlier YAML used `url:` keys the guide does not show and a reading connection with no replica entry; removed the unconfirmed query-log `role` advice.

Method: documentation only; no commands were run.
