---
id: computing-software.devops-ci-cd.ci-pipeline-design.test-data-management
name: test-data-management
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, test-data-management, test-data, test-isolation, production-data-copy, pii-in-test, subsetting]
level: practitioner
status: docs-checked
description: "Supply tests with data that is available on demand, isolated and free of sensitive production data, following DORA's test data management guidance."
sources: ["https://dora.dev/capabilities/test-data-management/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Test data management

**Goal (DORA):** tests get adequate data, on demand, and test data never limits which
automated tests a team can run.

## 1. Core conditions DORA found in successful teams
- Adequate test data is available to run full automated test suites.
- Test data can be acquired on demand.
- Test data does not limit or constrain the automated tests teams can run.

## 2. Common pitfalls
- Over-reliance on data defined outside the test's scope: unit tests should not depend on
  data or state external to the test. Such reliance makes tests brittle and costly to maintain.
- Using a full copy of the production database instead of the relevant portions.
- Not masking or hashing sensitive data.
- Relying on data that is out of date or no longer relevant.

## 3. Practices DORA lists
- **Favour unit tests.** They are independent of each other and of the rest of the system,
  make up the majority of the pyramid, and need no external data.
- **Minimise test data.** It needs ongoing maintenance as APIs and interfaces change, a cost
  that slows the team.
- **Isolate test data.** Run tests in well-defined environments with controlled inputs and
  expected outputs. Data a test consumes should be explicitly associated with that test and
  not modified by other tests or processes. Where possible, tests create the state they need
  in setup through the application's APIs. Isolation is also a prerequisite for running tests
  in parallel.
- **Minimise reliance on data stored in databases.** Databases persist changes across tests
  unless reset, which hurts isolation and parallelisation, and they are slower to use than
  local data. Favour in-memory databases where appropriate.
- **Make data readily available without a full production copy.** Full copies are risky, slow
  to refresh (so go stale) and may contain sensitive information. Instead, identify the
  sections of data the tests need, export them regularly and make them easy for tests to get.

## 4. Measuring
- Time developers and testers spend managing data for test suites, or survey whether they
  have adequate data.
- Percentage of key data sets available, how often they are accessed and how often refreshed.
- Number of automated tests that can run without acquiring extra data, or survey whether
  data limits testing.

## Verify
- [ ] Any test can run alone and in any order with the same result.
- [ ] No raw production data is in test or staging environments; sensitive fields are masked
  or hashed in any derived data.
- [ ] Test data sets have a refresh routine and an owner.

## Checked
Confirmed 2026-11-09 against the DORA test data management page, read in full from a local text copy.
Removed as unconfirmed: the factory_boy code, faker and per-language factory libraries, deterministic Faker seeds, `.invalid` and `555` conventions, the isolation strategy speed table (transaction rollback, schema per worker, Postgres template databases, Testcontainers), idempotent seed scripts and the golden dataset personas, the production-derived data pipeline (Jailer, pg_sample, Tonic, Presidio, Macie, hashing recipes, scanner sign-off), the pipeline wiring section, the pseudonymisation legal claim, and the grep check. Humble and Farley chapter 12 and the Faker, factory_bot, GitLab and PostgreSQL sources were never read and were dropped from `sources`.
Method: docs-checked 2026-11-09 against dora.dev/capabilities/test-data-management
