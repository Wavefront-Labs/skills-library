---
id: education-training.instructional-design.scorm-and-xapi.packaging-and-debugging-lms-tracking
name: packaging-and-debugging-lms-tracking
category: education-training
field: instructional-design
product: scorm-and-xapi
tags: [scorm-and-xapi, scorm, scorm-1-2, scorm-2004, xapi, tin-can, cmi5, aicc, lrs, learning-record-store, imsmanifest, imsmanifest-xml, cmi-core-lesson-status, cmi-completion-status, cmi-success-status, cmi-suspend-data, lmsfinish, lmscommit, actor-verb-object, xapi-statements, scorm-cloud, lms-tracking, completion-tracking, bookmarking, resume, elearning-standards, adl, debugging]
level: advanced
status: draft
description: "Package e-learning as SCORM 1.2/2004, xAPI or cmi5 and debug tracking: the data model fields that matter, how completion is reported, testing in SCORM Cloud, and fixing courses that won't complete."
sources:
  - "ADL Initiative: SCORM 2004 4th Edition, xAPI 1.0.3 and cmi5 specifications (adlnet.gov)"
  - "Rustici Software, scorm.com technical guides and SCORM Cloud"
  - "IEEE 9274.1.1-2023 (xAPI 2.0) — newer standard; verify LRS support"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Packaging and debugging LMS tracking (SCORM, xAPI, cmi5)

**Goal:** an e-learning package that launches, resumes, completes and reports a score in
the target LMS first time — and a method for finding out why when it doesn't.

## 1. Pick the standard the LMS actually supports
| Standard | Use when | Notes |
|---|---|---|
| **SCORM 1.2** | Broadest LMS support; simple completion + score | `suspend_data` limited to 4,096 characters — long courses can overflow it |
| **SCORM 2004 (3rd/4th ed.)** | Need separate completion and pass/fail, bigger suspend data, sequencing | Support quality varies by LMS |
| **xAPI** | Tracking outside an LMS (apps, simulations, offline), rich data | Needs a Learning Record Store (LRS); LMS integration varies |
| **cmi5** | xAPI with LMS-style launch and rules | Growing support; check the LMS |
Ask the LMS admin which standard and edition they recommend; "supports SCORM" often means 1.2 well and 2004 less so.

## 2. What's in a SCORM package
A zip with `imsmanifest.xml` **at the root** (not inside a subfolder), plus the course files.
The manifest lists the launch file (SCO). Zipping the parent folder instead of its contents is
the classic upload failure.

## 3. The fields that decide completion
**SCORM 1.2:** one status field `cmi.core.lesson_status`: `passed`, `failed`, `completed`,
`incomplete`, `browsed`, `not attempted`. Score in `cmi.core.score.raw` (+ min/max).
**SCORM 2004:** two fields — `cmi.completion_status` (completed/incomplete) and
`cmi.success_status` (passed/failed/unknown); score in `cmi.score.scaled` (−1 to 1) and `raw`.
Bookmarking uses `cmi.core.lesson_location` / `cmi.location` and `suspend_data`.
The course must call **Commit** (`LMSCommit` / `Commit`) and **Finish/Terminate** for data to
save reliably.

## 4. xAPI basics
A statement = **actor** (who) + **verb** (an IRI, e.g. `http://adlnet.gov/expapi/verbs/completed`)
+ **object** (activity IRI), optionally **result** (score, success, completion, duration) and
**context**. Example:
```json
{"actor":{"mbox":"mailto:learner@example.com"},
 "verb":{"id":"http://adlnet.gov/expapi/verbs/passed","display":{"en-US":"passed"}},
 "object":{"id":"https://example.com/courses/fire-safety"},
 "result":{"score":{"scaled":0.85},"success":true,"completion":true}}
```
Use established verb vocabularies (ADL, cmi5) rather than inventing verbs; agree activity IRIs
that stay stable across versions.

## 5. Debug procedure: "the course won't complete"
1. **Reproduce in SCORM Cloud** (free tier). If it completes there, the problem is LMS
   configuration; if not, it's the package.
2. Check the **authoring tool's tracking setting** — completion by slides viewed vs quiz result
   (see education-training.instructional-design.articulate.building-storyline-interactions-with-triggers-and-variables).
3. Check the **LMS's mapping**: some LMSs only treat `passed` as done; others want `completed`.
   SCORM 1.2 packages reporting "passed/incomplete" vs "completed/incomplete" behave differently.
4. Open the LMS or SCORM Cloud **debug log** and look for: was `Initialize` called, which values
   were set, did `Commit`/`Terminate` run? Learners who close the browser tab abruptly may skip
   Terminate.
5. Look for **suspend_data overflow** (SCORM 1.2) on long courses — symptoms: resume fails or
   progress resets. Fix by publishing as SCORM 2004 or reducing tracked state.
6. Check **pop-up blockers and iframe/third-party cookie rules** if the course doesn't launch or
   can't find the API.
7. For xAPI: query the LRS for the learner's statements; check endpoint, credentials and that the
   actor identifier matches the LMS user.

## Gotchas
- **Re-uploading a new version** may reset or orphan existing learner attempts; check the LMS's
  versioning option before replacing a live package.
- **Mastery score in the manifest** can override the course's internal pass mark.
- **Multi-SCO packages** need sequencing rules the LMS may ignore; prefer single-SCO.
- Keep credentials out of course files; xAPI auth details belong in launch parameters/LMS config.
- *Unconfirmed:* xAPI 2.0 (IEEE 9274.1.1) adoption by LRSs and LMSs is uneven; confirm before using 2.0-only features.

## Verify
- [ ] The zip has `imsmanifest.xml` at its root and uploads without error.
- [ ] In SCORM Cloud, the package launches, resumes at the bookmark, completes and reports score.
- [ ] The completion/success values match what the LMS counts as done.
- [ ] The same test passes in the production LMS with a test learner.
- [ ] For xAPI, expected statements appear in the LRS with the right actor and verbs.
