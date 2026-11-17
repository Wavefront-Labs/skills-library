---
id: computing-software.software-engineering.debugging.production-debugging-and-observability
name: production-debugging-and-observability
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, observability, production-incident, distributed-tracing, structured-logging, metrics, opentelemetry, correlation-id, feature-flags, incident-response, postmortem, alerting, slo]
level: advanced
status: draft
description: "Debug a live production incident with correlation IDs, distributed traces, and metrics when you cannot reproduce locally or attach a debugger."
sources: ["Google SRE book - ch. Monitoring Distributed Systems, ch. Effective Troubleshooting", "OpenTelemetry docs - traces and spans", "personal on-call incident experience"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Production debugging — find the cause when you can't attach a debugger

**Goal:** go from "users report errors" to a confirmed root cause using the telemetry
already running, without redeploying instrumentation mid-incident.

## 1. Narrow with metrics before reading any logs
Dashboards answer "when, how much, where" faster than logs:
- Error rate by endpoint/service — did it spike at a specific time (deploy, config
  change, traffic pattern) or ramp gradually (resource exhaustion, leak)?
- Correlate against a deploy timeline — most incidents are caused by the last change;
  check `git log`/deploy events against the spike timestamp before theorizing further.
- Latency percentiles (p50/p99), not averages — a p50 that looks fine can hide a p99
  that's timing out downstream callers; averages hide bimodal distributions entirely.

## 2. Trace one request end-to-end, not one service's logs
In a distributed system, a single request's logs are scattered across every service
it touched. A **correlation/trace ID** generated at the edge and propagated through
every hop (HTTP header, message queue metadata, log field) is what makes this
searchable at all — if the system doesn't propagate one, that's the first gap to fix,
not the incident to solve manually. With OpenTelemetry/Jaeger/Honeycomb, pull the
full trace for one failing request: it shows exactly which hop added the latency or
returned the error, as spans with parent/child relationships.

## 3. Structured logs, queried, not grepped
`grep` across plaintext logs doesn't scale past one host. Structured (JSON) logs
shipped to a queryable store (Loki, Elasticsearch, Datadog, CloudWatch Logs Insights)
let you filter by the correlation ID, user ID, or error code directly:
```
fields @timestamp, @message | filter correlation_id = "abc-123" | sort @timestamp asc
```
If logs for the incident window were sampled or rate-limited, say so explicitly —
missing log lines during a high-error-rate incident is common and skews
"it only happened 3 times" conclusions.

## 4. Narrow the blast radius with flags, not deploys
A feature flag / config toggle that can disable the suspect code path *without a
deploy* turns "wait 20 minutes for CI" into "confirm or rule out in 30 seconds." If
the suspected cause is a recent flag rollout rather than a deploy, check the flag's
rollout percentage/cohort against who's reporting the issue before touching code.

## 5. When you genuinely can't reproduce
- Check if it's host-specific (one bad node, one AZ) before assuming it's code —
  `kubectl get pods -o wide` / infra dashboards by host first.
- Check if it's data-specific (one tenant, one input shape) by filtering the error
  rate by customer/payload type.
- Add a canary/synthetic request that exercises the exact failing path on a schedule,
  rather than waiting for the next real occurrence to gather more data.
- If nothing else works, ship additional structured logging around the suspected
  function behind a flag, deploy to one instance/canary, and wait for the next
  occurrence — this is slower but still faster than guessing.

## 6. Postmortem discipline
Blameless, timeline-based, and ends with concrete follow-ups (not "be more careful"):
what detected it, how long to detect (can a better alert shrink this?), how long to
mitigate, root cause, and the specific monitoring/test gap that let it ship.

## Gotchas
- A dashboard default time range hides a spike that started just before the window —
  always widen before concluding "nothing changed."
- Clock skew across hosts without NTP makes cross-service log ordering wrong by
  seconds — don't trust log timestamp ordering across services without checking.
- Caching (CDN, app-level) means a fix deployed doesn't show improved metrics until
  the cache layer also clears — rule this out before concluding a fix didn't work.

## Verify
- [ ] The incident timeline is anchored to a specific metric change, not a guess.
- [ ] A single request's full trace (not just one service's log) was examined for at
      least one failing case.
- [ ] If a deploy/flag change correlates in time, it was confirmed or ruled out by
      toggling it, not assumed.
- [ ] A postmortem names the monitoring or test gap, with a tracked follow-up.

Related: computing-software.software-engineering.debugging.systematic-debugging,
computing-software.software-engineering.software-architecture.module-boundaries-and-decomposition
