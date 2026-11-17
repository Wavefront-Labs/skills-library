---
id: computing-software.software-engineering.refactoring.dark-launching-and-shadow-traffic
name: dark-launching-and-shadow-traffic
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, dark-launch, shadow-traffic, traffic-mirroring, parallel-run, scientist]
level: advanced
status: draft
description: "Verify a rewritten component with dark launches and shadow traffic: run old and new side by side on real inputs, compare results, and only serve the old one until they match."
sources: ["https://github.com/github/scientist", "https://github.blog/engineering/move-fast/", "https://istio.io/latest/docs/tasks/traffic-management/mirroring/", "https://martinfowler.com/bliki/DarkLaunching.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dark launching and shadow traffic comparison

When refactoring or replacing critical code, tests can't cover every real input. Run the new code
on production traffic **without users seeing its results**, compare, fix differences, then switch.

## In-process: Scientist pattern (GitHub)
```ruby
science "permissions-check" do |e|
  e.use { legacy_allowed?(user, repo) }      # control: result returned to user
  e.try { new_allowed?(user, repo) }          # candidate: run, compared, result discarded
  e.compare { |a, b| a == b }
  e.ignore { |control, candidate| repo.archived? }   # known, accepted differences
end
```
Ports: `scientist` (Ruby), Scientist.NET, `laboratory` (Python), `scientist4j`. Publishes timing and mismatch metrics plus samples of mismatches with inputs.
- Sample (e.g. 1% of calls) to limit cost; run the candidate with a timeout so it can't slow
  requests; exceptions in the candidate are recorded, not raised.
- **Candidate must have no side effects** (no writes, emails, charges), or write to a shadow store.

## Infrastructure: traffic mirroring
Envoy/Istio `mirror` (fire-and-forget copy of requests to the new service, responses discarded),
NGINX `mirror` directive, AWS VPC traffic mirroring, GoReplay for recorded replays.
```yaml
http:
- route: [{destination: {host: orders-v1}}]
  mirror: {host: orders-v2}
  mirrorPercentage: {value: 10.0}
```
Comparison happens offline: log both responses keyed by request id and diff them (ignore timestamps,
ordering of sets, generated ids).

## Rollout
Mismatch rate trends to zero (or to an explained set) -> switch reads to the new path for a small %
via a toggle -> keep comparing in reverse briefly -> retire old code.

## Pitfalls
Mirrored writes doubling side effects; comparing non-deterministic outputs; candidate load hurting
shared dependencies (DB); PII in mismatch logs.
