---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.adr-format
name: adr-format
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [adr-format, architecture-decision-records, adr, madr, nygard, decision-log, decision-rationale, enterprise-architecture]
level: practitioner
status: docs-checked
description: "Capture context, decision, status and consequences in a short ADR using Nygard or MADR formats and keep it with the code or repository."
sources:
  - https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
  - https://adr.github.io/madr/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Write an architecture decision record

Goal: preserve why, not only what.

## Nygard format (2011 article)
- Store each record in the project repository, in the article's layout `doc/arch/adr-NNN.md`. Numbers increase sequentially and are never reused. Use a lightweight markup such as Markdown.
- Sections: Title (short noun phrase), Context (competing forces: technical, political, social and project-specific, described neutrally), Decision (the response, in active voice), Status, Consequences (all outcomes: positive, negative and neutral).
- Status is "proposed" until stakeholders agree, then "accepted"; a later record can mark it "deprecated" or "superseded", linking to its replacement.
- Keep records short, ideally one or two pages, written as if explaining the decision to a future developer.
- If a decision is reversed, keep the old record and mark it superseded rather than deleting it.

## MADR format
Sections in order: Title; Context and Problem Statement; Decision Drivers (optional); Considered Options; Decision Outcome (with an optional Consequences subsection); Confirmation (optional); Pros and Cons of the Options (optional, Good/Bad/Neutral per option); More Information (optional).
- Status values in the template: proposed, rejected, accepted, deprecated, superseded (for example "superseded by ADR-0123").
- Optional front matter: `status`, `date` (last updated, YYYY-MM-DD), `decision-makers`, `consulted`, `informed`.
- File naming: `NNNN-title-with-dashes.md`, lowercase with dashes, `.md` suffix, in a `decisions/` subfolder (optionally category subfolders, in which case numbers are unique only within each category).

Gotchas:
- Record the options you considered and why they lost; MADR has a place for this (Considered Options, Pros and Cons) and a "rejected" status.
- Do not rewrite accepted records; supersede them.

Verify: a new joiner understands the reason behind the decision without asking.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed on Michael Nygard's article and the MADR template page. Removed: the TOGAF, ArchiMate, Zachman, Business Architecture Guild and DoDAF sources (none of them define the ADR format; the TOGAF pages require a login) and the "one decision per record" rule (the article does not state it).
