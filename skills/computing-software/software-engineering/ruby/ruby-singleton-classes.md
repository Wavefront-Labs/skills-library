---
id: computing-software.software-engineering.ruby.ruby-singleton-classes
name: ruby-singleton-classes
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, singleton-classes, object-model]
level: advanced
status: docs-checked
description: "Understand singleton classes, class methods, ancestors and method lookup, and when to use class << self or extend."
sources: ["https://docs.ruby-lang.org/en/master/syntax/modules_and_classes_rdoc.html", "https://docs.ruby-lang.org/en/master/Object.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Singleton classes and the object model

Every object can have a hidden singleton class holding methods for that one object. "Class methods" are just singleton methods of the class object.

```ruby
class Config
  class << self                 # opens Config's singleton class
    attr_accessor :env
    def load(path) = new(path)
    private def secret = "x"    # private class method
  end
end
obj = Object.new
def obj.hello = "hi"            # singleton method
obj.singleton_methods           # [:hello]
obj.singleton_class.instance_methods(false)

module Greeter; def hi = "hi"; end
obj.extend(Greeter)             # same as obj.singleton_class.include(Greeter)
Config.extend(Greeter)          # adds class-level methods
```
Method lookup walks `obj.singleton_class.ancestors`: singleton class, extended modules, the class, its included/prepended modules, superclasses, Object, Kernel, BasicObject. Inspect with `Config.singleton_class.ancestors` and `obj.method(:hello).owner`.

## Gotchas
- `private` inside `class << self` is how you make class methods private; plain `private` above `def self.x` does nothing to them (use `private_class_method :x`).
- Singleton methods are inherited by subclasses of a class (class methods inherit) but not by `dup`ed objects; `clone` keeps them.
- Class variables (`@@vars`) are shared between a class, its subclasses and its instances, so they are easy to share by accident.
- `Marshal.dump` cannot dump objects which define singleton methods (its docs list them as not dumpable).

Verify: in irb, print `Config.singleton_class.ancestors.first(3)` and `obj.dup.respond_to?(:hello)` (false) versus `obj.clone` (true).

## Checked
2026-11-03. Confirmed against ruby/ruby `doc/syntax/modules_and_classes.rdoc` (singleton classes, `class << self`), `doc/syntax/assignment.rdoc` (class variables shared with subclasses), `marshal.c` (objects with singleton methods cannot be dumped), `vm_method.c` (`private_class_method`), `object.c` (`singleton_class`; clone attaches a cloned singleton class, dup setup does not). Removed: the claim about class-level instance variables.
Method: documentation only; no commands were run.
