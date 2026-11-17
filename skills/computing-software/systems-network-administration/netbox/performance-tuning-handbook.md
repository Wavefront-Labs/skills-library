---
id: computing-software.systems-network-administration.netbox.performance-tuning-handbook
name: performance-tuning-handbook
category: computing-software
field: systems-network-administration
product: netbox
tags: [performance, wsgi-workers, max-page-size]
level: advanced
status: docs-checked
description: "Apply the handbook's WSGI and configuration recommendations."
sources: ["https://netboxlabs.com/docs/netbox/best-practices/performance-handbook/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Performance handbook

Goal: tune the WSGI server and configuration.

NetBox is a WSGI application behind nginx or Apache; the backend (typically Gunicorn or uWSGI) runs worker processes that take relayed requests.

**WSGI recommendations**

- **Workers:** double the CPU cores plus one (`2 * CPUs + 1`).
- **Worker lifetime:** set a maximum request count before respawn, to guard against memory leaks.
- **Request timeout:** limit time per request; the docs suggest 120 seconds.
- **Unix socket:** when the frontend and WSGI server share a machine, binding by Unix socket instead of TCP may give slight gains.

Edit these in `gunicorn.py` (the copy made during install).

**NetBox settings**

- `MAX_PAGE_SIZE`: maximum results per page a client may request; default 1,000. Consider lowering it.
- `GRAPHQL_MAX_ALIASES`: default 10 aliases per query; consider reducing it.
- `GRAPHQL_MAX_QUERY_DEPTH`: set to cap how deeply a GraphQL query may nest.

Deeply nested GraphQL queries consume server resources and increase response times.

**API reads.** Use `fields`, `omit` and `brief` to cut query load.

**Checklist**

1. Set workers by CPU count.
2. Add max requests and timeout.
3. Lower page size and GraphQL limits.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Performance handbook: 2x CPUs + 1 workers, max-requests guidance, 120 second timeout suggestion, Unix socket binding, MAX_PAGE_SIZE default 1000, GraphQL alias and depth limits, brief/fields/omit. Removed: Nothing.

Method: documentation only; no commands were run.
