---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.archimate-notation-conventions
name: archimate-notation-conventions
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [archimate-notation-conventions, archimate-language-structure, archimate notation, element naming, model conventions, layout, colours, diagram style, enterprise-architecture]
level: practitioner
status: draft
description: "Apply ArchiMate icons and alternative notations, naming style and layout conventions to keep models readable."
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

# Notation, naming and diagram conventions

Goal: diagrams readable at a glance.

- Use the standard element shape or icon; layer colours (business yellow, application blue, technology green) are conventional, not mandatory.
- Name elements with nouns for structure, verb phrases for behaviour; services as noun phrases for the service provided.
- Avoid crossing lines; nest elements to show composition and assignment where allowed.
- Add a legend when using non-standard colours.

Gotchas:
- Nesting implies a relationship; define which one in your conventions.
- Keep one idea per view.

Verify: reviewers can read a view without explanation.
