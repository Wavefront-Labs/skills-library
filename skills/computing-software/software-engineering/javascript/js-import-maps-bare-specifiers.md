---
id: computing-software.software-engineering.javascript.js-import-maps-bare-specifiers
name: js-import-maps-bare-specifiers
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, import-maps, js-modules]
level: advanced
status: docs-checked
description: "Import map structure from the HTML Standard: imports, scopes and integrity keys, trailing-slash prefix rules, rule priority, and how multiple maps merge."
sources:
  - https://html.spec.whatwg.org/multipage/webappapis.html#import-maps
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Import maps and bare specifiers

- An import map is JSON that must be a JSON object with at most the three keys `imports`, `scopes` and `integrity`. Example: `{"imports":{"lodash":"/vendor/lodash.js","lib/":"/vendor/lib/"}}`.
- `imports` is a module specifier map. `scopes` maps URL prefixes to their own specifier maps, so rules apply by the path of the referring script. `integrity` maps module URLs to integrity metadata strings.
- Prefix mappings: if a key ends with `/`, the corresponding value must also end with `/`. The spec normalises an entry whose key ends with `/` but whose address does not to null (the rule is ignored; user agents may warn).
- Rule priority: keys and scopes are sorted in descending order so `foo/bar/` is tried before `foo/`, which gives the longer prefix higher priority.
- Integrity map keys are treated as URLs, not module specifiers, and keys that are bare relative names such as `foo` are rejected.
- A Document can process multiple import maps, before or after any modules were imported (for example through `import()` or module script elements). Merging means a new map cannot change resolution for modules already resolved or already defined by earlier maps: conflicting rules (same scope and specifier) keep the existing rule, and rules affecting an already-resolved module are dropped from the new map.
- Prefer self-hosted pinned URLs over unpinned CDN `@latest` addresses (practice, not a spec statement).

Self-check: after loading the page, check the console for specifier resolution errors for every bare import you rely on.

## Checked

Checked 2026-11-08 against the HTML Standard webappapis page: import map authoring requirements, processing model (imports, scopes, integrity), sorting and normalising rules, and the merge examples. Removed: the claim that the map must precede module scripts, the exact error message text, the Node resolution statement, and browser support notes for integrity (not on the cited page or not located).
Method: docs-only read of cited pages, 2026-11-08
