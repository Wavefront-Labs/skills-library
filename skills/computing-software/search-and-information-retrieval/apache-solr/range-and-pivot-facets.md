---
id: computing-software.search-and-information-retrieval.apache-solr.range-and-pivot-facets
name: range-and-pivot-facets
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [range-pivot-facets, facet-range, facet-pivot, range-facets, pivot-facets, facet-interval]
level: practitioner
status: docs-checked
description: "Facet Solr numeric and date ranges with facet.range.start, end and gap, control bound inclusion and other buckets, and build pivot facets over several fields."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/faceting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# range-and-pivot-facets

Range faceting: set `facet.range` to the field, then `facet.range.start`, `facet.range.end` and `facet.range.gap`. Add `facet.range.hardend` to control the last bucket.

Bounds: by default each gap range includes its lower bound and excludes its upper one, so nothing is double counted at boundaries. Change with `facet.range.include`: `lower`, `upper`, `edge`, or `outer`/`all`. Do not combine `lower` with `upper`, and avoid `outer` and `all` if you need to avoid double counting.

`facet.range.other` adds `before`, `after`, `between`, `none` or `all` buckets. `facet.mincount` also applies to ranges. Parameters can be per-field with `f.<field>.facet.range.include`.

Pivot facets: `facet.pivot=popularity,cat` nests counts by one field inside another; `facet.pivot.mincount` filters small pivots. Stats can be computed per pivot by tagging `stats.field={!tag=piv1,piv2 min=true max=true}price`.

Interval facets use `facet.interval` with `facet.interval.set`.

## Checked

2026-11-04. Confirmed against the Faceting page: range parameters, `facet.range.include` options and double-counting warning, `facet.range.other`, per-field syntax, pivot facets with stats tags, interval facets. Removed a generic closing tip.

Method: documentation only; no commands were run.
