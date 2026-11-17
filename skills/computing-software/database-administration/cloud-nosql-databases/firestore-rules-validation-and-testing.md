---
id: computing-software.database-administration.cloud-nosql-databases.firestore-rules-validation-and-testing
name: firestore-rules-validation-and-testing
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-rules-validation-and-testing, firestore-security-rules, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Validate data in rules and test them in the emulator."
sources:
  - https://firebase.google.com/docs/firestore/security/get-started
  - https://firebase.google.com/docs/firestore/security/rules-fields
  - https://firebase.google.com/docs/rules/unit-tests
  - https://firebase.google.com/docs/firestore/security/rules-structure
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validation, functions and testing

**Goal:** Validate data in rules and test them in the emulator.

## Steps
- Validate fields: allow create: if request.resource.data.keys().hasAll(['title','uid']) && request.resource.data.keys().hasOnly(['title','uid']); for updates, request.resource.data.diff(resource.data).affectedKeys().hasOnly([...]) limits which fields change.
- Reuse logic with function isOwner(uid) { return request.auth.uid == uid; }.
- Test with @firebase/rules-unit-testing: initializeTestEnvironment, authenticatedContext('alice'), assertSucceeds/assertFails.
- Deploy with firebase deploy --only firestore (rules and indexes).

## Gotcha
Rules apply to client access only; the server client libraries bypass rules and rely on IAM.

## Verify
- [ ] CI runs the rules test suite against the emulator and fails on any regression.

## Checked

2026-11-03. Confirmed on the Security Rules and fields, rules structure and Firebase unit-testing pages (keys().hasAll and hasOnly, affectedKeys(), functions, initializeTestEnvironment, authenticatedContext, assertSucceeds, assertFails, firebase deploy --only firestore, server libraries bypass rules). Removed: the is string and size() type checks and the firestore:rules deploy target, which the pages do not show.

Method: documentation only; no commands were run.
