---
id: computing-software.software-engineering.software-architecture.design-docs-and-rfc-process
name: design-docs-and-rfc-process
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-description, design-docs, rfc-process, technical-writing, decision-making]
level: practitioner
status: draft
description: "Write design docs and run an RFC process: when one is needed, a structure with alternatives and trade-offs, review flow, decision recording and keeping docs alive."
sources: ["https://www.industrialempathy.com/posts/design-docs-at-google/", "https://blog.pragmaticengineer.com/rfcs-and-design-docs/", "https://github.com/rust-lang/rfcs", "https://adr.github.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Design docs and the RFC process

## When to write one
New system or service, cross-team interface, data model or storage change, anything expensive to
reverse, or where reasonable engineers will disagree. Skip for changes whose design is obvious
from the code; a one-page doc that takes a day is fine, a 30-page one usually isn't.

## Structure (Google-style)
1. **Context and scope**: the problem, current state, constraints. Short.
2. **Goals and non-goals**: non-goals prevent scope creep and clarify trade-offs.
3. **Design**: the proposal with system-context and key sequence diagrams, APIs, data model,
   key algorithms. Focus on trade-offs, not implementation detail.
4. **Alternatives considered**: each with why it lost. The most valuable section for reviewers.
5. **Cross-cutting concerns**: security, privacy, observability, migration/rollout, cost, failure
   modes.
6. **Open questions** and a decision log.

## Process
- Draft -> share with a few experts early (informal) -> open review with a deadline (1-2 weeks) ->
  review meeting only for unresolved disagreements -> decision by a named approver -> status
  `Accepted`/`Rejected`.
- Comments in the doc tool or as a PR (docs-as-code RFC repo, like Rust RFCs) so discussion is
  linked and searchable.
- Record the outcome as an ADR so the decision survives the doc going stale.
- Final comment period (Rust) avoids decisions slipping through while people are away.

## Keep them honest
- Link the doc from the code repo; update or mark "superseded" after significant changes.
- Write in plain language with diagrams; reviewers skim.
- Don't use the doc to seek approval for a decision already implemented; that's documentation.
