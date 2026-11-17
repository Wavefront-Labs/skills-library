---
id: computing-software.software-engineering.software-architecture.system-context-and-scope
name: system-context-and-scope
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-description, system-context, scope-definition, c4-model, context-diagram]
level: practitioner
status: draft
description: "Define system scope with a context diagram and table of external actors and interfaces (C4 level 1 / arc42 section 3), separating business and technical context."
sources: ["https://c4model.com/diagrams/system-context", "https://docs.arc42.org/section-3/", "https://www.viewpoints-and-perspectives.info/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# System context and scope definition

**Purpose:** a single picture and table everyone agrees on: what is our system, what is outside it,
and what crosses the boundary. Most scope disputes and missed integrations come from skipping this.

## Context diagram (C4 level 1)
- Your system as one box in the middle.
- People (user roles/personas) and external systems around it (payment provider, IdP, ERP, email).
- Labelled arrows: what is exchanged and how ("sends orders via REST/JSON", "nightly SFTP CSV").
- No internal detail, no technology inside the box.

## Business vs technical context (arc42 section 3)
| Partner | Input | Output | Channel / protocol | Owner / SLA |
|---|---|---|---|---|
| Stripe | payment events | charge requests | HTTPS REST + webhooks | vendor, 99.99% |
| Warehouse WMS | stock levels | pick lists | SFTP CSV nightly | Ops team |
| Customer | orders | confirmations | web, email | - |
Business context = what information; technical context = channels, protocols, formats, network.

## Scope decisions to write down
- Explicitly **out of scope** items (we don't do invoicing; ERP does).
- Who owns each interface and its contract; which side changes it.
- Trust boundaries: which arrows cross the internet or a tenant boundary (feeds threat modelling).
- Data classification of each flow (PII, payment data -> PCI scope).

## Techniques
Event storming or a stakeholder workshop to list external actors; check against network egress
logs and integration inventory for systems people forget (monitoring, backups, analytics SDKs).
