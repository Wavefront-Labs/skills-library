---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-security-and-admin-endpoints
name: victoriametrics-security-and-admin-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [security, tls, basic-auth, auth-keys, admin-endpoints, pprof]
level: practitioner
status: docs-checked
description: "Secure VictoriaMetrics with basic auth, TLS and auth keys on delete, snapshot, flush, merge, reload and profiling endpoints."
sources: ["https://docs.victoriametrics.com/victoriametrics/single-server-victoriametrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics security and admin endpoints

Single-node VictoriaMetrics exposes several administrative endpoints that should be protected by flags.

- HTTP basic auth: `-httpAuth.username` and `-httpAuth.password`.
- TLS: `-tls`, `-tlsCertFile`, `-tlsKeyFile`. Enterprise mTLS: `-mtls` and `-mtlsCAFile`.
- Response headers: `-http.header.hsts`, `-http.header.csp`, `-http.header.frameOptions`.
- Per-endpoint auth keys:
  - `-deleteAuthKey` for series deletion
  - `-snapshotAuthKey` for snapshot endpoints
  - `-forceFlushAuthKey` and `-forceMergeAuthKey` for `/internal/force_flush` and `/internal/force_merge`
  - `-search.resetCacheAuthKey` for cache reset
  - `-reloadAuthKey` for `/-/reload`
  - `-configAuthKey`, `-flagsAuthKey`, `-pprofAuthKey`, `-metricNamesStatsResetAuthKey`
- Query tracing: clients request it with `trace=1`; operators can block it with `-denyQueryTracing`.

Self-monitoring: set `-selfScrapeInterval` above 0 (for example `10s`) to scrape its own `/metrics`; `-metrics.exposeMetadata` adds `TYPE` and `HELP` lines.

Put vmauth in front of public endpoints, restrict `-search.max*` flags to protect against expensive queries, and in clusters use the multitenant endpoints only from trusted sources. Because delete and snapshot calls are powerful, never expose their endpoints without both network controls and the matching auth key.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
