---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.dev-prod-parity
name: dev-prod-parity
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, 12-factor-app, twelve-factor, dev-prod-parity, environment-parity, continuous-deployment, backing-services]
level: practitioner
status: docs-checked
description: "Apply factor X: shrink the time, personnel and tools gaps between dev and prod; same type and version of each backing service in every deploy."
sources: ["https://12factor.net/dev-prod-parity"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Factor X: dev/prod parity

The twelve-factor app is designed for continuous deployment by keeping the gap between development and
production small. 12factor.net names three gaps:

| Gap | Traditional app | Twelve-factor app |
|---|---|---|
| Time between deploys | weeks (code can take days, weeks or months to reach production) | hours, even minutes |
| Code authors vs deployers | different people | the same people |
| Dev vs production environments | divergent (for example Nginx, SQLite and OS X locally, Apache, MySQL and Linux in production) | as similar as possible |

## Close the tools gap
1. Use the same type and version of each backing service (database, queue, cache) in development, staging
   and production.
2. Resist the urge to use a lightweight stand-in locally (SQLite locally and PostgreSQL in production, or
   in-process memory locally and Memcached in production), even when an adapter library abstracts the
   difference. Tiny incompatibilities cause code that passed in development or staging to fail in production, and
   that friction discourages continuous deployment.
3. Make running the real service locally cheap. The page points to system package managers (Homebrew, apt-get)
   and to declarative provisioning tools (Chef, Puppet) with lightweight virtual environments (Docker,
   Vagrant) so developers can run environments that closely approximate production.
4. Keep adapter libraries: they make porting to a new backing service painless. They do not replace using the
   same service type and version everywhere.

## Close the time and personnel gaps
- Deploy code hours or minutes after it is written.
- The developers who wrote the code are closely involved in deploying it and watching its behaviour in production.

## Verify
- [ ] Every deploy, including each developer's, uses the same type and version of every backing service.
- [ ] Time from commit to production is measured in hours, not weeks.

## Checked
2026-11-09. Confirmed against the 12factor.net Dev/prod parity page (read in full). Removed claims and sources
that were not read or are not on the page: Testcontainers, LocalStack and cloud emulators, preview environments per
pull request, same container image locally and in production, and the DORA lead-time check. The page predates
modern container tooling; Docker is mentioned only alongside Vagrant as a lightweight virtual environment.
Method: docs-checked 2026-11-09 against https://12factor.net/dev-prod-parity (read in full); documentation only, no commands run.
