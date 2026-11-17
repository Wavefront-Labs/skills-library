---
id: computing-software.software-engineering.refactoring.refactoring-workflow-and-principles
name: refactoring-workflow-and-principles
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, refactoring-workflow, refactoring-principles, small-steps, two-hats, preparatory-refactoring]
level: practitioner
status: draft
description: "Refactor the way Fowler's chapter 2 describes: two hats, tiny behaviour-preserving steps under tests, frequent commits, preparatory and opportunistic refactoring, and when not to."
sources: ["https://martinfowler.com/books/refactoring.html", "https://martinfowler.com/articles/workflowsOfRefactoring/", "https://martinfowler.com/articles/preparatory-refactoring-example.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Refactoring workflow and principles

**Definition:** a change to internal structure that preserves observable behaviour, made in small
steps. If the code is broken for days, that's restructuring, not refactoring.

## The loop
1. Tests green (if there are none, write characterisation tests first).
2. Make one small refactoring step (extract, rename, move).
3. Compile and run the relevant fast tests (seconds).
4. Commit (locally) when green. Many tiny commits are fine; squash later if you like.
5. If tests fail and the cause isn't obvious in a minute, revert to the last green commit
   (`git reset --hard` / `git checkout .`) and take a smaller step.

## Two hats (Kent Beck)
At any moment you are either **adding function** (new tests, behaviour changes) or **refactoring**
(no new behaviour, tests unchanged). Switch hats consciously; don't mix both in one commit.

## When (Fowler's workflows)
- **Preparatory**: "make the change easy, then make the easy change" before a feature.
- **Comprehension**: rename and extract while reading code to understand it.
- **Litter-pickup / campground rule**: small improvements in code you're touching anyway.
- **Planned**: occasionally needed for big debt, but the default is continuous small refactoring
  inside normal work, not separate "refactoring sprints".
- **Long-term**: branch by abstraction / strangler for big changes, still in small mergeable steps.

## When not to
Code you don't need to change or understand; code that will be rewritten soon; when tests can't
be added at reasonable cost (then use scratch refactoring to learn, and throw it away).

## Team practices
- Refactor in commits/PRs separate from behaviour changes, so reviews are easy.
- Trunk-based development with small merges; long-lived refactoring branches cause merge pain.
- Performance: refactor for clarity first, then profile and optimise the hot spots; clean code is
  easier to tune.
- Explain refactoring to managers as part of feature work: it is how you go faster, not a separate cost.
