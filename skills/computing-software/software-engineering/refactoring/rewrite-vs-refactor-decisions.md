---
id: computing-software.software-engineering.refactoring.rewrite-vs-refactor-decisions
name: rewrite-vs-refactor-decisions
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, rewrite-vs-refactor, strangler-fig, legacy-modernization, technical-debt, risk-management]
level: advanced
status: draft
description: "Decide between incremental refactoring, strangler-fig replacement and a full rewrite, using evidence about the code, the business and the risks of each."
sources: ["https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/", "https://martinfowler.com/bliki/StranglerFigApplication.html", "https://martinfowler.com/articles/patterns-legacy-displacement/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rewrite vs refactor decisions

## Default: incremental
Joel Spolsky's warning stands: big-bang rewrites throw away years of encoded bug fixes and edge
cases, freeze features for a long time, and usually take 2-3x the estimate. Netscape 6 is the
canonical example. Most "unmaintainable" systems are better served by continuous refactoring plus
strangling the worst parts.

## Evidence to gather
- **Hotspots**: change frequency x complexity (git log + complexity; CodeScene, code-maat). Often 5%
  of files drive most pain; refactor those.
- Test coverage and how fast you can get characterisation tests around key flows.
- Platform risk: unsupported runtime, unpatched framework, hiring impossible, licence costs.
- Business: is the domain changing fundamentally (then the old model is wrong, not just messy)?
- Team: do the people who know the old system still exist?

## Options
| Option | When |
|---|---|
| Refactor in place | architecture is roughly right; pain is local; tests feasible |
| **Strangler fig** (Fowler, legacy displacement patterns) | architecture or platform must change; system can be intercepted at seams (routes, events, UI pages) and replaced slice by slice |
| Rewrite a bounded component | small, well-understood, clear interface, replaceable behind an abstraction with parallel run |
| Full rewrite | rarely: tiny system, platform truly dead, or the business model changed so much the old system's behaviour isn't needed |
| Leave it | stable, rarely changed, cheap to run: encapsulate it and move on |

## If you rewrite anything
- Deliver value early: replace a slice that goes live in weeks, not a parallel universe that goes
  live in two years.
- Freeze or dual-implement features in the old system explicitly; decide who pays the double cost.
- Parallel run / dark launch to compare outputs on real data before switching.
- Plan data migration and rollback from the start; that's where rewrites die.
- Define "done": the old system is switched off, not merely the new one launched.

## Write it down
Record the decision in an ADR with the evidence, chosen option, expected milestones and the
conditions under which you'd revisit it.
