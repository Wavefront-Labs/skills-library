---
id: computing-software.software-engineering.crystal.spec-describe-it
name: spec-describe-it
category: computing-software
field: software-engineering
product: crystal
tags: [spec-describe-it, spec-framework, spec, describe, it, should, expect, eq, be-nil, be-true, contain, expect-raises, pending, matchers, testing, crystal]
level: intro
status: draft
description: "Write specs with describe, context and it, use should/expect syntax, eq, be_nil, contain, raise matchers and pending."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# describe, it and expectations

Goal: test Crystal code.

```crystal
require "./spec_helper"
describe Foo do
  it "adds" do
    Foo.add(1, 2).should eq(3)
  end
  it "fails on bad input" do
    expect_raises(ArgumentError, /negative/) { Foo.add(-1, 2) }
  end
  pending "later" do
  end
end
```
- Matchers: `eq`, `be`, `be_a(T)`, `be_nil`, `be_true`, `be_false`, `be_truthy`, `be_falsey`, `be_close(x, delta)`, `be < 5`, `contain`, `start_with`, `end_with`, `match(/re/)`, `be_empty`; negate with `.should_not`.
- `Spec` is stdlib (`require "spec"` auto in `crystal spec`).
- Failures print file:line and expected/got.
- Use `it "name", focus: true` / `tags: "slow"` options.

Gotchas:
- Nilable receivers: `x.should eq(1)` on `Int32?` is fine; use `x.not_nil!` only when needed.
- Every spec file shares one process and global state.
- Use `describe` with a type to get automatic grouping in output.

Verify: `crystal spec` shows `N examples, 0 failures`.
