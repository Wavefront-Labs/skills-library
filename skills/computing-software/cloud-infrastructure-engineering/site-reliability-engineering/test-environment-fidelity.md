---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.test-environment-fidelity
name: test-environment-fidelity
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [integration-test-environment, test-environment-fidelity, testing-for-reliability, configuration-tests, production-probes]
level: practitioner
status: docs-checked
description: "Close the gap between hermetic tests and production: configuration tests, production probes, fake-backend versions and canaries, per the SRE Book testing chapter."
sources: ["https://sre.google/sre-book/testing-reliability/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test environment fidelity

**Goal:** know what your tests do and do not prove, and cover the gap between a hermetic test environment and
production with production-side tests.

## What the SRE Book says (Testing for Reliability)
- Passing tests do not prove reliability, but failing tests generally prove its absence. A test that catches the same
  problem monitoring would catch, before the push, has zero MTTR: the push is blocked and the bug never reaches
  production.
- Traditional tests (unit, integration, system: smoke, performance, regression) run offline; production tests run
  against the live service and resemble black-box monitoring.
- Integration tests can use dependency injection to replace a complex dependency, such as a stateful database, with a
  lightweight mock of precisely specified behaviour.
- Rollouts entangle tests: production is deliberately not a single checked-in version, because changes go out in stages.
  A live test may use a newer config with an older binary or the reverse. A system test that passes against a config
  version for which the configuration test fails is valid hermetically but not operationally.
- Configuration test: for each config file in version control, a separate non-hermetic test examines production to see
  how a binary is actually configured and reports discrepancies. It is simple when production exposes a query returning
  the real file content (diff it); harder when the config relies on defaults compiled into the binary, passes through a
  preprocessor like bash, or depends on a shared runtime's release schedule. The pass/fail pattern across production
  shows how far production lags engineering work.
- Stress test: finds component limits (how full a database can get before writes fail, how many queries per second
  an application server takes before failing).
- Canary: upgrade a subset, leave it in an incubation period, continue progressively if no unexpected variance, revert
  quickly if not. The chapter calls it structured user acceptance rather than a real test and says it does not always
  catch new faults. Its footnote gives a rule of thumb of 0.1 percent of traffic first, then orders of magnitude per day.
- Production probes: known good requests, known bad requests, and known good requests that cannot be replayed against
  production form three sets that can serve as integration tests, release tests and monitoring probes. The production
  probe runs a configuration not previously tested (real load balancer frontend and scalable persistent backend, versus
  a fake backend in the release test), so a probe failure means frontend or backend APIs differ between environments,
  and the site is likely broken unless the difference is already understood. The production updater replaces probes
  gradually together with the application, so all four old/new combinations are exercised, and probes can be part of the
  readiness check so a bad update stalls without receiving user traffic.
- Fake backend versions: the fake backend is often maintained by the peer team and referenced as a build dependency;
  ideally that team cuts a fake-backend release alongside its backend release and probes. Monitoring should know all
  release versions on both sides of an interface and run new combinations when either team cuts a release; rollout
  automation should block production rollout while problematic combinations remain possible.
- Test dependencies: a release test can depend on so many parts that it transitively depends on everything in the
  repository; a test on a clean copy of the production environment would in principle need a disaster recovery iteration
  per patch, so practical environments pick branch points that resolve the most uncertainty.
- Config files and break-glass: a config changed more than once per application release dominates reliability unless
  its test and monitoring coverage exceeds the application's. A break-glass push should be noisy (for example, file a
  bug) and should leave the tests running, back-annotating the push with broken tests afterwards.

## Verify
- [ ] Every config file in version control has a test comparing it with what production is actually running.
- [ ] Probes for known good and known bad requests run in production as well as in release tests.
- [ ] The list of ways the test environment differs from production exists, and canary or probes cover each.

## Checked

Checked 2026-11-09. Confirmed against the SRE Book Testing for Reliability chapter. Removed: the Testcontainers and
12-factor dev/prod parity sources (not read), the fidelity table of image digest, Kubernetes version and data size, the
GoReplay, Pact and ephemeral-environment per PR techniques, the nightly masked restore, the sample known-gaps text and the
claim that shared staging drifts, none of which the chapter says.

Method: docs-checked 2026-11-09 against the page above, read from a downloaded copy; no commands were run.
