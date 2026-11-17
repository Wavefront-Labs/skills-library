---
id: computing-software.web-development.jekyll.url-and-date-filters
name: url-and-date-filters
category: computing-software
field: web-development
product: jekyll
tags: [relative-url, absolute-url, date-filters, date-to-xmlschema, date-to-rfc822, ordinal-dates]
level: practitioner
status: docs-checked
description: "Use Jekyll's URL and date Liquid filters: relative_url, absolute_url, date_to_xmlschema, date_to_rfc822, date_to_string and the long and ordinal variants."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_data/jekyll_filters.yml
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/liquid/filters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
URL filters:

- `relative_url` prepends the `baseurl` config value; recommended when the site lives on a subpath.
- `absolute_url` prepends `url` and `baseurl`.

```liquid
{{ "/assets/style.css" | relative_url }}   => /my-baseurl/assets/style.css
{{ "/assets/style.css" | absolute_url }}   => http://example.com/my-baseurl/assets/style.css
```

Date filters (shown with `site.time`):

```liquid
{{ site.time | date_to_xmlschema }}   => 2008-11-07T13:07:54-08:00
{{ site.time | date_to_rfc822 }}      => Mon, 07 Nov 2008 13:07:54 -0800
{{ site.time | date_to_string }}      => 07 Nov 2008
{{ site.time | date_to_long_string }} => 07 November 2008
```

- `date_to_xmlschema`: ISO 8601.
- `date_to_rfc822`: format used by RSS feeds.
- Ordinal forms (3.8.0+): `date_to_string: "ordinal", "US"` gives `Nov 7th, 2008`; `date_to_long_string: "ordinal"` gives `7th November 2008` (UK style).

## Checked

2026-11-04. Confirmed against the Jekyll Liquid filters data: relative_url, absolute_url, date filters and the 3.8.0 ordinal forms. Nothing removed.

Method: documentation only; no commands were run.
