---
id: computing-software.software-engineering.ruby.ruby-erb-templating
name: ruby-erb-templating
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, erb-templating, templates]
level: practitioner
status: draft
description: "Render text and config files with ERB: trim modes, binding scope, ERB::Util.html_escape and safe templating of user input."
sources: ["https://docs.ruby-lang.org/en/master/ERB.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ERB templating

```ruby
require "erb"
tpl = ERB.new(<<~T, trim_mode: "-")
  <% items.each do |i| -%>
  * <%= ERB::Util.html_escape(i) %>
  <% end -%>
T
Struct.new(:items) { def render(t) = t.result(binding) }.new(%w[a <b>]).render(tpl)
# or pass explicit locals:
tpl.result_with_hash(items: %w[a b])
```
Tags: `<% code %>`, `<%= expression %>`, `<%# comment %>`, `<%% literal %>`. `trim_mode: "-"` enables `-%>` to eat the newline and `<%-` to strip leading indentation; `"<>"` and `">"` are line-based alternatives.

## Gotchas
- `<%= %>` does not escape. In HTML, wrap user data with `ERB::Util.html_escape` (alias `h` when included); Rails views escape automatically but plain ERB does not.
- `result(binding)` exposes every local and private method of the binding; use `result_with_hash` for narrower scope.
- Never build a template string from untrusted input: ERB evaluates arbitrary Ruby, so that is remote code execution (server-side template injection). Only render templates you control.
- Config generation: escape for the target language (YAML, shell, JSON), not just HTML; for YAML values use `to_json`.
- Templates compile each time you create `ERB.new`; cache the object for hot paths.

Verify: render an item `<script>` and confirm the output contains `&lt;script&gt;`; check the file has no stray blank lines after enabling trim mode.
