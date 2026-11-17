---
id: computing-software.devops-ci-cd.argocd-image-updater.calver-ordering-and-trailing-segments
name: calver-ordering-and-trailing-segments
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, calver, calver-ordering, micro-segment, optional-segments, no-separators, tag-prefix]
level: advanced
status: docs-checked
description: "Understand how calver orders tags: segment order, the date as one unit, optional trailing MINOR and MICRO, tags without separators, and optional v prefix matching."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-strategies.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# calver ordering and trailing segments

Segments compare in the order the layout writes them; the date counts as a single segment placed where the layout first mentions it, compared by significance. So with `MAJOR.YY.0M` the major segment outranks the date: `1.26.03 < 1.26.11 < 2.25.01`. With `YY.0M.MAJOR`: `25.01.2 < 26.03.1 < 26.11.1`.

Rules:

- the date's fields must be adjacent; `YY.MINOR.0M` is rejected
- `MAJOR` always outranks `MINOR`, which outranks `MICRO`; reversing them is turned away as a typo
- a missing numeric segment counts as `0`, so `v26.4 < v26.4.1` under `vYY.MINOR.MICRO`

Optional trailing segments: `MINOR`, `MICRO` and `MODIFIER` may be absent from a tag if the layout writes them at the very end, each after a literal separator. This lets dated tags and rebuilds coexist:

```yaml
imageName: "some/image:vYYYY-0M-0D-MICRO"
# v2026-01-30 < v2026-01-30-2 < v2026-01-30-10 < v2026-02-01
```

Without `MICRO` in the layout, `v2026-01-30-2` is never considered. Micro is numeric, so `-1` and `-01` are the same version; if both exist the name sorting last is picked for stability. Same for short tokens: under `MM`, `2026-1-30` and `2026-01-30` are equal and the updater may rewrite one to the other. Use padded tokens or `ignoreTags` to avoid that.

No separators: only fixed-width tokens may sit adjacent. `YYYY0M0D` matches `20260130`; `YYYYMMDD` is rejected. `0Y0M0D` matches `260130` but not year 2106; use `YYYY0M0D` to outlive 2099.

Prefixes: a layout starting with a token accepts an optional `v` or `V`. A literal prefix in the layout is mandatory and case-sensitive.

## Checked

2026-11-04. Confirmed against update-strategies.md (How tags are ordered, Optional trailing segments, Tags without separators, Prefixes; the ordering examples match the page).

Method: documentation only; no commands were run.
