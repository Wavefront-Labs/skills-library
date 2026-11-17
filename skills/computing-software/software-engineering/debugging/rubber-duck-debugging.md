---
id: computing-software.software-engineering.debugging.rubber-duck-debugging
name: rubber-duck-debugging
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, rubber-duck-debugging, explaining-the-problem, assumptions, pair-debugging]
level: intro
status: draft
description: "Use rubber duck debugging: explain the code and problem line by line to someone or something, exposing the unchecked assumption that hides the bug."
sources: ["https://rubberduckdebugging.com/", "https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/", "https://www.debuggingbook.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Explaining the problem (rubber duck debugging)

From The Pragmatic Programmer: explain the problem out loud, in detail, to a rubber duck (or a
colleague who just listens). Articulating each step forces you to state assumptions you'd skipped,
and the bug often reveals itself mid-sentence.

## How to do it properly
1. State the **expected** behaviour and the **actual** behaviour precisely ("returns 0 for an
   order with two lines; expected 42.50").
2. Describe the inputs and environment, including what you have already ruled out and how.
3. Walk the code path **line by line**, saying what each line does and what every variable holds
   at that point. Do not summarise ("then it calculates the total"); say how.
4. For each claim, ask: "do I know this, or am I assuming it?" Mark assumptions and check them
   (print, debugger, test).

## Typical discoveries
- The code you're reading isn't the code that runs (stale build, wrong branch, cached artefact,
  different config file, wrong environment).
- An assumption about a library ("this returns a copy", "this is sorted", "this is UTC").
- A misread condition (`<` vs `<=`, operator precedence, negation).
- Data isn't what you think (whitespace, encoding, null vs empty, different type).

## Written variants
- Write the bug report or a question for a colleague/Stack Overflow with a minimal example. Making
  the example minimal frequently solves it.
- Keep a debugging log: hypothesis, test, result. Rereading it is rubber-ducking with yourself.

## With a person
Ask the listener to stop you whenever you skip a step, and not to propose solutions until you've
finished explaining. Time-box solo debugging (e.g. 30-60 minutes without progress) before asking
someone; the cost of a 10-minute explanation is low.
