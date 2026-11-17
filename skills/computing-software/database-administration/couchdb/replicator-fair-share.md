---
id: computing-software.database-administration.couchdb.replicator-fair-share
name: replicator-fair-share
category: computing-software
field: database-administration
product: couchdb
tags: [replication, fair-share, replicator-shares, usage-coeff, priority-coeff]
level: sme
status: docs-checked
description: "Allocate CouchDB replication scheduling shares per replicator database with [replicator.shares], plus usage_coeff and priority_coeff decay."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/config/replicator.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Added in 3.2.0. Higher share values give jobs from that replicator database a higher chance of running. Default 100, minimum 1, maximum 1000. A share can be configured before the database exists.

```ini
[replicator.shares]
_replicator = 50
foo/_replicator = 25
bar/_replicator = 25
```

The key is the replicator database name. The default is `_replicator`; additional ones must have names ending with `/_replicator` to be recognised.

Decay coefficients in `[replicator]`:

- `usage_coeff` (default example 0.5, range 0.0 to 1.0): decays historic fair share usage each cycle. Lower forgets faster.
- `priority_coeff` (0.98): decays job priorities so they drift toward the front of the run queue. Too small a value (0.1) leaves many jobs at priority 0, defeating the algorithm. 0.98 is chosen so a job that ran one cycle then waited 7 hours still has priority above 0, close to the 8 hour default maximum error backoff.

## Checked

2026-11-04. Confirmed against the CouchDB config/replicator page (replicator.shares, usage_coeff, priority_coeff): version 3.2.0, share default 100 and range 1 to 1000, naming rule for extra replicator databases, coefficient meanings, the 0.98 and 7 hour explanation. Nothing removed.

Method: documentation only; no commands were run.
