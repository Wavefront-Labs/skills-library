---
id: social-sciences.education-research.learning-analytics.predicting-outcomes-from-lms-clickstream-data
name: predicting-outcomes-from-lms-clickstream-data
category: social-sciences
field: education-research
product: learning-analytics
tags: [learning-analytics, educational-data-mining, edm, lms-data, clickstream, moodle-logs, canvas-data, blackboard, xapi, caliper, early-warning-system, at-risk-prediction, dropout-prediction, feature-engineering, temporal-validation, data-leakage, logistic-regression, random-forest, xgboost, auc, calibration, algorithmic-fairness, bias-audit, student-privacy, ferpa, gdpr, ethics-of-educational-data, oulad, dashboard-research, scikit-learn]
level: advanced
status: draft
description: "Build and evaluate research models predicting student outcomes from LMS clickstream logs: data extraction, feature engineering, leakage-free temporal validation, fairness audits and privacy/ethics."
sources:
  - "Kuzilek, Hlosta & Zdrahal (2017), Open University Learning Analytics Dataset, Scientific Data"
  - "Gardner & Brooks (2018), Student success prediction in MOOCs, User Modeling and User-Adapted Interaction"
  - "Baker & Hawn (2022), Algorithmic bias in education, Int. J. Artificial Intelligence in Education"
  - "Slade & Prinsloo (2013), Learning analytics: ethical issues and dilemmas, American Behavioral Scientist"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Predicting outcomes from LMS clickstream data

**Goal:** build a model that identifies students likely to fail or withdraw early enough
to act, from learning-management-system (LMS) activity — and evaluate it honestly, so a
research claim (or a deployed early-warning dashboard) isn't built on leakage or bias.

## 1. Data and permissions first
- **Governance**: institutional data-sharing approval, ethics review, and a lawful basis
  (FERPA "legitimate educational interest" in the US; GDPR legal basis and a DPIA in
  the EU/UK). Decide up front whether students will be told, can opt out, and who will
  see predictions.
- **Sources**: Moodle log tables (`mdl_logstore_standard_log`), Canvas Data 2 / Canvas
  Live Events, Blackboard data, or xAPI/Caliper records in a learning record store;
  join to student information system data (grades, enrolment, demographics) via
  pseudonymised IDs.
- Practise on open data first: **OULAD** (Open University) is a common benchmark.

## 2. Define the prediction problem precisely
- **Outcome**: fail/withdraw/final grade below threshold — defined as it will be known
  at the end of the course.
- **Prediction time**: e.g. end of week 3 of a 12-week course. Only data available
  *by then* may be used. Early prediction is useful but less accurate; report
  performance by week.
- **Unit**: student × course enrolment.

## 3. Feature engineering
- Activity counts and time-on-platform per week (time-on-task estimates from logs are
  crude — sessions with long gaps need a cut-off, e.g. 30 min).
- Regularity/procrastination: days active, time between resource release and first
  access, assignment submission lead time.
- Assessment-related: early quiz scores, late submissions.
- Course-relative features (z-score within course) — raw clicks are not comparable
  across courses with different designs.
- Prior attainment and enrolment variables (powerful, but see fairness below).

## 4. Validation without leakage
- **Temporal / cross-cohort validation**: train on earlier cohorts, test on a later one
  (Gardner & Brooks). Random k-fold within the same term overstates performance when
  courses change.
- Leakage sources: features computed over the full term, final-grade-linked actions
  (e.g. accessing the exam page), withdrawal-date-dependent activity drops.
- Baselines: prior GPA alone, or a simple logistic regression; if gradient boosting
  (XGBoost) or random forests barely beat them, say so.
- Metrics: AUC plus **precision/recall at the intervention capacity** (if advisors can
  contact 50 students, how many of the top 50 really are at risk?) and **calibration**
  (predicted vs observed risk).

## 5. Fairness and use
- Audit performance (AUC, false-negative/positive rates, calibration) across gender,
  ethnicity, first-generation, disability and socio-economic groups (Baker & Hawn).
- Including demographic variables can improve accuracy yet encode structural bias; test
  models with and without them and report trade-offs.
- Predictions influence behaviour: a "high-risk" flag can stigmatise students or lower
  expectations. Research the intervention (ideally an RCT of the alert) — prediction
  accuracy alone shows nothing about benefit.
- Dashboard studies: evaluate whether teachers/students interpret and act on the
  displays, not just usability.

## Gotchas
- Activity ≠ learning: high clicks can mean confusion.
- Courses using external tools (publisher platforms, video hosts) have invisible activity.
- Log formats change with LMS upgrades; document versions and extraction scripts.
- Uncertain: the Moodle table name and Canvas data products change across versions; check
  your instance's documentation.

## Verify
- [ ] Ethics/data-protection approval and transparency plan in place before extraction.
- [ ] Prediction time fixed; every feature uses only data available by then.
- [ ] Tested on a later cohort; compared against a simple prior-attainment baseline.
- [ ] Precision at intervention capacity and calibration reported.
- [ ] Subgroup fairness audit reported; intervention effects not inferred from accuracy.
