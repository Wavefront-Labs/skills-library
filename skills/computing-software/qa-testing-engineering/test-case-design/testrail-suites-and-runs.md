---
id: computing-software.qa-testing-engineering.test-case-design.testrail-suites-and-runs
name: testrail-suites-and-runs
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [testrail, test-management-tools, test-case-management, test-runs, test-plans-milestones, testrail-api]
level: practitioner
status: docs-checked
description: "Organise test cases in TestRail: projects, sections, suites, test runs with default statuses, milestones, and test plans with configurations, per the TestRail user guide."
sources:
  - https://support.testrail.com/hc/en-us/articles/7076810203028-Introduction-to-the-TestRail-API
  - https://support.testrail.com/hc/en-us/categories/7076541806228-Test-Cases
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TestRail: suites, runs and plans

**Goal:** a test repository that supports planning, execution tracking and reporting without duplicating work.

## Structure
- **Project** per real software project you want to manage; test runs, results and milestones all belong to a project.
- **Test case**: description of prerequisites, a list of steps, and the expected result; ideally verifiable by a single tester in a short period of time.
- **Sections and sub-sections** group test cases, often by module or area of the product. For many cases in one module, break sections down into sub-sections by feature; cases that verify one dialog or page belong in one section.
- **Test suite** is the plan of how the application is tested; a **test run** is an actual test you are conducting against a suite.
- **Milestones** (a planned release, an internal test version, a beta for a customer) can have test runs assigned, so progress is tracked separately per milestone.
- **Test plans** start several runs at once for different **configurations** (operating systems, browsers). Create one with Add Test Plan on the Test Runs & Results page and choose configurations with Select Configurations on a run.

## Running
- Start multiple runs of one suite over time (for example one per release), or several active at once for different configurations.
- When starting a run you can include all cases, select specific cases, or set a dynamic filter on case values.
- Default test statuses: Untested, Passed, Failed, Retest, Blocked. A test that has received a result can never go back to Untested.
- Tests can be assigned to users (to-do lists) with email notifications; the run and milestone pages offer status, activity and progress views, and a Reports area exists.
- A closed run cannot be edited, and later changes to case attributes do not apply to it, so closing archives the run.

## Automation results
TestRail has an API Manual with use-case articles including "Importing test results" and "Exporting test results", and language bindings (Java, PHP, Python, Ruby). Take endpoint names, status ids and the CLI options from those pages; this skill does not restate them.

## Gotchas
- Duplicating cases per release bloats the repository; reuse cases and start a new run per release instead.

## Verify
The milestone page shows its runs with progress, and runs for each configuration exist under the test plan.

## Checked
Date: 2026-11-08
Read in full: the cited support article (actually titled "Introduction to TestRail": dashboard, test cases and sections, test runs and tests, projects, milestones, test plans and configurations, to-dos, tracking) and the API Manual category page (headings only).
Confirmed: all structure and run behaviour above, including the five default statuses and the Untested rule, case selection options, closed-run behaviour.
Removed: the curl example, `add_results_for_cases` endpoint, numeric status ids, `trcli` command line, the "single suite with sections (recommended mode)" claim and the named case templates ("Test Case (Steps)", "Exploratory Session"): none appear on the cited pages. The API article cited is the product introduction, not API reference, so API specifics are pointed at the API Manual instead of stated.
Method: documentation only; no commands were run.
