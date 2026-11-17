---
id: social-sciences.economics.microeconomic-theory.setting-up-and-solving-a-micro-model
name: setting-up-and-solving-a-micro-model
category: social-sciences
field: economics
product: microeconomic-theory
tags: [microeconomic-theory, microeconomics, economic-modelling, optimisation, lagrangian, kkt-conditions, comparative-statics, envelope-theorem, implicit-function-theorem, consumer-theory, producer-theory, game-theory, nash-equilibrium, subgame-perfect-equilibrium, backward-induction, bayesian-nash-equilibrium, perfect-bayesian-equilibrium, mechanism-design, revelation-principle, incentive-compatibility, participation-constraint, welfare-analysis, consumer-surplus, deadweight-loss, pareto-efficiency, general-equilibrium, mas-colell]
level: advanced
status: verified
description: "Build and solve a microeconomic model: minimal primitives, the right equilibrium concept, first-order and KKT conditions, comparative statics, and welfare — with checks against corner cases."
sources: ["Mas-Colell, Whinston & Green, Microeconomic Theory (Oxford 1995)", "Fudenberg & Tirole, Game Theory (MIT 1991)", "Varian, Microeconomic Analysis (3rd ed., Norton 1992)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building and solving a micro model

**Goal:** a model small enough to solve and explain, rich enough to generate the effect
you care about, with results whose sign you can trace to a named assumption.

## 1. Start from the result you want to explain
Write the target in one sentence: "Price caps can raise quantity when the seller has
market power." Then ask what is the *minimum* structure that could produce it. Every
extra agent type, period or friction should earn its place by changing a result.

## 2. Specify primitives explicitly
- **Players/agents** and what each chooses (action sets).
- **Preferences/technology:** functional forms or general assumptions (continuity,
  monotonicity, concavity/quasiconcavity, single crossing).
- **Information:** who knows what and when (types, priors, signals).
- **Timing:** order of moves; draw the game tree or timeline.
- **Equilibrium concept** that matches the timing and information:
  | Structure | Concept |
  |---|---|
  | Simultaneous, complete info | Nash equilibrium |
  | Sequential, complete info | Subgame-perfect (backward induction) |
  | Simultaneous, private types | Bayesian Nash |
  | Sequential with private info (signalling) | Perfect Bayesian / refinements (intuitive criterion) |
  | Price-taking, many markets | Competitive / general equilibrium |

## 3. Solve
- **Unconstrained:** first-order conditions; check second-order conditions or concavity.
- **Constrained:** Lagrangian; with inequalities use **KKT** — complementary slackness
  means checking each candidate regime (constraint binds or not). Corner solutions are
  where many "surprising" results hide.
- **Games:** best-response functions; intersect them. In sequential games solve from the last
  mover back. Check for multiple equilibria and say which you select and why.
- **Mechanism design:** by the **revelation principle**, restrict to direct mechanisms with
  incentive compatibility (IC) and participation (IR) constraints. Typical pattern: the low
  type's IR and the high type's downward IC bind; "no distortion at the top".
- If it will not solve in closed form, specialise functional forms (quadratic, CES, uniform
  types) or solve numerically — but prove the general sign result if you can.

## 4. Comparative statics
- **Implicit function theorem** on the FOC: dx*/dθ = −(∂²f/∂x∂θ)/(∂²f/∂x²). Sign follows from
  the cross-partial when the problem is concave.
- **Envelope theorem** for how the value function moves: only the direct effect of θ matters.
- **Monotone comparative statics** (supermodularity/single crossing; Topkis, Milgrom–Shannon)
  give signs without differentiability or concavity.

## 5. Welfare
State the welfare criterion (total surplus, Pareto, a social welfare function with weights).
Compare equilibrium with the planner's solution; the wedge between the two FOCs names the
inefficiency (externality, market power, information rent). Measure losses as deadweight
loss or compensating/equivalent variation.

## 6. Robustness and presentation
- Push each assumption: which results survive if you drop it? Put the knife-edge cases in
  the text, not hidden in proofs.
- Lead with the simplest case in the body, generalisations in an appendix.
- Give intuition for each proposition in words before the proof.

## Gotchas
- Assuming interior solutions without checking boundaries.
- Using Nash equilibrium for a sequential game, keeping non-credible threats.
- Comparative statics with multiple equilibria: the derivative may refer to a different
  equilibrium than the one selected.
- Quasilinear utility kills income effects — fine, but say that's why a result holds.

## Verify
- [ ] Primitives, timing and information written down; equilibrium concept justified.
- [ ] Second-order/concavity conditions or regime checks done; corners examined.
- [ ] Existence and (non-)uniqueness addressed.
- [ ] Each comparative-static sign traced to a specific assumption.
- [ ] Welfare criterion stated and equilibrium compared with the planner's solution.
- [ ] A numerical example reproduces every proposition.

*Checked with sympy (2026-10-19): linear demand p=a-q, cost c*q gives monopoly q=(a-c)/2, p=(a+c)/2; with a=10, c=2 a cap at p=4 (below the monopoly price 6) lifts quantity from 4 to 6, and the competitive quantity is 8. The implicit-function formula and the envelope theorem were confirmed on f=t*x-x^3/3. In a two-type screening example (valuation theta*q-q^2/2, zero cost) the high type gets the efficient q_h=theta_h and the low type is distorted down, q_l=theta_l-(1-mu)(theta_h-theta_l)/mu. A methods checklist from standard graduate texts; follow field conventions.*
