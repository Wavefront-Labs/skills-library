---
id: computing-software.web-development.mkdocs.validation-strictness
name: validation-strictness
category: computing-software
field: web-development
product: mkdocs
tags: [validation, link-checking, strict-mode, anchors]
level: advanced
status: docs-checked
description: "Tune MkDocs link and nav diagnostics with the validation tree (warn, info, ignore), defaults as of 1.6, and a maximal-strictness setup for CI."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`validation` (new in 1.5) sets severity per diagnostic: `warn`, `info` or `ignore`. `warn` is meant for `mkdocs build --strict`, where it becomes an error.

Defaults as of 1.6:

```yaml
validation:
  nav:
    omitted_files: info
    not_found: warn
    absolute_links: info
  links:
    not_found: warn
    anchors: info
    absolute_links: info
    unrecognized_links: info
```

Recommended for most sites (maximal strictness):

```yaml
validation:
  omitted_files: warn
  absolute_links: warn  # or relative_to_docs (1.6)
  unrecognized_links: warn
  anchors: warn
```

Shorthand: in the examples the `nav` and `links` keys are omitted; `absolute_links:` means setting both `nav: absolute_links:` and `links: absolute_links:`. Set only the items that differ from defaults.

Example messages: broken link target ("target is not found among documentation files"), missing anchor, unrecognized relative link.

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Configuration" (validation: levels, 1.6 defaults, maximal-strictness example, `relative_to_docs`, message examples). Removed the Verify line, which the page does not state.
Method: documentation only; no commands were run.
