---
id: computing-software.database-administration.cloud-nosql-databases.firestore-rules-authentication-and-ownership
name: firestore-rules-authentication-and-ownership
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-rules-authentication-and-ownership, firestore-security-rules, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Write rules that authorise by request.auth and document data."
sources:
  - https://firebase.google.com/docs/firestore/security/get-started
  - https://firebase.google.com/docs/firestore/security/rules-query
  - https://firebase.google.com/docs/firestore/security/rules-conditions
  - https://firebase.google.com/docs/firestore/security/insecure-rules
  - https://firebase.google.com/docs/firestore/quotas
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rules for authentication and ownership

**Goal:** Write rules that authorise by request.auth and document data.

## Steps
- Skeleton: rules_version = '2'; service cloud.firestore { match /databases/{db}/documents { match /users/{uid} { allow read, write: if request.auth != null && request.auth.uid == uid; } } }
- Server client libraries bypass Security Rules and authenticate through IAM, so rules protect only client access.
- Rules are not filters: a query must be provably within the rules, so include the same constraint in the query (where uid == auth.uid).
- Use get() and exists() to read other documents (each is a billed read; the limit is 10 access calls for single-document and query requests and 20 for multi-document reads, transactions and batched writes).

## Gotcha
Open rules such as allow read, write: if true let anyone who guesses your project ID read, modify or delete the data once the app is deployed.

## Verify
- [ ] Emulator unit tests deny unauthenticated and cross-user access and allow owner access.

## Checked

2026-11-03. Confirmed on the rules structure, Securing queries (rules are not filters), conditions, Fix insecure rules and Usage and limits pages (rules_version 2, request.auth.uid pattern, query constraints, 10 and 20 access-call limits, open-access risk, server libraries bypass rules). Removed: the custom-claims example and the 30-day test-mode expiry, which the pages do not state.

Method: documentation only; no commands were run.
