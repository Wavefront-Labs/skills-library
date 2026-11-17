---
id: computing-software.web-development.jekyll.permalink-placeholders
name: permalink-placeholders
category: computing-software
field: web-development
product: jekyll
tags: [permalink-placeholders, date-placeholders, slug-placeholder, slugified-categories, week-placeholders]
level: advanced
status: docs-checked
description: "Pick the right Jekyll permalink placeholder for posts: date parts, week and weekday parts, title vs slug, categories vs slugified_categories, output_ext."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_data/permalinks.yml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Post placeholders. Year, month and day parts come from the filename and can be overridden by the `date` front matter.

- `:year` four digits; `:short_year` no century (00..99).
- `:month` (01..12); `:i_month` no leading zeros; `:short_month` e.g. "Jan"; `:long_month` e.g. "January" (4.0).
- `:day` (01..31); `:i_day` no leading zeros; `:y_day` ordinal day of year (001..366).
- `:w_year` week year, may differ from the month year for up to three days at the start of January and end of December (4.0).
- `:week` (01..53), starting with the first week having a majority of its days in January (4.0).
- `:w_day` (1..7, Monday first), `:short_day` e.g. "Sun", `:long_day` e.g. "Sunday" (all 4.0).
- `:hour` (00..23), `:minute`, `:second`: from the `date` front matter.
- `:title`: title from the filename, case preserved; overridden by the `slug` front matter.
- `:slug`: slugified filename title, anything but numbers and letters becomes a hyphen; also overridden by `slug`.
- `:categories`: multiple categories form a hierarchy (`/category1/category2`); double slashes are removed, so none is fine.
- `:slugified_categories` (4.1): lowercased, non-alphanumerics become hyphens (`"Work 2 Progress"` becomes `"work-2-progress"`).
- `:output_ext`: output extension; included by default and usually unnecessary.

Example:

```yaml
permalink: /:categories/:year/:month/:day/:title:output_ext
```

## Checked

2026-11-04. Every placeholder, range, example value and version note (4.0, 4.1) confirmed against the Jekyll permalinks data file. Reworded the filename/date-override sentence to cover only the placeholders the page says can be overridden.

Method: documentation only; no commands were run.
