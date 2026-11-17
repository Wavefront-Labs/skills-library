---
id: computing-software.web-development.ghost.ghost-content-api-nql-filtering
name: ghost-content-api-nql-filtering
category: computing-software
field: web-development
product: ghost
tags: [ghost, nql, filter, content-api, query-language, operators]
level: advanced
status: docs-checked
description: "Write Ghost NQL filters: property:operator value syntax, comparison and string operators, in-groups, and, or, grouping and relative dates."
sources:
  - https://github.com/TryGhost/docs/blob/main/content-api/filtering.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: filter Ghost API results with NQL.

Form: `property:operator value`. Properties are lowercase paths such as `tag`, `authors.slug` or `posts.count`; they must start with a letter and cannot contain whitespace. A bare colon is roughly equals.

Values: `null`, `true`, `false`, integers, literals (no leading `-`, none of the symbols `'"+,()><=[]` unless escaped, no whitespace), quoted strings (single quotes, escape inner quotes, whitespace allowed), and relative dates like `now-30d` (intervals d, w, M, y, h, m, s).

Operators: `-` not, `>`, `>=`, `<`, `<=`, `~` contains, `~^` starts with, `~$` ends with, and `[a,b]` in-groups (negate with `-`).
Combine with `+` for AND and `,` for OR; wrap sub-expressions in parentheses to override precedence.

Examples:
- `featured:true`
- `tag:getting-started`
- `tag:[news,updates]+featured:true`
- `published_at:>now-30d`
- `tag:fiction+tag:-fables`

Filter strings must be URL encoded. The filtering page says NQL does not yet support SQL-style `like` matching.

Verify: browse with `limit=1` and the filter, then confirm every returned record satisfies it.

## Checked

2026-11-04. Confirmed: syntax, property rules, value types, relative dates and intervals, operators, combinations, URL encoding (filtering page). Removed: the invented `tag:-hash-de` example and the "only the ~ family" wording.

Method: documentation only; no commands were run.
