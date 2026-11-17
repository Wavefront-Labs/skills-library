---
id: computing-software.software-engineering.software-architecture.core-supporting-generic-subdomains
name: core-supporting-generic-subdomains
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, ddd, core-domain, subdomains, strategic-design, build-vs-buy]
level: practitioner
status: draft
description: "Classify subdomains as core, supporting or generic, and use that to decide where to invest design effort, what to build, buy or outsource, and team allocation."
sources: ["https://www.domainlanguage.com/ddd/reference/", "https://github.com/ddd-crew/core-domain-charts", "https://www.oreilly.com/library/view/learning-domain-driven-design/9781098100124/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Core, supporting and generic subdomains

## Classify
| Type | Definition | Example (online lender) | Strategy |
|---|---|---|---|
| **Core** | competitive advantage; complex and differentiating | credit risk scoring, underwriting rules | build in-house, best people, rich domain model, DDD tactical patterns |
| **Supporting** | needed, specific to you, not differentiating | loan document generation, broker portal | build simply (CRUD, transaction script) or outsource |
| **Generic** | solved problem everyone has | identity, payments, email, accounting | buy/SaaS/open source |

## How to find them
- Event storming or business capability mapping to list subdomains.
- Ask: "would customers choose us because we do this better?" (core) and "could we buy this off
  the shelf and lose nothing?" (generic).
- Core domain chart (DDD Crew): plot **business differentiation** vs **model complexity**; core is
  high-high. Track movement over time: today's core becomes commodity (e.g. recommendation engines).

## Consequences
- Bounded contexts often align with subdomains but not always; one context may serve several.
- Put senior engineers and domain experts on core; avoid starving it with generic plumbing work.
- Don't hand-build generic subdomains (your own auth, your own ledger) unless constraints force it.
- Supporting subdomains are good candidates for simpler architecture and less test rigour.
- Write a **domain vision statement** for the core: one page on what makes it valuable.

## Pitfalls
Calling everything core; treating a generic subdomain as core because engineers find it fun;
outsourcing the core.
