---
id: computing-software.web-development.hugo.dev-server-config
name: dev-server-config
category: computing-software
field: web-development
product: hugo
tags: [server-config, dev-server, redirects, headers, spa-rewrite]
level: practitioner
status: docs-checked
description: "Configure Hugo's development server: custom response headers, redirect and rewrite rules, the 404 redirect, and ordering in multilingual projects."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Server settings apply only to the development server. Put them in a development configuration directory, for example `config/development/server.toml`.

By default the server redirects unknown URLs to `/404.html`.

Custom headers (useful for testing a Content Security Policy):

```toml
[[headers]]
for = '/**'

[headers.values]
X-Frame-Options = 'DENY'
X-Content-Type-Options = 'nosniff'
```

Redirect keys: `from` (glob) or `fromRe` (regular expression, with `$1`, `$2` in `to`), `fromHeaders` (map of header names to globs), `to`, `status` and `force`. Either `from` or `fromRE` must be set. A status of 200 rewrites the URL, typically what single-page applications need.

```toml
[[redirects]]
from = '/myspa/**'
to = '/myspa/'
status = 200
force = false
```

If you define other redirects you must add the 404 redirect explicitly:

```toml
[[redirects]]
from   = '/**'
to     = '/404.html'
status = 404
```

In multilingual projects, the default language's 404 redirect must be defined last. When the default language is served from a subdirectory, its catch-all points at that language's 404 page, for example `/en/404.html`.

## Checked

2026-11-04. Confirmed against the Hugo docs page Configure server: development-only scope and the `config/development/server.toml` layout, the default 404 redirect, the header example, the redirect keys and the `fromRe` and `$1` behaviour, the status 200 rewrite, and the multilingual 404 ordering. Nothing removed.

Method: documentation only; no commands were run.
