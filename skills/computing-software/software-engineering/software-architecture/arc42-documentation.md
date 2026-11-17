---
id: computing-software.software-engineering.software-architecture.arc42-documentation
name: arc42-documentation
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-description, arc42, architecture-documentation, solution-strategy, quality-requirements, docs-as-code]
level: practitioner
status: draft
description: "Document an architecture with the arc42 template: what goes in each of the 12 sections, minimal viable arc42, docs-as-code tooling and keeping it current."
sources:
  - https://arc42.org/overview
  - https://docs.arc42.org/home/
  - https://github.com/arc42/arc42-template
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# arc42 architecture documentation

arc42 (Starke and Hruschka) is a free, pragmatic template for communicating and documenting software architecture. Sections are optional; fill what helps readers.

## The 12 sections
1. **Introduction and Goals** - essential requirements, top 3-5 quality goals, stakeholders and their expectations.
2. **Constraints** - technical, organisational, regulatory limits the team must accept.
3. **Context and Scope** - business and technical context: external interfaces, partners, channels (C4 context diagram fits here).
4. **Solution Strategy** - the few fundamental decisions and approaches (technology, decomposition, how quality goals are achieved). Short.
5. **Building Block View** - static decomposition, level by level (C4 container/component diagrams).
6. **Runtime View** - important scenarios as sequence/dynamic diagrams (startup, critical use cases, error handling).
7. **Deployment View** - infrastructure, environments, mapping of building blocks to nodes.
8. **Crosscutting Concepts** - patterns and rules used across the system: domain model, persistence, security, error handling, logging, i18n.
9. **Architecture Decisions** - ADRs or links to them.
10. **Quality Requirements** - quality tree and concrete quality scenarios (see the quality-attribute scenarios skill).
11. **Risks and Technical Debt** - known problems, prioritised.
12. **Glossary** - domain and technical terms.

## Minimal viable arc42
For most teams: 1 (goals), 3 (context), 4 (strategy), 5 (building blocks, level 1-2), 9 (decisions), 11 (risks). Add 6/7/8 as complexity grows. A short, current document beats a complete, stale one.

## Docs as code
- Template available in AsciiDoc and Markdown (`arc42/arc42-template`); keep in `docs/architecture/` in the repo, reviewed via pull requests.
- Render with docToolchain, Antora, MkDocs, or Docusaurus; embed diagrams from Structurizr/PlantUML/Mermaid so they regenerate.
- Link ADRs (`docs/adr/0007-use-postgres.md`, adr-tools/log4brains) from section 9.

## Keeping it alive
- Make "update arc42 if this changes the architecture" a PR template checkbox.
- Review sections 10-11 at each quarterly planning; delete outdated content rather than leaving it.
- Write for a reader: state the audience at the top of each section.

## Verify
- [ ] Top quality goals in section 1 trace to scenarios in section 10 and to decisions in section 9.
- [ ] Docs build in CI; broken diagram includes fail the build.
