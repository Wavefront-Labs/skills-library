---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.application-architecture-development
name: application-architecture-development
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [application-architecture-development, adm-phase-c-application, application architecture, application portfolio, application services, application components, target applications, enterprise-architecture]
level: practitioner
status: draft
description: "Define the application portfolio, services and their interactions needed to process the data and support the business."
sources:
  - https://pubs.opengroup.org/togaf-standard/
  - https://pubs.opengroup.org/architecture/archimate32-doc/
  - https://www.zachman.com/about-the-zachman-framework
  - https://www.businessarchitectureguild.org/
  - https://www.dodcio.defense.gov/Library/DoD-Architecture-Framework/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Develop baseline and target application architecture

Goal: identify applications by capability, not by technology.

1. Derive required application services from business services and processes.
2. Map existing applications to those services in the baseline.
3. Define target applications as ABBs, then candidates as SBBs.
4. Describe interfaces and integration patterns.
5. Identify gaps: retire, retain, new, replace.

Gotchas:
- Starting from a product list instead of services reproduces the current mess.
- Shadow IT and SaaS are part of the baseline.

Verify: the Application/Function matrix shows each business function supported at least once.
