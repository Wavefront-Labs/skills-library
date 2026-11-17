---
id: computing-software.software-engineering.ruby.ruby-constant-lookup-autoload
name: ruby-constant-lookup-autoload
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, constant-lookup-autoload, constants]
level: advanced
status: docs-checked
description: "Resolve Ruby constant lookup with Module.nesting: compact A::B versus nested modules, ::Const, inheritance and fix NameError."
sources: ["https://docs.ruby-lang.org/en/master/syntax/modules_and_classes_rdoc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Constant lookup and nesting

Which constants are accessible depends on the module nesting, that is, which syntax defined the module. `Module.nesting` shows the nesting.
```ruby
module A
  Z = 1
  module B
    p Module.nesting   #=> [A::B, A]
    p Z                #=> 1
  end
end

module A
  Z = 1
end
module A::B
  p Module.nesting     #=> [A::B]
  p Z                  # raises NameError: the nesting does not include A
end

Z = 0
module A
  Z = 1
  module B
    p ::Z              #=> 0: a leading :: references the top-level constant
  end
end
```
- `module Outer::Inner::GrandChild` needs `Outer` and `Outer::Inner` already defined, or it raises NameError. It saves indentation but changes the scope of constant lookup compared with nested `module` blocks.
- Inheritance: a class inherits methods and constants from its superclass, so `B < A` can reference `Z` defined in `A` from inside its methods.
- Instance methods defined in a module reach the constants of that module through the ancestors list once the module is included.
- When a class method references a constant it uses the same rules as outside the method, as the scope is the same.
- Reopening a class with a different superclass raises `TypeError: superclass mismatch`; omitting the superclass on reopen is fine.
- Reopen only modules you own; reopening others can cause naming conflicts and hard-to-diagnose bugs.

## Gotchas
- Switching from nested blocks to compact `A::B` style is the usual cause of "uninitialized constant" errors after a refactor, because the outer module leaves the nesting.
- Print `Module.nesting` where a NameError occurs to see what the lookup can reach.

## Checked

Date: 2026-11-08. Read in full: the Ruby syntax documentation for modules and classes (the raw rdoc source on GitHub). Removed: all `Module#autoload`, `autoload?`, `const_missing`, Zeitwerk and `rails zeitwerk:check` claims, the reassignment warning and thread-safety claims, and the freezing advice, as the Module class page is a stub at docs.ruby-lang.org and I did not read any page covering them. The Module class page was dropped from the sources.

Method: documentation only; no commands were run.
