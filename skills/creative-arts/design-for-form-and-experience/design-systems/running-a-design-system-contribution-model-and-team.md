---
id: creative-arts.design-for-form-and-experience.design-systems.running-a-design-system-contribution-model-and-team
name: running-a-design-system-contribution-model-and-team
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [contribution-model, design-system-team, design-system-governance, federated-design-system, centralised-design-system, governance, design-ops]
level: practitioner
status: draft
description: "Run design-system governance: choose a team model (centralised, federated, hybrid), define contribution paths, decision rights, intake and review criteria, and staffing."
sources:
  - "Nathan Curtis (EightShapes), Team Models for Scaling a Design System (medium.com/eightshapes-llc/team-models-for-scaling-a-design-system-2cf9d03be6a0)"
  - "Brad Frost, Atomic Design and design system governance (atomicdesign.bradfrost.com)"
  - "Alla Kholmatova, Design Systems (Smashing Media, 2017)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Contribution model and team structure

## Team models (Nathan Curtis)
- **Solitary:** one person or team builds it for themselves; fast, small, bottleneck risk.
- **Centralised:** a dedicated core team owns components; consistent, can lag product needs.
- **Federated:** representatives from product teams contribute; scales, needs strong standards.
- **Hybrid:** a core team plus contribution paths; the most common at scale. Choose by org size, number of products, and funding.

## Contribution model
1. **Paths by size:** (a) *request/bug* via an intake form (problem, product, deadline, examples), (b) *small PR* to fix or extend (core reviews), (c) *new component* via a proposal with research, API, accessibility plan, and a pair-build with the core team.
2. **Criteria** for acceptance: reusable by 3+ teams or a clear pattern; accessible (WCAG AA, keyboard, screen reader tests); documented; tokens only; tests and visual snapshots; design and code parity (`creative-arts.design-for-form-and-experience.design-systems.running-a-design-code-parity-audit`).
3. **Decision rights:** a RACI or simple charter: who triages (weekly), who approves API, who can merge, how conflicts escalate.
4. **Cadence:** weekly office hours and triage, bi-weekly or monthly release train, public roadmap and changelog.
5. **Contributor kit:** templates (component spec, accessibility checklist), a starter repo, Figma file template, a `CONTRIBUTING.md`; recognise contributors.

## Roles
Product owner, design lead, engineering lead, accessibility specialist, documentation/DesignOps; typical starter team 3-5, and an advocate network in product teams.

## Verify
- [ ] Team model chosen deliberately; decision rights documented.
- [ ] Intake, review criteria and release cadence published.
- [ ] Contributions follow the kit and are tracked.
