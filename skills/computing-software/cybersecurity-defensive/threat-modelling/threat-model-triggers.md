---
id: computing-software.cybersecurity-defensive.threat-modelling.threat-model-triggers
name: threat-model-triggers
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [threat-modelling-process, threat-model-triggers, security-design-gate, change-classification, owasp-samm, threat-assessment, sdlc-integration]
level: practitioner
status: draft
description: "Decide when a threat model is needed: triggers based on change type, data and exposure, depth tiers, and how to wire the trigger into design and change processes."
sources: ["Threat Modeling Manifesto (threatmodelingmanifesto.org)", "OWASP SAMM - Design / Threat Assessment", "OWASP Threat Modeling Cheat Sheet"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# When to threat model (triggers)

**Goal:** threat models happen for the changes that need them, at the right depth, without
becoming a bottleneck for every small ticket.

## Triggers (any one is enough)
- New system, service or product.
- New external exposure: internet-facing endpoint, public API, partner integration, mobile app.
- New or changed trust boundary: new identity provider, cross-account access, third-party SaaS with data access.
- New sensitive data type handled (payments, health, credentials, children's data) or new data flows to third parties.
- Authentication, authorisation, session or cryptography changes.
- Significant architecture change (monolith to microservices, move to cloud, new message bus).
- AI/LLM features using tools, plugins or private data.
- After a security incident or a pentest finding in the system.

## Depth tiers
| Tier | When | Format | Time |
|---|---|---|---|
| Lightweight | Small feature with a trigger | 4-question checklist in the design doc or ticket | 30-60 min with the team |
| Standard | New service, new exposure | DFD + STRIDE workshop, threats in backlog | Half day |
| Deep | Critical systems, regulated data, high-risk tech | Full model, attack trees, security architect review, validation tests | Days |

The four questions (Manifesto): What are we working on? What can go wrong? What are we going
to do about it? Did we do a good enough job?

## Wiring it in
- Add a "security impact" field to the design doc template and epic template: yes/no per trigger list.
- Architecture review board or design review checks the field; security champions do lightweight models.
- Keep threat models in the repo (`/docs/threat-model.md` or pytm) so changes to code prompt updates.

## Gotchas
- "Threat model everything" fails on capacity; "only big projects" misses risky small changes like a new auth flow.
- One-off models rot: tie updates to the same triggers.
- Security team doing all models alone does not scale; train teams.

## Verify
- [ ] Sample of last quarter's triggered changes all have a model at the right tier.
- [ ] Time from request to completed model tracked and acceptable to delivery teams.
