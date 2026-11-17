---
id: computing-software.web-development.rails.upgrading-rails-versions
name: upgrading-rails-versions
category: computing-software
field: web-development
product: rails
tags: [rails, rails-upgrade, load-defaults, new-framework-defaults, deprecations, dual-boot, ruby, web-development]
level: practitioner
status: docs-checked
description: "Upgrading Rails safely: one minor version at a time, deprecation cleanup, bin/rails app:update, new_framework_defaults files, load_defaults and gem compatibility."
sources:
  - https://guides.rubyonrails.org/upgrading_ruby_on_rails.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading Rails versions

**Goal:** move to the next Rails version in small, reversible steps with a green test suite at each one.

## 1. Preconditions
- Good test coverage of critical paths (the upgrade's safety net).
- On the latest patch of your current minor (e.g. 7.1.x latest) with **zero deprecation warnings**.
- Ruby version supported by the target (Rails 8.0 and 8.1 require Ruby 3.2.0 or newer; 7.2 requires 3.1.0 or newer).
- Upgrade one minor at a time: 7.0 -> 7.1 -> 7.2 -> 8.0, so the deprecation warnings do their job.

## 2. Surface deprecations
Run the suite on the current version, read the deprecation warnings and fix them before bumping.

## 3. Gems
```bash
bundle outdated
bundle update rails
```
Check each gem's changelog for support of the target Rails. Replace abandoned gems first.

## 4. Update config
```bash
bin/rails app:update        # run after bumping the Rails version in the Gemfile; interactive; creates config/initializers/new_framework_defaults_X_Y.rb
```
Review each diff. Keep `config.load_defaults <old>` initially. Then, in `config/initializers/new_framework_defaults_8_0.rb`, uncomment flags gradually over several deployments and verify. When the app runs with the new defaults, delete the file and flip `config.load_defaults`.

## 5. Roll out
Deploy to staging, run smoke and E2E tests, watch error tracker and performance; deploy production with an easy rollback (previous image).

## Checked
2026-10-31. Confirmed against the Rails Upgrading guide: Ruby minimums for 7.2 and 8.0/8.1, one minor version at a time, `bin/rails app:update` run after bumping the Gemfile, `new_framework_defaults_X_Y.rb` enabled gradually then removed and `load_defaults` flipped. Removed: `--conservative`, `next_rails`/`bootboot` dual-boot specifics, the per-version feature list, the data-affecting-flags remark and the `deprecation = :raise` snippet (not in the guide).
Method: documentation only; no commands were run.

## Verify
- [ ] Test suite green with deprecations raising.
- [ ] `config.load_defaults` matches the Rails version and `new_framework_defaults` file removed.
- [ ] Error rates and p95 latency unchanged a week after release.
