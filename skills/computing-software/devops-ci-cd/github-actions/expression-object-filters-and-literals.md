---
id: computing-software.devops-ci-cd.github-actions.expression-object-filters-and-literals
name: expression-object-filters-and-literals
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, object-filter, wildcard-filter, expression-literals, star-filter, array-filter, contains-array, labels-filter, commits-filter, expression-syntax, property-dereference, index-syntax, null-literal, hexadecimal-literal, expressions, contexts]
level: practitioner
status: verified
description: "Use the * object filter to pull one property from every array element (labels, commits) plus literal and index rules, so 'any label named X' conditions work."
sources: ["https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/evaluate-expressions-in-workflows-and-actions#object-filters", "https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/evaluate-expressions-in-workflows-and-actions#literals"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expression object filters and literals

**Goal:** write `if:` conditions over arrays without a script step.

## 1. The `*` filter
`array.*.prop` returns an array of `prop` from every element; `object.*` returns the values.
```yaml
# any commit message in the push mentions "release"
if: contains(join(github.event.commits.*.message, ' '), 'release')

# PR has label "deploy" (labels is an array of objects)
if: contains(github.event.pull_request.labels.*.name, 'deploy')

# label names as a JSON array
run: echo '${{ toJSON(github.event.pull_request.labels.*.name) }}'
```
`contains(array, item)` is true when `item` is an element; `contains(string, substr)` is a substring
test. Both ignore case and cast values to strings. `join(array, sep)` turns the filtered array into a
string for regex-free checks.

Filters are read-only projections — you cannot filter *by* a condition (no `where`). For
"label starting with `env:`", join and use `contains`/`startsWith` on the string, or move to
`actions/github-script`.

## 2. Property access
- `github.event['pull_request']['title']` — the `[ ]` index operator also works for keys that are not
  plain identifiers (`github.event.inputs['dry-run']`).
- Dereferencing a nonexistent property evaluates to an empty string (GitHub contexts reference).
- Index into arrays with `github.event.commits[0].id`.

## 3. Literals and types
| literal | note |
|---|---|
| `null` | coerces to 0, so `'' == null` is true |
| `true`/`false` | coerce to 1/0; the string `'true'` is NaN, so `'true' == true` is **false** |
| `42`, `-9.2`, `0xff`, `-2.99e-2` | any JSON number format (plus hex); `'1' == 1` true |
| `'single quoted'` | strings must use **single** quotes; escape `'` as `''` |
Double-quoted strings are an error inside `${{ }}`. Equality is loose: when types differ both sides are
coerced to numbers (`'' == 0` is true — guard empties with `!= ''`). A NaN operand makes `<`, `>`, `<=`,
`>=` false.

## 4. Practical conditions
```yaml
# run deploy job only when PR merged with a label
if: github.event.pull_request.merged == true && contains(github.event.pull_request.labels.*.name, 'auto-deploy')

# matrix include has a boolean flag
if: matrix.experimental == true

# pick first commit author
env: { AUTHOR: "${{ github.event.commits[0].author.name }}" }
```

## 5. Gotchas
- `*` on an object (not an array) returns its property values, for example `vegetables.*.ediblePortions`.
- `contains(github.event.pull_request.labels.*.name, 'deploy')` is false on `push` (no PR
  object) — combine with `github.event_name`.
- An `if:` that starts with `!` must be wrapped in `${{ }}` or quoted (`if: "!contains(...)"`) because
  YAML treats a bare `!` as a tag.

## Verify
- [ ] Label-gated jobs run when the label is present and are skipped when it is not.
- [ ] `echo '${{ toJSON(github.event.pull_request.labels.*.name) }}'` prints the expected list.
