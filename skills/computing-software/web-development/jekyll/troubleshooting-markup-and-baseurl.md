---
id: computing-software.web-development.jekyll.troubleshooting-markup-and-baseurl
name: troubleshooting-markup-and-baseurl
category: computing-software
field: web-development
product: jekyll
tags: [baseurl-troubleshooting, excerpt-liquid-errors, liquid-braces, symlink-production]
level: practitioner
status: docs-checked
description: "Diagnose Jekyll quirks: baseurl sites needing the full path locally, excerpts raising Liquid errors, Liquid 2.0 brace escapes and missing static files in production."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Base URL: with

```sh
jekyll serve --baseurl '/blog'
```

open `http://localhost:4000/blog/index.html`. Plain `http://localhost:4000/blog` will not work.

Excerpts: since v1.0.0 posts get automatic excerpts, and since v1.1.0 they also pass through Liquid, which can produce odd errors when references do not exist or a tag is not closed. Try setting `excerpt_separator: ""` in `_config.yml`, or a nonsense string.

Liquid 2.0 appears to break the use of the escaped double-brace output syntax in templates, raising:

```
'{{ "{{" }}' was not properly terminated with regexp: /\}\}/  (Liquid::SyntaxError)
```

Production: since 3.2.0, if a static file cannot be found during a production build, set the environment to `production`. The cause is trying to copy a non-existing symlink.

If you hit a bug, report it as a GitHub issue with any workaround you find.

## Checked

2026-11-04. Confirmed against the Jekyll Troubleshooting page: baseurl access path, excerpt Liquid errors (1.0.0 and 1.1.0), Liquid 2.0 brace error and the 3.2.0 production symlink note. Removed the JEKYLL_ENV=production command, which the page does not give (it only says to set the environment to production).

Method: documentation only; no commands were run.
