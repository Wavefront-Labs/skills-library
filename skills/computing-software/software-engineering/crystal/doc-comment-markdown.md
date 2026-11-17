---
id: computing-software.software-engineering.crystal.doc-comment-markdown
name: doc-comment-markdown
category: computing-software
field: software-engineering
product: crystal
tags: [doc-comment-markdown, doc-comments, documentation, markdown, ditto, nodoc, api-docs, rdoc-like, code-sample, crystal]
level: practitioner
status: draft
description: "Document types and methods with # comments in Markdown, code samples, :ditto:, :nodoc: and cross-reference links."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing doc comments

Goal: write useful API docs.

- Comments directly above a class, module, def, macro, constant or alias become docs; Markdown supported.
- First paragraph is the summary shown in lists; keep it one line.
- Code fences with `crystal` are highlighted; examples often use `# => result` convention.
- Links to other items: `` `Foo#bar` `` and `` `Foo.baz` `` backticked names are auto-linked.
- Directives: `# :nodoc:` hides the item (and nested items), `# :ditto:` copies the previous doc, `# :inherit:` inherits docs from an ancestor method (confirm).
- Admonitions: `NOTE:`, `WARNING:`, `DEPRECATED:`, `TODO:` etc. at paragraph start are styled.
- Module-level docs belong in the main file's top comment.

Gotchas:
- Doc samples are not executed; keep them correct manually or copy into specs.
- A blank line between comment and def detaches it.
- Private methods are not documented.

Verify: `crystal docs` and view the page.
