---
id: computing-software.devops-ci-cd.forgejo.robots-txt-and-search-engines
name: robots-txt-and-search-engines
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [robots-txt, search-engine-indexing, archive-crawling, custom-public-dir]
level: intro
status: docs-checked
description: "Stop search engines indexing a Forgejo instance or crawling archive downloads with a custom robots.txt."
sources:
  - https://forgejo.org/docs/latest/admin/advanced/search-engines/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default search engines may index a Forgejo instance, and Forgejo serves an empty 404 for `robots.txt`. To serve your own, create `public/robots.txt` in the Custom File Root Path shown on the `/admin/config` page. To block all indexing use:

```
User-agent: *
Disallow: /
```

If Forgejo lives in a subdirectory, create or edit the robots.txt at the top level of the site and disallow that path instead, for example `Disallow: /forgejo/`.

Crawling archives wastes disk. Archive files are generated dynamically and kept around when crawlers request them, which can add up to a lot of storage. Prevent this by adding `Disallow: /*/*/archive/` to the file. The page points to the Codeberg robots.txt for a more complete example, and to Moz for syntax help.

## Checked

2026-11-04. Confirmed against the Forgejo Search Engines Indexation page: default indexing, the empty 404 default, the public/robots.txt path under the Custom File Root Path, both example blocks, the subdirectory advice and the archive rule. Removed: the verify-by-requesting step and the remark about sharing one User-agent block, which the page does not state.

Method: documentation only; no commands were run.
