---
id: computing-software.qa-testing-engineering.jmeter-k6.jmeter-taurus-ci
name: jmeter-taurus-ci
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [jmeter, taurus, bzt, ci-integration, performance-ci, pass-fail-criteria, jmeter-reporting]
level: practitioner
status: docs-checked
description: "Run JMeter (and k6, Locust, Gatling) from CI with Taurus: YAML configs, load overrides, pass/fail criteria that fail the build, and JUnit-style reporting."
sources:
  - https://gettaurus.org/docs/Installation/
  - https://gettaurus.org/docs/PassFail/
  - https://gettaurus.org/docs/JMeter/
  - https://gettaurus.org/docs/CommandLine/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running JMeter from CI with Taurus

**Goal:** declarative performance tests in CI with automatic pass/fail.

## Install and run
```bash
pip install bzt          # or: docker run -it --rm -v <dir>:/bzt-configs blazemeter/taurus perf.yml
bzt perf.yml -o modules.jmeter.properties.host=staging.example.com
```
`-o` overrides a config setting from the command line. If JMeter is not installed at the configured path, Taurus attempts to install the latest JMeter and plugins automatically (default `~/.bzt/jmeter-taurus/<version>/bin/jmeter`; internet access needed).

## perf.yml
```yaml
execution:
- executor: jmeter
  scenario: checkout
  concurrency: 100
  ramp-up: 2m
  hold-for: 10m
  # throughput: 50   (optional RPS limit; needs ramp-up and/or hold-for)

scenarios:
  checkout:
    script: tests/perf/checkout.jmx      # existing JMX; or define requests inline

reporting:
- module: final-stats
  summary: true
  percentiles: true
  dump-xml: results/stats.xml
- module: junit-xml
  filename: results/junit.xml
  data-source: pass-fail
- module: passfail
  criteria:
  - avg-rt of Checkout>800ms for 30s, stop as failed
  - p95 of Checkout>1500ms, continue as failed
  - fail>2% for 1m, stop as failed
```
When the JMX has several thread groups and the YAML sets `concurrency`, the YAML value is divided between them in proportion to their own concurrency values (for example 30 split 1:2 gives 10 and 20).

## CI
Taurus exit codes: 0 no problems, 1 generic error, 2 manual shutdown, 3 shut down automatically (for example by Pass/Fail criteria). Check which code your pipeline sees for a `continue as failed` criterion in a trial run; publish `junit.xml` and keep the JTL/report as artifacts.

## Gotchas
- Taurus rescales the JMX's thread-group concurrency to the YAML value; be explicit.
- With `for`, each value in the timeframe must trigger the condition (`avg-rt>1s for 5s` needs five consecutive seconds above 1 s), so brief spikes pass; `within` and `over` aggregate the window instead.
- Criteria format: `subject of label condition threshold`, no spaces around the operator; action is `stop` (default) or `continue`, status `failed` (default) or `non-failed`.

## Verify
Lower a criterion threshold below current performance: Taurus stops the test and junit.xml shows the failed criterion.

## Checked
Checked against the Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual, master as of 2026-10-01; latest release 5.6.3) and the Taurus docs sources (Blazemeter/taurus, site/dat/docs, last commit 2026-10-23). Confirmed: pip and docker install, `-o` override and `modules.jmeter.properties` path, JMeter auto-install, execution ramp-up/hold-for/throughput, concurrency splitting across thread groups, passfail criteria grammar and timeframe logic, final-stats and junit-xml reporter options, exit codes. Not confirmed from the docs: whether a `continue as failed` criterion changes the exit code.

Method: documentation only; no commands were run.
