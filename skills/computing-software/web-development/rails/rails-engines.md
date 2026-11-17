---
id: computing-software.web-development.rails.rails-engines
name: rails-engines
category: computing-software
field: web-development
product: rails
tags: [rails-engines, mountable-engines, modular-monolith, rails-plugins, rails]
level: advanced
status: docs-checked
description: "Building Rails engines: mountable vs full, isolate_namespace, mounting, migrations, configuration hooks, modular monoliths, and testing with the dummy app."
sources:
  - https://guides.rubyonrails.org/engines.html
  - https://api.rubyonrails.org/classes/Rails/Engine.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rails engines

An engine is a miniature Rails app packaged as a gem or in-repo component: models, controllers, views, routes, migrations and assets. Devise is an example of an engine.

## 1. Generate
```bash
bin/rails plugin new billing --mountable    # isolated namespace, own routes, dummy app for tests
# in-repo engine: put it in engines/billing and reference it with path: in the Gemfile
gem "billing", path: "engines/billing"
```
`--full` generates an engine with an `app` tree, `config/routes.rb` and `lib/billing/engine.rb`; `--mountable` adds namespace isolation (`isolate_namespace`), asset manifests and mounts the engine in the dummy app at `test/dummy`. The guide highly recommends keeping the `isolate_namespace` line.

## 2. Isolation
```ruby
module Billing
  class Engine < ::Rails::Engine
    isolate_namespace Billing                 # Billing::Invoice, billing_ tables, billing.invoices_path
    initializer "billing.assets.precompile" do |app|
      app.config.assets.precompile += %w[admin.js admin.css]   # only for assets the host does not require itself
    end
  end
end
```
- Models are namespaced and their tables prefixed (`billing_invoices`); link into the engine from host views with the routing proxy (`billing.invoices_path`) and to the host from engine views with `main_app.root_path`.
- Engine routes are drawn on `Billing::Engine.routes.draw do ... end` in the engine's `config/routes.rb`.

## 3. Mounting and routes
```ruby
# host config/routes.rb
mount Billing::Engine => "/billing"
```
The guide's example is `mount Blorgh::Engine => "/blorgh"`; the engine's routes and helpers are isolated from the application's.

## 4. Migrations
`bin/rails billing:install:migrations` copies the engine's migrations into the host application (copied files get new timestamps and an engine suffix); `bin/rails railties:install:migrations` copies them from every engine, and `MIGRATIONS_PATH=` and `DATABASE=` options select the target.

## 5. Configuration and host coupling
```ruby
# lib/billing.rb
module Billing
  mattr_accessor :customer_class
end
# host config/initializers/billing.rb
Billing.customer_class = "Account"      # a String, converted with constantize inside the engine
```
- Avoid referencing host classes directly from the engine; configure them with a `mattr_accessor`. The guide warns to set the String name, not the class, so Rails does not load the class (and its table) too early.
- Initializers and locales work as in an application (`config/initializers`, `config/locales`).
- The host can reopen engine classes with `class_eval` or `ActiveSupport::Concern` and can preload overrides in a `config.to_prepare` block.

## 6. Testing
Generated engines include a dummy application at `test/dummy`, used as a mounting point for testing the engine; you can extend it.

## Verify
- [ ] Engine works mounted in the dummy app and the host; no direct references to host constants; migrations run once in the host; route helpers resolve with `billing.` and `main_app.`.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 Getting Started with Engines guide. Confirmed: `rails plugin new --mountable/--full` contents, `isolate_namespace`, namespaced models and tables, `mount ... => "/path"`, the routing proxy and `main_app`, `<engine>:install:migrations` and `railties:install:migrations` options, the `mattr_accessor` plus String configuration pattern, `config/initializers` and `config/locales` in engines, override techniques (`class_eval`, `ActiveSupport::Concern`, `to_prepare`), precompile initializer and the `test/dummy` app. Removed the Mission Control/Active Storage examples, the Devise-style `authenticate` mount, `paths["db/migrate"]`, `on_load` and packwerk advice, none of which the guide covers.

Method: documentation only; no commands were run.
