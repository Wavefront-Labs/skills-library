---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.production-probes
name: production-probes
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [production-probes, probe-tests, testing-for-reliability, blackbox-exporter, synthetic-monitoring, prober]
level: practitioner
status: docs-checked
description: "Reuse known-good and known-bad test requests as production monitoring probes, per the SRE Book, and express them as blackbox_exporter HTTP modules."
sources: ["https://sre.google/sre-book/testing-reliability/", "https://github.com/prometheus/blackbox_exporter/blob/master/CONFIGURATION.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Production probes

## What the SRE Book says (Testing for Reliability, "Production Probes")
- Known good requests should work and known bad requests should error. Implementing both as an integration test is generally a good idea, and the same bank of requests can be replayed as a release test.
- Split the known good requests into those that can be replayed against production and those that cannot. That gives three sets: known bad requests, known good replayable against production, and known good not replayable. Each set can serve as integration and release tests, and most can also be monitoring probes.
- The probe is not redundant with the release test. The release test probably wrapped the integrated server with a frontend and a fake backend; the probe wraps the release binary with a load-balancing frontend and a separate scalable persistent backend; and frontends and backends probably have independent release cycles. So the production probe is a configuration not previously tested.
- Probes should never fail. If one does, either the frontend API (from the load balancer) or the backend API (to the persistent store) is not equivalent between production and release environments, and unless you know why, the site is likely broken.
- The production updater that gradually replaces the application also gradually replaces the probes, so all four combinations of old or new probe against old or new application are generated continuously. The updater can detect a failing combination and roll back to the last known good state.
- If probes are inspected as part of the readiness check, a bad update fails safely: no user traffic is routed to the new version and the update stays paused until engineers diagnose it and roll it back cleanly.
- Feedback is more useful the earlier it reaches engineers, and automating the test lets warnings scale.
- Monitoring should know all release versions on both sides of a service interface between two peers, and only needs to run the new combinations when either team cuts a release. Rollout automation should ideally block the production rollout until a problematic combination is no longer possible.

## Expressing a probe in blackbox_exporter
The blackbox_exporter configuration page describes a module with `prober` (http, tcp, dns, icmp, grpc, unix), an optional `timeout`, and an `http` section. In the `http` section, `method` defaults to `GET`, `valid_status_codes` defaults to 2xx, and `body` sets the request body. There are also `fail_if_body_matches_regexp` and `fail_if_body_not_matches_regexp`, and an `authorization` block that accepts `credentials_file`.
```yaml
modules:
  api_known_good:
    prober: http
    timeout: 5s
    http:
      method: GET
      valid_status_codes: [200]
      fail_if_body_not_matches_regexp: ['"status":\s*"ok"']
  api_known_bad:
    prober: http
    http:
      method: POST
      body: '{"amount": -5}'
      valid_status_codes: [400]
```
The exporter is a testing tool: it makes a single connection attempt, with no retry. If a hostname resolves to several addresses it tests one, so a host with both AAAA and A records needs two separate tests.

## Checked
- 2026-11-08: the probe-set split, the reasons the probe is a new configuration, the four old/new combinations, readiness-check behaviour and the fake-backend versioning advice were confirmed on the SRE Book Testing for Reliability page. The module field names, defaults, and single-attempt behaviour were confirmed on the blackbox_exporter CONFIGURATION page.
- Removed: custom journey-prober metric names, the PromQL alert threshold, multi-location alerting advice, the example status codes as recommendations, and pollution and cleanup advice, none of which the pages state. The YAML above is an illustration of the documented fields, not a recommended configuration.
Method: docs-only read of cited pages, 2026-11-08
