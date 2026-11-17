---
id: computing-software.software-engineering.ruby.ruby-method-objects-to-proc
name: ruby-method-objects-to-proc
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, method-objects-to-proc, functional]
level: practitioner
status: docs-checked
description: "Use Method objects, Symbol#to_proc, curry and composition (>> <<) to pass behaviour around in Ruby."
sources: ["https://docs.ruby-lang.org/en/master/Method.html", "https://docs.ruby-lang.org/en/master/Proc.html", "https://docs.ruby-lang.org/en/master/Symbol.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Method objects and to_proc

```ruby
words.map(&:upcase)                 # Symbol#to_proc: ->(w) { w.upcase }
m = 5.method(:+)                    # bound Method
[1, 2].map(&m)                      # [6, 7]
um = Array.instance_method(:size)   # UnboundMethod
um.bind_call([1, 2, 3])             # 3
m.owner; m.receiver; m.arity; m.source_location; m.parameters

compose = ->(x) { x + 1 } >> ->(x) { x * 2 }   # f >> g = g(f(x))
(method(:Integer) >> :to_s.to_proc).call("42")
add = ->(a, b, c) { a + b + c }
add.curry[1][2][3]                  # 6
add.curry.(1, 2).(3)

def double(x) = x * 2
%w[1 2].map(&method(:Integer)).map(&method(:double))
```
Method objects keep their receiver; `Method#unbind` gives an UnboundMethod that can only be called after `bind`ing it to an object that is `kind_of?` the method's original class (otherwise `TypeError`: "bind argument must be an instance of ...").

## Gotchas
- `Symbol#to_proc` calls the named method on the first argument and passes the rest, so `inject(&:+)` works (two args) but `[1, 2].map(&:+)` fails (no argument for `+`). The proc is a lambda.
- Lambdas check arity; procs do not. `method(:x).to_proc` is a lambda.
- `define_method(:name, method_obj)` accepts a Proc, Method or UnboundMethod, but the method's owner must be the class, an ancestor or a module, else `TypeError`.
- Currying a lambda with fixed arity: `add.curry[1, 2][3]` is 6, but passing too many arguments (`add.curry[1, 2][3, 4]`) raises `ArgumentError` ("given 4, expected 3").
- `m.source_location` returns `[file, line]` for Ruby-defined methods and `nil` for C-defined ones such as `Kernel.method(:puts)`.

Verify: `[1,2,3].map(&10.method(:+))` returns `[11, 12, 13]`; `add.curry[1][2]` returns a lambda, not a number.

## Checked
2026-11-03. Confirmed against ruby/ruby `proc.c` rdoc and source (`Symbol#to_proc` and its lambda-ness, `Method#to_proc` lambda, `Proc#curry` and `Method#curry`, `>>` and `<<` composition on Proc and Method, `UnboundMethod#bind` and `bind_call`, the kind_of? rule and TypeError text, `define_method` accepted forms, `source_location` nil for C methods). Removed: the "modules' methods bind to any object since Ruby 2.0" claim, the slow-`Symbol#to_proc` claim.
Method: documentation only; no commands were run.
