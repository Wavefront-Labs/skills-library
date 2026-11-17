---
id: computing-software.qa-testing-engineering.test-case-design.tester-skills-and-constructive-defect-communication
name: tester-skills-and-constructive-defect-communication
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [tester-skills, constructive-defect-communication, testing-principles, soft-skills, defect-reporting]
level: practitioner
status: draft
description: "Build core tester skills and communicate defects constructively: neutral fact-based wording, collaboration framing, and handling pushback on bug reports."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tester skills and constructive defect communication

**Goal:** findings get fixed, not argued about. CTFL v4.0 1.5.1-1.5.2 lists the skills; communication is the one that decides outcomes.

## Core skills
Testing knowledge (techniques), thoroughness and curiosity, attention to detail, analytical and critical thinking, domain knowledge, technical knowledge (tools, logs, APIs, SQL), and communication (listening, writing, teamwork).

## Communicating defects
- Start from the shared goal: "We both want checkout to work for gift cards."
- Report facts: steps, data, expected (with source), actual, evidence. No judgement words ("obviously", "sloppy", "again").
- Describe the failure, not the person: "The total ignores the voucher" not "you forgot the voucher".
- State impact in business terms: users affected, money, legal exposure.
- Ask, do not accuse, when unsure: "Is this expected? The spec says X."
- Deliver bad news early and privately when it is serious; surprises in a big meeting create defensiveness.

## Handling pushback ("works as designed", "can't reproduce")
1. Re-check your oracle; quote the requirement or a comparable product.
2. Provide a minimal reproduction, environment and build ID; offer to pair.
3. If it is a design question, take it to the product owner with options, not demands.
4. Accept a "won't fix" decision that is informed; record the risk.

## Gotchas
- Confirmation bias works both ways: developers expect code to work, testers expect bugs. Evidence settles it.
- Praise good fixes and well-tested code; credibility grows when you are not only the bearer of bad news.

## Verify
Reread your last five reports: each states expected-result source and impact, with no blame words.
