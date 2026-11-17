---
id: computing-software.rpa-and-low-code.uipath.uipath-try-catch-rethrow
name: uipath-try-catch-rethrow
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-exception-handling, uipath-try-catch-rethrow]
level: practitioner
status: draft
description: "Catch, log and recover from errors."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use Try Catch, Rethrow and Retry Scope
**Goal:** Catch, log and recover from errors.

- Try Catch with specific exception types before System.Exception; Finally closes resources.
- Retry Scope retries an action a set number of times with an interval.
- Rethrow to let the framework decide.

## Gotchas
- Catch-all with empty body hides failures.

## Self-check
A forced error is logged and handled.
