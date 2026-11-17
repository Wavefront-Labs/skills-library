---
id: computing-software.search-and-information-retrieval.apache-solr.dismax-parameters
name: dismax-parameters
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [dismax, qf-mm, minimum-should-match, q-alt, disjunction-max]
level: practitioner
status: docs-checked
description: "Tune the Solr DisMax query parser for end-user input: qf field boosts, mm minimum-should-match syntax, q.alt, pf phrase boost, tie, and bq, bf boost parameters."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/dismax-query-parser.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dismax-parameters

DisMax (`defType=dismax`) accepts almost any raw user input without erroring. `+` and `-` mark required and prohibited terms, balanced quotes make phrases (an odd number of quotes is treated as none). `q` does not support wildcards.

Parameters:
- `q.alt`: query used when `q` is missing or blank; pair with `rows=0` for collection-wide facet counts.
- `qf`: fields with boosts, for example `fieldOne^2.3 fieldTwo fieldThree^0.4`.
- `mm`: how many optional clauses must match. Forms: positive integer (`3`), negative integer (`-2`, all optional minus 2), percentage (`75%`, rounded down), negative percentage (`-25%`), conditional (`3<90%`: all required up to 3 clauses, above that 90%).
- Boosts via `pf` (phrase fields), `bq` (boost query) and `bf` (additive boost functions).
- `tie`: weight of non-maximum matching fields in the max-disjunction score.

All can be defaults in `solrconfig.xml` or overridden per request. DisMax also accepts the common, highlighting and facet parameters.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide DisMax Query Parser page: raw user input, `+`/`-`, balanced quotes and the odd-quote rule, no wildcard support in `q`, `q.alt` with `rows=0`, the `mm` forms (percentage rounded down, negative percentage, `3<90%` conditional), `pf`, `ps`, `tie`, `bq`, `bf`, and defaults in `solrconfig.xml`. Removed the claim that other special characters are escaped, which the page does not state.

Method: documentation only; no commands were run.
