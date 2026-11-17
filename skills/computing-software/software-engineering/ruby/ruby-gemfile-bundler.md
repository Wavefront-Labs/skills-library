---
id: computing-software.software-engineering.ruby.ruby-gemfile-bundler
name: ruby-gemfile-bundler
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-bundler, gemfile-bundler]
level: practitioner
status: draft
description: "Manage dependencies with Gemfile, lockfile, groups and bundle exec."
sources: ["https://docs.ruby-lang.org/en/", "https://www.ruby-lang.org/en/documentation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gemfile Gemfile.lock and bundle exec
- `Gemfile`: `source "https://rubygems.org"`, `ruby "3.3.0"`, `gem "rails", "~> 7.1"`, groups `group :test do ... end`; pessimistic `~> 1.2` allows >=1.2 <2.0, `~> 1.2.3` allows <1.3.
- Commit `Gemfile.lock` (apps and, today, gems too); `bundle install`, `bundle update gem --conservative`, `bundle exec cmd`, `bundle outdated`, `bundle audit` (bundler-audit gem).
- Deployment: `bundle config set --local without 'development test'` and `bundle install --frozen` equivalent via `BUNDLE_FROZEN`.
Verify: `bundle check`.
