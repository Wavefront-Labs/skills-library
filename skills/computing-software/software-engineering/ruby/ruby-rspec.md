---
id: computing-software.software-engineering.ruby.ruby-rspec
name: ruby-rspec
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-testing-style, rspec]
level: practitioner
status: draft
description: "Write RSpec examples with let, matchers, doubles and verified doubles."
sources: ["https://docs.ruby-lang.org/en/", "https://www.ruby-lang.org/en/documentation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RSpec describe it and matchers
- `RSpec.describe Foo do; let(:foo) { described_class.new }; it "adds" do; expect(foo.add(1, 2)).to eq(3); end; end`; matchers `raise_error`, `include`, `match`, `have_attributes`, `change { }.by(1)`.
- Prefer `instance_double(Class)` (verifies methods exist) to `double`; `allow(x).to receive(:y)`.
- `.rspec` with `--require spec_helper`; `rspec --bisect` finds order-dependent failures.
Verify: random order `config.order = :random`.
