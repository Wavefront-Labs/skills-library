---
id: computing-software.software-engineering.ruby.ruby-simplecov-coverage
name: ruby-simplecov-coverage
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, simplecov-coverage, testing]
level: practitioner
status: docs-checked
description: "Measure Ruby test coverage with SimpleCov: start order, branch coverage, thresholds, patch coverage and the simplecov CLI."
sources: ["https://github.com/simplecov-ruby/simplecov"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test coverage with SimpleCov

SimpleCov gathers data with Ruby's built-in Coverage library and adds filtering, grouping, merging and formatting. It works with any test framework, because it watches what code executes.

```ruby
# Gemfile
gem 'simplecov', require: false, group: :test

# Very top of test/test_helper.rb, spec/spec_helper.rb, rails_helper.rb or features/support/env.rb
require 'simplecov'
SimpleCov.start do
  enable_coverage :branch            # track branches as well as lines
  cover "{app,lib}/**/*.rb"          # report on these files, even if never loaded
  skip "app/legacy"                  # leave these out
  group "Models", "app/models"       # organise the report into groups
  coverage :line do
    minimum 90                       # fail the suite below 90% line coverage
    maximum_drop 1                   # ...or when coverage drops more than 1%
    maximum_missed 5, per: :file     # no file may carry more than 5 uncovered lines
  end
  coverage :branch, minimum: 80, ignore: :implicit_else
end
```
- Configuration goes in the start block, or in a `.simplecov` file at the project root when several suites share it. Legacy spellings of the old configuration API still work but warn and name their replacement; `deprecations :raise` turns them into errors. Configuration options are documented in the repo's docs/Configuration.md (not read for this check).
- Rails: `SimpleCov.start 'rails'` is a built-in profile that groups Controllers, Models, Helpers and Libraries. `cover_views` adds ERB, Haml and Slim templates.
- Results from several test types are cached and merged, so one report covers the whole suite.
- Bundled formatters are HTML and JSON. Open the report with `simplecov open`, and consider adding `coverage` to `.gitignore`.
- `track_tests` records which test covers each line; `simplecov tests lib/foo.rb:42` lists them and `simplecov affected --base main --run bundle exec rspec` runs only the tests touching changed code.
- `simplecov patch --base main --minimum 100` scores only the lines changed against a base ref and can gate a pull request.
- `simplecov ratchet` writes a checked-in per-file baseline whose floors only tighten; each successful run appends to `coverage/.history.json`, shown with `simplecov history`.
- Other CLI subcommands named in the README: `watch`, `show`, `status`, `uncovered --missing`, `badge --output badge.svg`.

## Gotchas
- `SimpleCov.start` must run before any application code is required; otherwise SimpleCov and Coverage cannot track those files. This hits tools that keep the app loaded between runs, such as Spring.
- SimpleCov must run in the process you want to analyse. To cover a server started separately from the test process, require it in the server process, for Rails near the top of `bin/rails` after `config/boot`, guarded by `ENV['RAILS_ENV'] == 'test'`.
- Recording with `track_tests` has a real cost, which is why it is opt-in.

## Checked

Date: 2026-11-08. Read in full: the SimpleCov README on GitHub. Not read: the linked docs pages (Configuration, CLI, Troubleshooting, Production). Removed: `add_filter`, `add_group`, `minimum_coverage`, `track_files`, `SimpleCov.collate`, `command_name` and `at_fork` APIs, report file names other than `.history.json`, the exit status 2 claim, `simplecov-lcov` and the bootsnap claim, since the README does not state them.

Method: documentation only; no commands were run.
