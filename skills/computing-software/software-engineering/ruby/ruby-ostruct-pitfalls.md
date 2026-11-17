---
id: computing-software.software-engineering.ruby.ruby-ostruct-pitfalls
name: ruby-ostruct-pitfalls
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ostruct-pitfalls, data-structures]
level: intro
status: docs-checked
description: "Know when OpenStruct hurts (speed, typos, method clashes, bundled gem status) and pick Struct, Data or Hash instead."
sources: ["https://docs.ruby-lang.org/en/master/OpenStruct.html", "https://docs.ruby-lang.org/en/master/Data.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenStruct and when to avoid it

```ruby
require "ostruct"
o = OpenStruct.new(name: "Ann")
o.age = 3
o.missing            # nil (no error!)
o[:name]; o.to_h; o.dig(:a, :b)
o.respond_to?(:age)  # true only once set
```
Problems:
- Unknown attributes return `nil`, so typos (`o.nmae`) pass silently.
- Slower than a Hash or Struct: it uses `method_missing` and `define_singleton_method`. The gem's docs say creating one from a small Hash and accessing a few entries can be 200 times slower than using the hash directly.
- Attribute names can overwrite built-in methods (`o.methods = [:foo]` replaces `methods`). OpenStruct provides `!`-suffixed aliases such as `o.class!` for the built-ins, and recommends not using fields ending in `!`.
- Ruby 4.0 promoted ostruct from a default gem to a bundled gem, so add `gem "ostruct"` to your Gemfile when running under Bundler.
- Building one from untrusted data (for example a JSON web request) can mount a "symbol denial of service" attack, because keys create methods and method names are never garbage collected. The docs conclude "consider not using OpenStruct at all".

Prefer:
```ruby
Point = Struct.new(:x, :y, keyword_init: true)   # mutable, known fields
Money = Data.define(:cents, :currency)           # immutable value object, added in Ruby 3.2
config = { retries: 3 }.freeze                    # plain hash with fetch(:retries)
```
Use `Hash#fetch` for optional config so missing keys raise or default explicitly.

Verify: construct each type, call a misspelled accessor, and confirm only the Struct/Data versions raise NoMethodError.

## Checked
2026-11-03. Confirmed against the ruby/ostruct `lib/ostruct.rb` header docs and `method_missing` (unknown reader returns `@table[mid]`, i.e. nil; `[]`, `dig`, `to_h`; the 200 times figure; `!` aliases; symbol DoS caveat), `doc/NEWS/NEWS-4.0.0.md` (ostruct promoted to a bundled gem) and `doc/NEWS/NEWS-3.2.0.md` (`Data.define`, Struct without `keyword_init: true`). Removed: Ruby 3.5 removal plan, the `JSON.parse(object_class: OpenStruct)` claim and "Ruby warns for some".
Method: documentation only; no commands were run.
