---
id: computing-software.software-engineering.ruby.ruby-refinements
name: ruby-refinements
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-modules, refinements]
level: advanced
status: docs-checked
description: "Scope monkey patches with refine/using instead of global core class reopening."
sources: ["https://raw.githubusercontent.com/ruby/ruby/master/doc/syntax/refinements.rdoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Refinements
- Plain monkey patching changes a class globally for every user; refinements (`refine` inside a module, activated with `using`) limit the change. See the syntax guide for activation scope.
- Prefer plain helper objects when a refinement is not needed.
Verify: confirm the method is absent where `using` is not in effect.

## Checked
2026-11-02. Confirmed against: refinements syntax doc: monkey-patch motivation. Removed or softened (not stated on those pages): scope/reflection limits and version claims (not stated in the page).
Method: documentation only; no commands were run.
