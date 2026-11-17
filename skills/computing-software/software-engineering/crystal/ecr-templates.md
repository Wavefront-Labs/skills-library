---
id: computing-software.software-engineering.crystal.ecr-templates
name: ecr-templates
category: computing-software
field: software-engineering
product: crystal
tags: [ecr-templates, crystal-for-rubyists, ecr, embedded-crystal, templates, html-escape, ecr-embed, def-to-s, views, slang, crystal]
level: practitioner
status: draft
description: "Render text and HTML with ECR (Embedded Crystal): ECR.def_to_s, ECR.embed, escaping and layouts."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ECR templates and string building

Goal: template output at compile time.

- Template file `views/hello.ecr`: `Hello <%= name %>! <% items.each do |i| %><li><%= i %></li><% end %>`.
- Class: `class Page; def initialize(@name : String); end; ECR.def_to_s "views/hello.ecr"; end` then `Page.new("x").to_s`.
- Embed into any IO: `ECR.embed "views/hello.ecr", io` (path is relative to the project root at compile time).
- Trim markers `<%-` and `-%>`; comments `<%# ... %>`; literal `<%% %>`.
- Escape: `HTML.escape(s)` for user data; ECR does NOT auto-escape.

Gotchas:
- Template compile errors point into generated code; keep logic out of templates.
- Templates are embedded at compile time, so edits need a rebuild.
- Alternative engines: Slang, Kilt (shards).

Verify: render and compare to the expected HTML in a spec.
