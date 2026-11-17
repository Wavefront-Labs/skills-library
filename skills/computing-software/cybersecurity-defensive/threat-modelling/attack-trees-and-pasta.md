---
id: computing-software.cybersecurity-defensive.threat-modelling.attack-trees-and-pasta
name: attack-trees-and-pasta
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [attack-trees, pasta, risk-centric-threat-modelling, threat-modelling-methodology, attack-likelihood, dread]
level: advanced
status: docs-checked
description: "Build attack trees with AND/OR nodes and propagated values (Schneier), and know where PASTA and other methods fit (SEI summary)."
sources: ["https://www.schneier.com/academic/archives/1999/12/attack_trees.html", "https://insights.sei.cmu.edu/blog/threat-modeling-12-available-methods/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attack trees and PASTA

**Goal:** model a specific attacker goal as a tree of ways to reach it, then use node
values to compare attacks and test countermeasures. PASTA is the risk-centric framework
that attack trees often sit inside.

## 1. Attack trees (Schneier, Dr. Dobb's Journal, December 1999)
- The attack goal is the root node; ways of achieving it are the children. Each node becomes a
  subgoal, and its children are ways to achieve that subgoal. Each goal forms a separate tree,
  although trees may share subtrees and nodes.
- OR nodes are alternatives. AND nodes are different steps that must all be achieved (to
  eavesdrop on a combination, attackers must both listen to the conversation and get the owner
  to say it).
- Leaf values can be Boolean (possible or impossible, easy or difficult, expensive or not,
  legal or illegal, special equipment needed or not) and propagate up the tree. An OR node is
  possible if any child is; an AND node only if all children are.
- Values can also be continuous. For cost, an OR node takes the value of its cheapest child
  and an AND node the sum of its children. Probability of success and likelihood that an
  attacker tries an attack are other possible values.
- Query the tree with combined values: cheapest attack needing no special equipment, most
  likely nonintrusive attack, best low-skill attack, and so on.
- Link the tree to knowledge about attackers. Skill, access, risk aversion and money differ
  by attacker, and the attacker's characteristics decide which parts of the tree matter.
- "What if" countermeasures: change a node value (the cost of the cheapest attack) and
  recalculate the root to see its effect.
- Building one: identify attack goals, think of all attacks on each goal, repeat down the
  tree, then give the tree to someone else to add nodes. Repeat over time, because node values
  change as attacks get easier or better information arrives.
- Uses Schneier lists: check whether the goal is vulnerable, list the security assumptions,
  assess a system change or a newly found vulnerability, and compare or rank attacks.
- Schneier's PGP example found that attacks on the cryptography were not the most profitable
  ones; keystroke capture, passphrase recovery or private key theft were easier.

## 2. PASTA (SEI summary)
- PASTA (Process for Attack Simulation and Threat Analysis) is a risk-centric framework
  developed in 2012, with seven stages, each with several activities.
- It aims to bring business objectives and technical requirements together, involves key
  decision makers, and needs security input from operations, governance, architecture and
  development.
- It uses an attacker-centric perspective to produce an asset-centric output: threat
  enumeration and scoring.

## 3. How attack trees relate to other methods (SEI)
- SEI describes attack trees as one of the oldest and most widely applied techniques, used on
  cyber, cyber-physical and purely physical systems, first stand-alone and later combined
  with STRIDE, CVSS and PASTA.
- For a complex system, trees can be built per component rather than for the whole system.
- SEI's Quantitative Threat Modeling Method builds component attack trees for STRIDE
  categories and then applies CVSS scores to the components in the tree.
- SEI recommends no single method; choose by the area to target (risk, security, privacy),
  time available, experience and stakeholder involvement.

## Gotchas
- Node values are estimates from research; Schneier's figures are illustrative only.
- Trees are never provably complete; Schneier notes there is always a chance an attack was
  forgotten.

## Verify
- [ ] The root is a specific named goal.
- [ ] Each leaf has a stated value and the attacker profile it assumes.
- [ ] The tree has an owner and is recalculated when values or the system change.

## Checked
Confirmed 2026-11-09 against Schneier's "Attack Trees" (read in full) and the SEI blog "Threat Modeling: 12 Available Methods" (read in full).
Removed as unconfirmed: the numbered PASTA stage names, the claim that STRIDE is weaker than trees at likelihood ranking, the helpdesk and phishing examples, the product and weakest-link scoring for AND nodes, the low/medium/high scoring advice, the PASTA slow-process warning and the VerSprite and OWASP sources, which were not read.
Method: docs-checked 2026-11-09 against schneier.com attack_trees and insights.sei.cmu.edu threat-modeling-12-available-methods
