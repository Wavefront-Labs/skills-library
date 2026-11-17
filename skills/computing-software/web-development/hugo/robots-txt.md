---
id: computing-software.web-development.hugo.robots-txt
name: robots-txt
category: computing-software
field: web-development
product: hugo
tags: [robots-txt, enablerobotstxt, crawler-rules, static-directory]
level: intro
status: docs-checked
description: "Generate robots.txt from a Hugo template with enableRobotsTXT, the embedded default, override locations, or ship a plain file from the static directory."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/templates/robots.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable template generation in project configuration:

```toml
enableRobotsTXT = true
```

By default Hugo uses an embedded template that outputs:

```text
User-agent: *
```

This tells search engines honoring the Robots Exclusion Protocol they may crawl everything.

To override the internal template, Hugo checks, in order:

1. `/layouts/robots.txt`
2. `/themes/<THEME>/layouts/robots.txt`

Example `layouts/robots.txt` that disallows every page:

```text
User-agent: *
{{ range .Pages }}
Disallow: {{ .RelPermalink }}
{{ end }}
```

To skip templating, set `enableRobotsTXT` to `false` and place a `robots.txt` file in the `static` directory. Hugo copies everything in `static` to the root of `public` when building.

## Checked

2026-11-04. Confirmed against the Hugo docs page robots.txt template: `enableRobotsTXT`, the embedded default output, the two-step lookup order, the Disallow example and the static-file alternative. Nothing removed.

Method: documentation only; no commands were run.
