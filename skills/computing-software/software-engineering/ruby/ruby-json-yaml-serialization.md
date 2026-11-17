---
id: computing-software.software-engineering.ruby.ruby-json-yaml-serialization
name: ruby-json-yaml-serialization
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, json-yaml-serialization, serialization]
level: practitioner
status: draft
description: "Read and write JSON and YAML in Ruby safely: symbolize_names, pretty_generate, to_json hooks, YAML.safe_load permitted classes."
sources: ["https://docs.ruby-lang.org/en/master/JSON.html", "https://docs.ruby-lang.org/en/master/Psych.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# JSON and YAML (Psych)

```ruby
require "json"; require "yaml"
data = JSON.parse(text, symbolize_names: true)
JSON.generate(data)           # compact
JSON.pretty_generate(data)    # indented
JSON.parse(text, max_nesting: 20)  # default depth limit is 100

class Money
  def initialize(c) = @c = c
  def to_json(*a) = { cents: @c }.to_json(*a)   # accept and forward *a
end

YAML.safe_load(File.read("c.yml"), permitted_classes: [Date, Symbol], aliases: false)
YAML.load_file("c.yml")       # Psych 4 (Ruby 3.1+): load is safe_load-like
```

## Gotchas
- `JSON.parse` raises `JSON::ParserError` on bad input and also on empty string or `nil`; rescue it at boundaries.
- Symbol keys become strings on round trip: `{a: 1}.to_json` parses back as `"a"`.
- `JSON.parse` of `NaN`, large integers and floats: big integers stay exact (Integer) but floats lose precision; use `decimal_class: BigDecimal` for money.
- Psych 4 (bundled since Ruby 3.1) makes `YAML.load` safe by default, and `YAML.unsafe_load` restores object instantiation. Never feed untrusted YAML to `unsafe_load` or to `Marshal`; see the deserialisation skill.
- YAML 1.1 quirks: unquoted `no`, `on`, `1e3`, `0123` and dates become booleans, floats, octals or Date objects. Quote strings that must stay strings.

Verify: `YAML.safe_load("a: 2026-01-01")` raises `Psych::DisallowedClass` until Date is permitted; `YAML.safe_load("a: no")` returns `false`.
