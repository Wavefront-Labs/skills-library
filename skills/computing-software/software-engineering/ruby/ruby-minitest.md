---
id: computing-software.software-engineering.ruby.ruby-minitest
name: ruby-minitest
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-testing-style, minitest]
level: intro
status: docs-checked
description: "Write Minitest tests with assertions, setup, and run them with rake."
sources: ["https://github.com/minitest/minitest"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Minitest unit tests and assertions
- `require "minitest/autorun"`; subclass `Minitest::Test`, define `setup` and `test_*` methods; `assert_equal`, `refute_match` and `skip` appear in the README example.
- Run a file with `ruby -Ilib:test test/foo_test.rb`; the run prints `--seed` so a failing order can be reproduced; `Rake::TestTask` generates `rake test`.
Verify: tests fail when logic is broken.

## Checked
2026-11-02. Confirmed against: Minitest README. Removed or softened (not stated on those pages): assert_raises/assert_in_delta/refute_nil detail, Minitest::Mock and stub, bin/rails test.
Method: documentation only; no commands were run.
