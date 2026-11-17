---
id: education-training.curriculum-and-assessment-design.assessment-platforms.authoring-delivering-and-analysing-digital-assessments
name: authoring-delivering-and-analysing-digital-assessments
category: education-training
field: curriculum-and-assessment-design
product: assessment-platforms
tags: [assessment-platforms, digital-assessment, online-testing, item-bank, item-banking, question-bank, gradescope, examsoft, formative, goformative, edulastic, pear-assessment, moodle-quiz, canvas-new-quizzes, inspera, questionmark, learnosity, qti, standards-tagging, randomisation, question-pools, accommodations, extra-time, lockdown-browser, proctoring, rubric-grading, answer-groups, item-analysis, results-dashboard, regrade]
level: practitioner
status: draft
description: "Run digital assessments in platforms like Gradescope, ExamSoft, Formative or Edulastic: build a tagged item bank, configure delivery and accommodations, grade with shared rubrics, read item reports."
sources:
  - "Vendor help centres: Gradescope Guides, ExamSoft Support, Formative Help, Edulastic/Pear Assessment Help (checked in general terms only)"
  - "1EdTech (IMS Global) Question & Test Interoperability (QTI) specification"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Authoring, delivering and analysing digital assessments

**Goal:** use an assessment platform so that items are reusable and tagged, delivery is fair
and secure enough for the stakes, grading is fast and consistent, and the results feed back
into teaching.

*Platforms change features and names (e.g. Edulastic is now marketed as Pear Assessment);
check current vendor docs for exact steps.*

## 1. Know the platform's strength
| Platform (examples) | Strength |
|---|---|
| **Gradescope** | Grading paper or PDF/online work fast with shared, editable rubrics; AI-assisted **answer groups** for some question types; strong in higher ed STEM |
| **ExamSoft** (and Inspera, Questionmark) | Secure high-stakes exams, offline/locked-down delivery, item banking with tagging, psychometric reports — common in medical/law/nursing schools |
| **Formative**, **Edulastic/Pear Assessment** | K-12 live and standards-aligned assessment, teacher-friendly item authoring, real-time dashboards |
| LMS quiz engines (Moodle Quiz, Canvas New Quizzes, Blackboard Tests) | Integrated gradebook, question pools, adequate for most course quizzes |

## 2. Build an item bank, not a test
- **One item, many uses:** store items in a bank/pool rather than writing inside a single test.
- **Tag every item**: objective or standard code, topic, cognitive level (Bloom/DOK), difficulty, author,
  date, status (draft/reviewed/retired). Tags drive blueprinted test assembly and per-standard reports.
- Store **rationales/feedback** with each item.
- Use the platform's **review workflow** (or a status tag) so no unreviewed item reaches students.
- For migration, check **QTI** import/export support — and test it; QTI implementations differ and
  formatting, images and math often break.

## 3. Assemble and configure delivery
1. Build the test from the **blueprint** (see
   education-training.curriculum-and-assessment-design.test-item-writing.writing-items-and-blueprinting-a-test)
   using tagged draws, e.g. "3 random items from pool *Transport, Apply*".
2. **Randomise** question and option order where it doesn't break items (turn off for "all of the
   above"-type or ordered numeric options).
3. Set **time limits, availability windows, attempts, and feedback release** (immediately, after
   close, or never for secure items).
4. **Accommodations:** set extra time or separate windows per student — usually a per-student
   override, not a separate test. Check it's applied before the window opens.
5. **Security** proportionate to stakes: lockdown browser and/or proctoring for high stakes;
   question pools and time limits for routine quizzes. Remote proctoring raises privacy and equity
   issues — follow institutional policy.
6. **Preview as a student** on the actual device type, including accessibility (screen reader,
   zoom, keyboard) and math rendering.

## 4. Grade consistently
- In Gradescope-style rubric grading, build the rubric **while grading the first 10–20 submissions**,
  then reuse. Rubric edits apply retroactively to everyone who received that rubric item — powerful
  for consistency, but announce changes to co-graders.
- Divide grading **by question, not by student** among TAs, so each question gets one consistent grader.
- Use **anonymous grading** where available.
- Handle **regrade requests** through the platform with a set window and policy.

## 5. Read the results
- Per item: difficulty, discrimination, distractor choices — then apply
  education-training.curriculum-and-assessment-design.item-analysis-and-psychometrics.classical-item-analysis-for-teacher-made-tests.
- Per standard/objective: mastery by tag → re-teaching plan.
- Per student: weak tags → targeted practice or intervention.
- Fix item problems (miskeys) with the platform's regrade function, which recalculates all scores;
  update the item's status in the bank.

## Gotchas
- **Auto-scored short answers** reject correct variants (units, spelling, equivalent forms); allow
  alternatives or manually review.
- **Randomised forms** must be equivalent — draw from pools of matched difficulty.
- **Feedback settings** that show correct answers immediately leak secure items.
- **Export your data** at term end; licence changes or account closure can lose history.
- **Student data protection** (FERPA, GDPR) — use institution-approved tools only.

## Verify
- [ ] Every item in the bank has objective, level, difficulty and review-status tags.
- [ ] The test was assembled from the blueprint and previewed as a student on target devices.
- [ ] Accommodations were applied per student and confirmed before the window opened.
- [ ] Grading was split by question with shared rubrics; regrade policy published.
- [ ] Item and per-standard reports were reviewed, miskeys regraded, and bank statuses updated.
