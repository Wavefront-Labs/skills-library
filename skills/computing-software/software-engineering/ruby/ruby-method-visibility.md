---
id: computing-software.software-engineering.ruby.ruby-method-visibility
name: ruby-method-visibility
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-modules, method-visibility]
level: practitioner
status: docs-checked
description: "Apply private, protected and public correctly, including the private-constant and private_class_method forms."
sources: ["https://raw.githubusercontent.com/ruby/ruby/master/doc/syntax/modules_and_classes.rdoc", "https://docs.ruby-lang.org/en/master/Module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Visibility private protected and module_function
- Public methods can be called from anywhere. A protected method may be called only when the sender inherits the class or module defining it. A private method may be called only inside the owner class without a receiver, or with a literal `self` receiver.
- `private_class_method`, `private_constant` and `module_function` are documented on `Module`; `module_function` turns an instance method into a module (class) method.
Verify: NoMethodError in tests when calling outside.

## Checked
2026-11-02. Confirmed against: modules_and_classes syntax doc and Module page. Removed or softened (not stated on those pages): private-with-no-args and private def forms, version tag.
Method: documentation only; no commands were run.
