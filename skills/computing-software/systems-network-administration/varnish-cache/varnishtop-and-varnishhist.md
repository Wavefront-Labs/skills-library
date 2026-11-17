---
id: computing-software.systems-network-administration.varnish-cache.varnishtop-and-varnishhist
name: varnishtop-and-varnishhist
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [varnishtop, varnishhist, log-ranking, request-histogram]
level: practitioner
status: docs-checked
description: "Find hot URLs and request timing live: varnishtop rankings with -i and -I, backend load with BereqURL, and the varnishhist hit/miss histogram, plus the -q filter."
sources:
  - https://www.varnish.org/docs/users-guide/operation-statistics/
  - https://www.varnish.org/docs/users-guide/increasing-your-hitrate/
  - https://www.varnish.org/docs/reference/varnishtop/
  - https://www.varnish.org/docs/reference/varnishhist/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# varnishtop and varnishhist

Both read varnishd's shared memory logs and present continuously updated live output. Both list `-q` (a VSL query), `-d` and `-r` in their synopses; `-q` takes the same queries as varnishlog.

varnishtop shows a ranking of the most commonly occurring log entries. Filter with `-i` (include tag) and `-x` (exclude tag), or `-I` and `-X` (tag list with regex); with them it can rank documents, clients, user agents or anything else in the log.

```bash
varnishtop -i ReqURL                         # URLs clients ask for
varnishtop -i BereqURL                       # what the backend is asked for most
varnishtop -I ReqHeader:Accept-Encoding      # most popular Accept-Encoding values
varnishtop -C -I ReqHeader:User-Agent        # most common user agents
```

The hit-rate guide calls `varnishtop -i BereqURL` an essential command for seeing the top requests Varnish sends to the backend. Once you have found a URL that goes to the backend often, look at it with `varnishlog -q 'ReqURL ~ "^/foo/bar"'`. The same guide warns that `Vary: User-Agent` makes Varnish cache one copy per distinct User-Agent, so normalise the header or hit rate suffers badly; varnishtop on User-Agent shows how varied they are.

varnishhist draws a histogram of the distribution of the last N requests by processing time. N and the vertical scale are shown in the top left; the horizontal scale is logarithmic; hits are marked `|` and misses `#`. Its synopsis also has `-P` options to plot other measures (such as responsetime, size, Bereqtime) and `-g request|vxid`, which the pages do not otherwise explain. Example with a filter: `varnishhist -q 'ReqURL eq "/foo"'` (the query form is from the VSL cheatsheet, not these pages).

## Checked

Method: 2026-11-08 docs-only read of all four cited pages (the hit-rate guide by search around the varnishtop and Vary sections, not in full). Removed the earlier gloss of `-C` as "ignores case" (the reference lists it without description) and noted the varnishhist `-P` options as unexplained.
