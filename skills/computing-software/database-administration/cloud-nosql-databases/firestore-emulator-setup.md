---
id: computing-software.database-administration.cloud-nosql-databases.firestore-emulator-setup
name: firestore-emulator-setup
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-emulator-setup, firestore-emulator, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Run Firestore locally for development and tests."
sources:
  - https://firebase.google.com/docs/emulator-suite
  - https://firebase.google.com/docs/emulator-suite/connect_firestore
  - https://firebase.google.com/docs/emulator-suite/install_and_configure
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Emulator setup

**Goal:** Run Firestore locally for development and tests.

## Steps
- firebase init emulators then firebase emulators:start --only firestore; the default Firestore emulator port is 8080 (change it in firebase.json).
- Connect: connectFirestoreEmulator(db, '127.0.0.1', 8080) in the web SDK; admin SDK uses FIRESTORE_EMULATOR_HOST.
- Import and export data between runs with firebase emulators:start --import=./seed --export-on-exit (this also works with emulators:exec).
- The emulator exposes a REST endpoint at http://localhost:8080/v1 for the database.

## Gotcha
The emulator does not track compound indexes and runs any valid query, so test against a real Firestore instance to find the indexes you need.

## Verify
- [ ] Tests run offline against the emulator and clean data between tests with an HTTP DELETE to /emulator/v1/projects/<project_id>/databases/(default)/documents.

## Checked

2026-11-03. Confirmed on the Connect your app to the Firestore emulator and Install, configure and integrate the Emulator Suite pages (port 8080, connectFirestoreEmulator, FIRESTORE_EMULATOR_HOST, --import and --export-on-exit, REST endpoint, clear-documents DELETE endpoint, no compound index tracking). Removed: the auth emulator in the start command, the UI and rules-evaluation claim, and the unsourced quota and billing statement.

Method: documentation only; no commands were run.
