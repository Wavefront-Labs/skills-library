---
id: computing-software.web-development.hugo.embedded-partials
name: embedded-partials
category: computing-software
field: web-development
product: hugo
tags: [embedded-templates, opengraph, schema, twitter-cards, disqus]
level: practitioner
status: docs-checked
description: "Use Hugo's six embedded partials: Disqus, Google Analytics, Open Graph, pagination, schema and X cards, with their config, privacy settings and override rule."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/templates/embedded.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hugo has six embedded partials. Call each with `partial` and the current context. To customize one, copy its source into a file of the same name in `layouts/_partials`.

```go-html-template
{{ partial "disqus.html" . }}
{{ partial "google_analytics.html" . }}
{{ partial "opengraph.html" . }}
{{ partial "pagination.html" . }}
{{ partial "schema.html" . }}
{{ partial "twitter_cards.html" . }}
```

- **Disqus:** set `services.disqus.shortname`. Front matter `disqus_identifier`, `disqus_title`, `disqus_url`. `privacy.disqus.disable` (default `false`) turns it off. Local previews show a notice instead of the widget.
- **Google Analytics (GA4):** measurement ID at `services.googleAnalytics.id`. `privacy.googleAnalytics.disable` (default `false`) and `privacy.googleAnalytics.respectDoNotTrack` (default `true`).
- **Open Graph:** uses `params.description`, `params.images`, `params.social.facebook_app_id` plus front matter. Emits `og:` tags, up to six images, audio and videos, and up to seven `og:see_also` tags from the same series.
- **Pagination:** formats `default` and `terse`.
- **Schema:** microdata `meta` elements. Keywords come from the `keywords` taxonomy, the `keywords` front matter, the `tags` taxonomy, then all taxonomy terms.
- **X (Twitter) Cards:** `twitter:card` is `summary_large_image` when an image is found, otherwise `summary`. `twitter:site` uses `params.social.twitter`, adding `@` if missing.

## Checked

2026-11-04: the six partial names, override location, Disqus config and front matter, privacy defaults, Google Analytics 4 id, Open Graph image/tag limits (6 images, 7 og:see_also), pagination formats, schema keyword order and X card behaviour confirmed against the Hugo docs Embedded partial templates page. Nothing removed.

Method: documentation only; no commands were run.
