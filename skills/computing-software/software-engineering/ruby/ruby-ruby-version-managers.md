---
id: computing-software.software-engineering.ruby.ruby-ruby-version-managers
name: ruby-ruby-version-managers
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-bundler, ruby-version-managers]
level: intro
status: draft
description: "Pin Ruby versions with .ruby-version and rbenv, asdf or chruby, and diagnose load path issues."
sources: ["https://docs.ruby-lang.org/en/", "https://www.ruby-lang.org/en/documentation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ruby version managers and environment
- `.ruby-version` read by rbenv/chruby/asdf (`.tool-versions`); Bundler honours `ruby` in the Gemfile.
- Diagnose with `ruby -v`, `which ruby`, `gem env`, `bundle env`, `ruby -e 'puts $LOAD_PATH'`.
- Avoid system Ruby on macOS/Linux distros for apps.
Verify: CI reads the same version file.
