---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.remote-read-configuration
name: remote-read-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, remote-read, remote-read-config, read-recent, required-matchers, filter-external-labels, streamed-xor-chunks]
level: practitioner
status: docs-checked
description: "Configure Prometheus remote_read (read_recent, required_matchers, filter_external_labels, chunked streaming) to query long-term storage without overloading it."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_read", "https://prometheus.io/docs/prometheus/latest/querying/remote_read_api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# remote_read configuration

remote_read makes PromQL on this Prometheus also fetch raw samples from another store and merge them.
It is a federation-of-raw-data mechanism; most teams query the long-term store (Thanos Query, Mimir) directly
from Grafana instead. Use remote_read when local rules/alerts must see older data or a migration source.

```yaml
remote_read:
  - url: http://old-prometheus:9090/api/v1/read
    read_recent: false              # default false: skip remote for ranges local TSDB fully covers
    required_matchers:              # only queries carrying these equality matchers go remote
      source: archive
    filter_external_labels: true    # default true: add this server's external labels as matchers
    remote_timeout: 1m              # default 1m
    headers: {X-Scope-OrgID: team-a}
```

## Key behaviours
- **read_recent: false** - per the docs, reads are not made for time ranges the local storage should have
  complete data for. Set `true` only when local data is incomplete (e.g. after a migration).
- **required_matchers** - opt-in per query: `rate(http_requests_total{source="archive"}[5m])` goes remote,
  everything else stays local. This prevents every dashboard query fanning out.
- **filter_external_labels** - if the remote store holds data from many Prometheus servers, this narrows to
  this server's series. Set false to read everything (and watch duplicates).
- The Remote Read API has two response forms, raw samples and streamed chunks (XOR-encoded, millisecond
  resolution). The remote read API is documented as not part of the stable API.
- `external_labels` matter on both sides: the querying server sends its external labels as equality matchers,
  so mismatched labels can return no results.

## Serving remote read
Every Prometheus serves `/api/v1/read` (snappy-compressed). Limit it with `--storage.remote.read-concurrent-limit`
(default 10), `--storage.remote.read-sample-limit` (default 5e7, ignored for streamed responses) and
`--storage.remote.read-max-bytes-in-frame` (default 1MB).

## Gotchas
- Remote read pulls raw samples over the network then evaluates locally; long-range queries are expensive.
- Thanos sidecar uses remote read against its Prometheus; tight read limits on that Prometheus break Thanos.

## Checked
2026-10-28. Confirmed on the Prometheus configuration page (`remote_read` fields, defaults for `read_recent`,
`filter_external_labels`, `remote_timeout`, `required_matchers`, `headers`), the Remote Read API page (streamed chunks,
external_labels behaviour, stability note) and the command-line page (read limits and defaults). Removed: the
`STREAMED_XOR_CHUNKS` / 2.13 claim, two metric names not found in the Prometheus source, and the partial-data-on-outage claim.
Method: documentation only; no commands were run.

## Verify
- [ ] A query with the required matcher returns data older than local retention.
- [ ] Queries without it don't show traffic on the remote (check the remote's own request metrics).
- [ ] Remote read latency is acceptable on the remote's side.
