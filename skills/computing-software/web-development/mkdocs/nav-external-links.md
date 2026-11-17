---
id: computing-software.web-development.mkdocs.nav-external-links
name: nav-external-links
category: computing-software
field: web-development
product: mkdocs
tags: [nav, external-links, relative-urls, site-url]
level: practitioner
status: docs-checked
description: "Add external or sibling-site links to MkDocs nav; titles are mandatory for external items and unknown paths are treated as external."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nav entries may point outside the site. A title is optional for internal pages but required for external links. Any path not found among the docs files is assumed to be an external link; it may be a full URL or a relative URL.

```yaml
nav:
  - Introduction: 'index.md'
  - 'about.md'
  - 'Issue Tracker': 'https://example.com/'
```

When the site lives in a subdirectory of a bigger site, relative URLs reach siblings:

```yaml
site_url: https://example.com/foo/

nav:
  - Home: '../'
  - 'User Guide': 'user-guide.md'
  - 'Bug Tracker': '/bugs/'
```

Here `Home` steps up to `https://example.com/` and `Bug Tracker` is an absolute path from the server root (`https://example.com/bugs/`).

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (nav): optional titles for internal links, required for external ones, unknown paths assumed external, full or relative URL, both examples and the `Home` and `Bug Tracker` resolution. Removed: a gotcha about typos and validation that the page does not state, and a generic verify line.

Method: documentation only; no commands were run.
