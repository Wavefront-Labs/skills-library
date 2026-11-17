---
id: business-finance.product-management.product-discovery.customer-interviews-and-opportunity-validation
name: customer-interviews-and-opportunity-validation
category: business-finance
field: product-management
product: product-discovery
tags: [product-management, product-discovery, continuous-discovery, customer-interviews, user-interviews, mom-test, jobs-to-be-done, jtbd, problem-framing, opportunity-solution-tree, assumption-testing, demand-validation, fake-door-test, smoke-test, concierge-mvp, prototype-testing, teresa-torres, user-research, interview-synthesis]
level: practitioner
status: draft
description: "Find what to build: past-behaviour customer interviews that avoid false positives, an opportunity solution tree, and cheap assumption tests (fake door, concierge, prototype)."
sources: ["Rob Fitzpatrick, The Mom Test (2013)", "Teresa Torres, Continuous Discovery Habits (2021) - opportunity solution tree"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Customer interviews and opportunity validation

**Goal:** commit roadmap capacity only to problems customers demonstrably have, and
solutions with evidence they'll use, instead of building on opinions and polite praise.

## 1. Interview about the past, not the future
People are poor predictors of their own future behaviour and kind to your ideas.
Ask about **specific recent instances**:
- "Tell me about the last time you <did the task>. Walk me through it."
- "What was hardest about that?" "What did you try instead?" "What did that cost you?"
- "Have you looked for / paid for a solution?" (spend = real problem)
Avoid: "Would you use...?", "Do you like this idea?", "How much would you pay?" (all
produce false positives). Pitching during discovery contaminates everything after it.

## 2. Logistics that keep it continuous
- Aim for a small steady cadence (e.g. 1-3 interviews per week by the product trio:
  PM, designer, engineer) rather than one big study per year.
- Recruit via in-product prompts, customer success, sales calls, and churned users
  (they tell you the most). Offer a modest incentive where allowed.
- 30 minutes, one interviewer, one note-taker; record with consent.
- Write a **one-page snapshot** within 24 hours: who, key quotes, opportunities
  (needs/pain points), insights, follow-ups.

## 3. Synthesise into an opportunity solution tree
Top: the **desired outcome** (a product metric you're asked to move, e.g. week-4
retention). Below it: **opportunities** (customer needs/pains, in customer language,
heard from several interviews). Below each: candidate **solutions**. Below each
solution: the **assumptions** that must be true and tests for them.
Pick **one target opportunity** at a time, sized by how many customers hit it and
how badly, then generate at least three solutions so you compare instead of falling
in love with the first.

## 4. Test the riskiest assumption cheaply
List assumptions by type: desirability (they want it), usability (they can use it),
feasibility (we can build it), viability (it works for the business). Map them on
importance × evidence; test the **important, little-evidence** ones first.
| Test | Good for | Cost |
|---|---|---|
| Prototype test (clickable mock, 5-8 users) | usability, comprehension | days |
| Fake door / painted door (button or landing page, measure clicks, then explain) | demand | days |
| Concierge / Wizard-of-Oz (do it manually behind the scenes) | value, workflow | weeks |
| Pre-sale / letter of intent | willingness to pay (B2B) | weeks |
| One-feature spike | feasibility | days |
Set a **success threshold before running** (e.g. "≥8% of exposed users click"), or
you'll rationalise any result as success.

## 5. Problem framing for the team
Write the problem as: "<Segment> struggles to <job> because <cause>, which costs them
<impact>. Today they <workaround>." If you can't fill the workaround, you probably
haven't confirmed the problem.

## Gotchas
- Interviewing only friendly power users skews toward edge features.
- Sales-requested features are data points, not discovery; ask the customer the
  past-behaviour questions yourself.
- Fake doors annoy users if overused; show an honest "coming soon, tell us more" message.
- Five interviews saying the same thing is a signal; one loud customer is an anecdote.
- Uncertain: optimal interview cadence depends on team size and B2B access; the
  weekly habit is a recommendation, not a measured optimum.

## Verify
- [ ] Interview guide has no future-hypothetical or pitch questions.
- [ ] Snapshots written for each interview within a day.
- [ ] Opportunity tree links a target outcome to ≥3 candidate solutions for the chosen opportunity.
- [ ] Riskiest assumption has a test with a pre-set pass threshold.
- [ ] Problem statement includes the current workaround.
