---
id: education-training.instructional-design.lms-platforms.setting-up-a-course-gradebook-and-completion-in-an-lms
name: setting-up-a-course-gradebook-and-completion-in-an-lms
category: education-training
field: instructional-design
product: lms-platforms
tags: [lms-platforms, lms, learning-management-system, moodle, canvas, canvas-lms, blackboard, blackboard-learn, d2l, brightspace, schoology, docebo, cornerstone, totara, talentlms, course-setup, course-template, enrolment, enrollment, cohorts, groups, gradebook, weighted-categories, activity-completion, course-completion, release-conditions, restrict-access, modules, prerequisites, completion-reporting, lti, sis-integration]
level: practitioner
status: draft
description: "Set up a course in any LMS (Moodle, Canvas, Blackboard, corporate LMSs): structure modules, enrol learners, build a weighted gradebook, define completion rules, and pull reports."
sources:
  - "Moodle Docs (docs.moodle.org) — Activity completion, Course completion, Gradebook"
  - "Instructure Canvas Guides (community.canvaslms.com)"
  - "Anthology Blackboard Help (help.blackboard.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Setting up a course, gradebook and completion in an LMS

**Goal:** a course whose structure is obvious to learners, whose gradebook calculates what
the syllabus says, and whose completion reports tell the truth — on whichever LMS you've
been given.

## 1. The same five concepts, different names
| Concept | Moodle | Canvas | Blackboard Learn (Ultra) | Corporate LMS (typical) |
|---|---|---|---|---|
| Course shell | Course | Course | Course | Course / curriculum / learning path |
| Unit of structure | Section / topic | Module | Learning module / folder | Module / learning path step |
| Gating | Restrict access | Module requirements & prerequisites | Release conditions | Prerequisites / sequencing |
| Grades | Gradebook (categories) | Gradebook + Assignment groups | Gradebook (categories, overall grade) | Score / pass status |
| Done | Activity + course completion | Module completion / requirements | Progress tracking | Completion status (often from SCORM) |
*Names and menus vary by version and by how your institution has configured the platform.*

## 2. Build from a template
1. Start from your institution's **course template** or copy a working course (Moodle *Import*/
   backup-restore; Canvas *Import Course Content* / Blueprint; Blackboard *Copy content*).
2. Create one module/section per week or unit with the same internal order every time:
   *Overview & objectives → Learn → Practise → Assess*.
3. Write a "Start here" page: how the course works, schedule, contact rules, where help is.

## 3. Enrolment
- Prefer **automated enrolment** from the student information system (SIS) or HR system; manual
  enrolment drifts out of date.
- Use **groups/cohorts/sections** for different intakes or tutors; set them up before assigning work
  so group-restricted activities and grading filters work.
- Check the **role** of every non-student account (teacher, non-editing teacher/TA, observer);
  the wrong role either can't grade or can edit everything.

## 4. Gradebook that matches the syllabus
1. Write the weighting down first, e.g. Quizzes 20%, Assignments 40%, Exam 40%.
2. Create **categories/assignment groups** with those weights; turn on weighting (Canvas: Assignment
   groups › Weight final grade; Moodle: aggregation method *Weighted mean of grades*).
3. Put every graded item in a category and set **points possible** consistently.
4. Decide treatment of **ungraded/missing** items: counted as zero or excluded. Canvas, for example,
   by default calculates on graded items only unless missing policies or "treat ungraded as 0" are
   applied — learners can see inflated grades early in term.
5. Hide or mute grades until released if moderation is needed.
6. Test with a **student view / test student**: submit work, grade it, and check the total.

## 5. Completion rules
- Define completion per activity: viewed, submitted, received a grade, passed (minimum grade).
- Define course completion: all required activities complete, or a final grade threshold, or an
  end date. In corporate LMSs, completion often comes from the e-learning package's SCORM/xAPI
  status (see education-training.instructional-design.scorm-and-xapi.packaging-and-debugging-lms-tracking).
- **Gate sparingly:** restrict-access chains are hard for learners to diagnose when something
  doesn't unlock; explain the rule on the page.

## 6. Reports
Find, before launch, the report you'll be asked for: activity completion matrix, gradebook export
(CSV), course analytics, overdue/compliance report. Check it shows real data from the test student.

## Gotchas
- **Completion set after learners start** may not recalculate past activity; settle rules before launch.
- **Copied courses carry dates**: shift all due/availability dates (most LMSs have a date-shift option on copy).
- **Extra credit and dropped lowest scores** behave differently across platforms; test the math.
- **LTI tools** (publisher content, plagiarism checkers) need grade passback configured and tested.
- **Data protection:** export only what you need; gradebook exports contain personal data.

## Verify
- [ ] Modules follow a consistent internal order and a "Start here" page exists.
- [ ] Enrolment is automated or reconciled, with groups and roles checked.
- [ ] The gradebook weighting reproduces the syllabus; a test student's total is correct by hand.
- [ ] Missing/ungraded work is treated as the policy says.
- [ ] Completion rules are set before launch and the completion report shows the test student correctly.
