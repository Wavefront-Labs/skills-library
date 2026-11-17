---
id: computing-software.cloud-infrastructure-engineering.fluentd.match-patterns-and-order
name: match-patterns-and-order
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, match, filter, tag-patterns, wildcards, routing]
level: practitioner
status: docs-checked
description: "Fluentd tag pattern syntax (*, **, {a,b}, regex, embedded Ruby) and why match and filter order in the file decides which events are processed."
sources:
  - https://docs.fluentd.org/configuration/config-file
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd match patterns and order
Patterns usable in `<match>` and `<filter>`:

- `*` matches one tag part: `a.*` matches `a.b`, not `a` or `a.b.c`.
- `**` matches zero or more parts: `a.**` matches `a`, `a.b`, `a.b.c`.
- `{X,Y,Z}` matches any listed pattern; combinable, e.g. `a.{b,c}.*`, `a.{b,c.**}`.
- `/regex/` for complex patterns, e.g. `/(?!a\.).*/` (supported since v1.11.2 per the page).
- `#{...}` evaluates Ruby (since v1.4.0), e.g. `<match "app.#{ENV['FLUENTD_TAG']}">`.
- Several space-separated patterns in one tag match any of them: `<match a.** b.*>`.

Order matters: Fluentd matches in file order. A `<match **>` placed first swallows everything, so `myapp.access` below it never matches. Put narrow patterns first and the catch-all last. Two identical patterns: the second never matches; to send to several outputs use `out_copy`.

Common pitfall: a `<filter>` placed after the `<match>` for the same tag never runs, because events already left through the match.

## Checked

2026-11-04. Confirmed against the Fluentd Config File page (docs.fluentd.org/configuration/config-file), Tag pattern and Note on Match Order sections: *, **, {X,Y,Z}, regex with v1.11.2, #{...} with v1.4.0, multiple patterns, match order and out_copy. Nothing removed.

Method: documentation only; no commands were run.
