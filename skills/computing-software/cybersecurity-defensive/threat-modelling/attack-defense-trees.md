---
id: computing-software.cybersecurity-defensive.threat-modelling.attack-defense-trees
name: attack-defense-trees
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [attack-defense-trees, adtree, attack-trees, countermeasures, adtool, threat-modelling]
level: advanced
status: draft
description: "Build attack-defence trees that interleave attacker goals with defender countermeasures and counter-attacks, then evaluate them for cost or success probability."
sources: ["https://satoss.uni.lu/software/adtool/", "https://www.schneier.com/academic/archives/1999/12/attack_trees.html", "https://doi.org/10.1093/logcom/exs029"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Attack-defence trees

Plain attack trees show how a goal can be reached (AND/OR refinements) but not what stops it.
Attack-defence trees (Kordy, Mauw, Radomirovic and Schweitzer) add **defence nodes** that counter attack
nodes, and attack nodes that counter defences, so the tree shows the arms race and the residual paths.

## Notation
- Attack nodes are drawn as circles (red), defence nodes as rectangles (green).
- Refinement is OR (any child) or AND (all children, drawn with an arc).
- A **countermeasure** edge (dotted) attaches a node of the opposite type: defence "MFA" under attack "Phish
  password", attack "real-time phishing proxy" under "MFA", defence "FIDO2 keys" under that.

## Building one
1. Root = attacker goal tied to an asset ("Transfer money out of a customer account").
2. Refine with OR/AND down to leaf actions concrete enough to estimate.
3. Attach existing defences to leaves and subgoals. For each, ask "how is this bypassed?" and attach
   counter-attacks. Stop when the counter-attack is out of scope or uneconomic.
4. Leaves without a defence, or whose defence has an un-countered counter-attack, are residual risk.

## Quantitative evaluation
Assign leaf attributes and propagate bottom-up (ADTool automates this):
- Minimal attacker cost: OR = min, AND = sum; a countered attack needs its counter-attack paid for too.
- Success probability: OR = 1 - product(1 - p), AND = product (assumes independence; state that).
- Satisfiability: does any successful attack exist with the deployed defences?
Compare scenarios with and without a proposed control to justify investment.

## Tools
ADTool (University of Luxembourg) edits trees and computes attribute domains. Text formats (Graphviz or
as-code tools) let you diff trees in git.

## Gotchas
- Trees explode; scope to one goal and a timebox, and mark pruned branches "out of scope".
- Numbers are estimates; use them to rank alternatives, not as absolute risk.
- Shared subtrees (the same credential theft under many goals) should be modelled once and referenced.

## Verify
Every leaf has a defence or an explicit accepted-risk note, and the minimal-cost path is called out in the
threat model report.
