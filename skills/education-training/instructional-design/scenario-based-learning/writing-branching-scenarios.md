---
id: education-training.instructional-design.scenario-based-learning.writing-branching-scenarios
name: writing-branching-scenarios
category: education-training
field: instructional-design
product: scenario-based-learning
tags: [scenario-based-learning, branching-scenarios, branching, decision-points, simulations, case-based-learning, consequences, realistic-feedback, intrinsic-feedback, action-mapping, cathy-moore, flowchart, twine, storyline, rise-scenario-block, soft-skills-training, compliance-training, customer-service-training, sales-training, healthcare-simulation, distractors, plausible-mistakes, debrief, instructional-design]
level: practitioner
status: draft
description: "Design branching scenarios that teach judgement: choose decisions worth practising, write plausible wrong options, show consequences before telling, keep the branch map small."
sources:
  - "Moore, C. Map It (2017) and her branching-scenario writing guidance"
  - "Clark, R. C. Scenario-Based e-Learning (2013)"
  - "Twine (twinery.org) documentation for prototyping"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing branching scenarios

**Goal:** a scenario where learners make the kind of decisions the job demands, see the
realistic results of their choices, and leave better at judging — not just better at
recognising the "right" answer on a quiz.

## 1. Choose decisions worth a scenario
Scenarios are expensive. Use them where the job requires **judgement under ambiguity**: a
customer escalation, a clinical deterioration, a manager's difficult conversation, a safety
call. For fact recall or a fixed procedure, a simpler practice activity is better.
From your task analysis, list the **2–4 critical decisions** where people actually go wrong,
and ask SMEs: *What do new people do here? Why does it seem reasonable to them?*

## 2. Write the decision points
Each decision point has:
- **Situation** — concise, specific, in the second person, with the information a real
  performer would have (and lack). 50–150 words is plenty.
- **Options** — usually 3. One best, one or two **plausible mistakes** drawn from what real
  people do. If an option is obviously silly, nobody learns from rejecting it.
- Write options as **actions**, not opinions ("Offer the refund now", not "Refunds are good").
- Avoid tells: the right answer shouldn't be the longest or the only polite one.

## 3. Consequences before commentary
- **Intrinsic feedback first:** show what happens — the customer's reply, the patient's vitals,
  the colleague's face. Let the learner infer the quality of the choice.
- **Instructive feedback** after (or at the end): why that happened, what an expert would weigh.
- Mistakes should lead somewhere realistic: often a **recoverable** path (the situation gets
  harder but can be rescued) and occasionally an end state that shows the cost.

## 4. Keep the structure under control
Full trees explode (3 options × 4 levels = 81 endings). Common patterns:
- **Gauntlet / mostly linear:** wrong choices get feedback and loop back to retry.
- **Bottleneck / fold-back:** branches diverge for a step or two, then reconverge at the next
  key moment, carrying a state (e.g. "customer trust: low").
- **Short deep tree:** fully branching but only 2–3 levels, with 3–5 distinct endings.
Draw the flowchart before writing prose. **Twine** (free) or a whiteboard tool is fast for
prototyping; build later in the authoring tool (Storyline variables, Rise's scenario block for
simpler linear versions).

## 5. End with a debrief
Summarise the path the learner took, the endings they could have reached, and the principle
behind the best choices. Offer a **replay** — exploring other paths is part of the learning.
In live or blended settings, debrief as a group discussion.

## Writing tips
- Characters need names, roles and one sentence of motive; keep the cast small.
- Use real language from the workplace (with SME check), not training-speak.
- Pilot with 2–3 real performers: if experts disagree on the "best" option, either the situation
  needs more detail or the decision really is a judgement call — say so in feedback.

## Gotchas
- **A quiz in costume:** a short story followed by "Which of the following is correct?" isn't a
  scenario. The choice must be an action in context.
- **Punishing exploration** with scores discourages trying alternatives; consider scoring only the
  first attempt or not at all.
- **Sensitive content** (harassment, clinical harm) needs SME and often HR/legal review and a
  content note.
- **Branch maintenance**: every policy change touches every path; keep the source flowchart current.
- *Uncertainty:* evidence on scenarios' transfer advantage over simpler practice is promising but
  context-dependent; evaluate with a job-relevant measure, not satisfaction scores.

## Verify
- [ ] Each decision point targets a real, documented mistake from the task analysis.
- [ ] Every wrong option is something a reasonable novice might actually do.
- [ ] Consequences are shown before explanations.
- [ ] The branch map fits on one page and every path ends in a debrief.
- [ ] A pilot with real performers confirmed options are plausible and the best choice defensible.
