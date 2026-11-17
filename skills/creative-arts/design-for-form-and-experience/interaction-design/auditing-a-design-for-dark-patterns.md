---
id: creative-arts.design-for-form-and-experience.interaction-design.auditing-a-design-for-dark-patterns
name: auditing-a-design-for-dark-patterns
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [dark-patterns, deceptive-design, dark-pattern-audit, manipulative-ux, confirmshaming, ethical-design]
level: practitioner
status: draft
description: "Audit an interface for dark patterns: spot common deceptive patterns, assess impact on choice, document evidence, redesign and note the legal context to verify."
sources:
  - "Interaction Design Foundation literature (interaction-design.org/literature)"
  - "Deceptive Design (deceptive.design)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Auditing for dark patterns

Harry Brignull coined the term dark patterns (2010) for interface tricks that push people into actions they did not intend; his site now uses "deceptive patterns". Regulators and researchers have published their own catalogues.

## Common patterns to look for
- **Confirmshaming:** wording that guilts a decline ("No thanks, I do not like saving money").
- **Roach motel:** easy to get in, hard to get out (see `...interaction-design.designing-a-fair-cancellation-flow`).
- **Hidden costs / drip pricing:** fees revealed late in checkout.
- **Misdirection and visual interference:** prominent button for the business-preferred option, faint link for the other.
- **Forced continuity:** a free trial that silently converts without clear notice.
- **Preselected options and sneak-into-basket:** extras added by default.
- **Nagging, false urgency and scarcity:** repeated prompts, fake countdowns or stock messages.
- **Trick wording:** double negatives in opt-outs.
- **Privacy zuckering:** steering to share more data (see `...interaction-design.designing-consent-and-cookie-interfaces`).

## Audit steps
1. Walk through key flows (sign-up, checkout, cancel, privacy settings) as a new user.
2. For each decision point ask: Is the choice clear? Are options presented with equal weight? Is the cost or consequence stated? Can the user reverse it easily?
3. Document with screenshots, the pattern name, severity and the metric that benefits.
4. Propose a fairer design and test it with users.
5. **Legal check:** laws and regulator guidance on deceptive design exist in several jurisdictions (for example consumer protection and privacy rules in the US and EU); this skill does not state specifics, so involve legal counsel.

## Verify
- [ ] Each flagged pattern has evidence and a proposed fix.
- [ ] Opt-in and opt-out choices have equal prominence.
- [ ] Legal review was requested for risky patterns.
