---
id: computing-software.software-engineering.ruby.ruby-building-gems
name: ruby-building-gems
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-bundler, building-gems]
level: advanced
status: docs-checked
description: "Create a gemspec, version and release a gem to RubyGems with MFA."
sources: ["https://guides.rubygems.org/make-your-own-gem/", "https://guides.rubygems.org/specification-reference/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building and publishing a gem
- `bundle gem name` scaffolds the gem, including `lib/name/version.rb` which defines the `VERSION` constant the gemspec reads.
- The gemspec declares `required_ruby_version`, `add_dependency` and `add_development_dependency`.
- `gem build name.gemspec` produces the .gem; `gem install ./name-0.0.0.gem` tests it locally; `gem push` publishes it.
Verify: install the built .gem into a clean GEM_HOME.

## Checked
2026-11-02. Confirmed against: RubyGems make-your-own-gem guide and specification reference. Removed or softened (not stated on those pages): MFA metadata, gem yank, semantic versioning claims, minimal files list.
Method: documentation only; no commands were run.
