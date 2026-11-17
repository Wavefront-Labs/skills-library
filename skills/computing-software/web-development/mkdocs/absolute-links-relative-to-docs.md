---
id: computing-software.web-development.mkdocs.absolute-links-relative-to-docs
name: absolute-links-relative-to-docs
category: computing-software
field: web-development
product: mkdocs
tags: [absolute-links, relative-to-docs, validation, internal-links]
level: advanced
status: docs-checked
description: "Opt in to MkDocs 1.6 absolute links that start with a slash and resolve against docs_dir, validated like relative links."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Historically MkDocs only recognised relative links to `*.md` files; absolute links were left unmodified or warned against. Since 1.6 you can opt in:

```yaml
validation:
  links:
    absolute_links: relative_to_docs
    anchors: warn
    unrecognized_links: warn
```

With `relative_to_docs`, every Markdown link starting with `/` is read as relative to the `docs_dir` root and validated by the same rules as relative links. In HTML output the links are still turned relative so the site works reliably.

So `dir1/foo.md` can link to `dir2/bar.md` as:

```markdown
[link](/dir2/bar.md)
```

in addition to `[link](../dir2/bar.md)`.

Not enabled by default: the default is still to skip the link.

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (Validation of absolute links, new in 1.6): the `relative_to_docs` value, the example config, and the `/dir2/bar.md` link example. Removed: a claim about raw HTML and a generic verify line the page does not state.

Method: documentation only; no commands were run.
