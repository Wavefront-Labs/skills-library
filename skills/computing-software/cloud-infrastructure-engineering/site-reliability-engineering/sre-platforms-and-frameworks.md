---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.sre-platforms-and-frameworks
name: sre-platforms-and-frameworks
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre-platform, production-platform-frameworks, sre-engagement, platform-engineering, paved-road, golden-path]
level: advanced
status: docs-checked
description: "Scale SRE engagement with frameworks and a production platform as the Google SRE Book describes: why per-service PRRs do not scale, framework principles, benefits."
sources: ["https://sre.google/sre-book/evolving-sre-engagement-model/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SRE platforms and frameworks

Source: SRE Book "The Evolving SRE Engagement Model", section "Evolving Services Development: Frameworks and SRE Platform".

## Why per-service PRRs stopped scaling
The book's lessons learned: onboarding a service took two or three SREs and typically two or three quarters; lead times were quarters away and takeovers were serialised; each production feature was reimplemented per service (the canonical example is functionally similar logging frameworks written repeatedly in one language); fixes for common issues like overload and data hot-spotting could not be replicated easily; SRE contributions were local to a service. External pressure: microservices increase the number of services, each with a base fixed operational cost, and expect lower deployment lead time; hiring SREs is difficult and training is lengthy.

## Principles of the framework model
- Codified best practices: commit what works in production to code so services become "production ready" by design.
- Reusable solutions for scalability and reliability mitigations.
- A common production platform with a common control surface: uniform interfaces to production facilities, uniform operational controls, and uniform monitoring, logging and configuration.
- Easier automation and smarter systems, such as a single view of relevant information for an outage.

## What frameworks contain
Google built SRE-supported frameworks for each supported environment (Java, C++, Go). Framework modules encapsulate concerns such as instrumentation and metrics, request logging, and control systems for traffic and load management. The book's example features: standard dimensions for monitoring instrumentation, a standard format for request debugging logs, a standard configuration format for load shedding, and a consistent measure of single-server capacity and "overload". Different language implementations cannot share code but aim to expose the same API, behaviour, configuration and controls.

## Benefits the book reports
- Lower operational overhead: conformance tests for coding structure, dependencies and tests, built-in deployment, monitoring and automation, easier management of many microservices, and deployment of an idea to SRE-level production quality "in a matter of days".
- Universal support by design: services that do not get full SRE support can still use SRE-maintained production features.
- Faster engagements: onboarding usually by a single SRE during one quarter, with less cognitive burden.
- Shared responsibility: SREs support the platform infrastructure (load shedding, overload, automation, traffic management, logging, monitoring) while developers provide on-call for functional issues in application code. Platform teams are staffed by need to maintain the platform rather than by service count (footnote 153).
- All three models (Simple PRR, early engagement, frameworks) are still practised at Google; frameworks are becoming the prominent influence.

## Applying it
Treat the specific tooling (templates, scorecards, platform APIs) as your own design; the book describes the principles and benefits, not products.

## Verify
- [ ] New services get logging, metrics, overload controls and deployment from shared framework code rather than per-service work.
- [ ] Platform ownership and the on-call split between platform and application are written down.

## Checked
Confirmed against the SRE Book "The Evolving SRE Engagement Model" (Lessons Learned, External Factors, Frameworks, New Service and Management Benefits, Conclusion, footnote 153). Removed: the modernised concern table (RED metrics, autoscaling, quota checks), Backstage and cookiecutter templates, scorecards, the escape-hatch and drift gotchas, and the Workbook and Backstage sources which were not read for this review.
Method: docs-only read of cited pages, 2026-11-08
