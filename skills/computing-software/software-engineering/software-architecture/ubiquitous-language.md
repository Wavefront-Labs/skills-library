---
id: computing-software.software-engineering.software-architecture.ubiquitous-language
name: ubiquitous-language
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, ddd, ubiquitous-language, domain-glossary, bounded-context, domain-modeling]
level: practitioner
status: draft
description: "Build and enforce a ubiquitous language per bounded context: glossary, using domain terms in code and conversation, resolving synonyms and homonyms across contexts."
sources: ["https://martinfowler.com/bliki/UbiquitousLanguage.html", "https://www.domainlanguage.com/ddd/reference/", "https://github.com/ddd-crew/ddd-starter-modelling-process"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ubiquitous language

Evans: a shared, rigorous language between domain experts and developers, used in conversation,
documents, tests and **code**, within one bounded context.

## Building it
- Collect terms during event storming, interviews and by reading real artefacts (forms,
  contracts, support tickets). Experts' words, not developers' ("policy holder", not "user").
- Glossary per bounded context: term, definition, examples, counter-examples, related terms,
  owner. Keep it in the repo (`docs/glossary.md`) or a wiki linked from code.
- Probe with scenarios: "what happens to the *quote* when the *customer* changes address after
  *binding*?" Disagreements reveal hidden concepts.

## In code
- Class, method and event names are glossary terms: `Policy.bind()`, `QuoteExpired`, not
  `InsuranceRecord.setStatus(3)`.
- Tests read like domain rules (`a_lapsed_policy_cannot_be_renewed`).
- When the model changes in conversation, rename in code (IDE rename refactoring); stale names are
  language drift.
- Avoid generic technical words in the domain layer: `Manager`, `Processor`, `Data`, `Info`.

## Synonyms and homonyms
- Synonyms (client/customer/account holder) in one context: pick one, list others as aliases.
- Homonyms across contexts are normal: "Account" in Billing (ledger) vs Identity (login). Don't
  force one enterprise-wide definition; give each context its own model and translate at the
  boundary (context map, anti-corruption layer).

## Signs it's failing
Developers translate in their heads during meetings; code names differ from UI labels; bugs
caused by two teams meaning different things by "active customer".
