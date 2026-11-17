---
id: computing-software.database-administration.cloud-nosql-databases.firestore-emulator-rules-testing-ci
name: firestore-emulator-rules-testing-ci
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-emulator-rules-testing-ci, firestore-emulator, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Automate rule tests."
sources:
  - https://firebase.google.com/docs/emulator-suite
  - https://firebase.google.com/docs/rules/unit-tests
  - https://firebase.google.com/docs/firestore/security/test-rules-emulator
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rules testing in CI

**Goal:** Automate rule tests.

## Steps
- Use initializeTestEnvironment from @firebase/rules-unit-testing with a projectId and firestore: { rules: fs.readFileSync('firestore.rules', 'utf8') }.
- Use testEnv.withSecurityRulesDisabled to seed data, and authenticatedContext(uid, tokenOptions) or unauthenticatedContext() for the cases under test. Clear data between tests with clearFirestore().
- Run in CI with firebase emulators:exec --only firestore "<your test command>", which starts the emulator, runs the command, then shuts the emulator down.
- After a run, fetch the rules coverage report from http://localhost:8080/emulator/v1/projects/<project_id>:ruleCoverage.html (or :ruleCoverage for JSON).

## Gotcha
Admin SDK and server-library access bypasses Security Rules, so tests that use it prove nothing about rules.

## Verify
- [ ] CI fails when a rule change allows an unintended access.

## Checked

2026-11-03. Confirmed on the Firebase unit-testing rules page (initializeTestEnvironment, withSecurityRulesDisabled, authenticatedContext, unauthenticatedContext, clearFirestore, assertSucceeds, assertFails) and the Test Firestore Security Rules with the Emulator page (emulators:exec, default port 8080, ruleCoverage endpoints). Removed: the placeholder npm test command.

Method: documentation only; no commands were run.
