---
id: computing-software.qa-testing-engineering.test-case-design.error-handling-and-validation-message-testing
name: error-handling-and-validation-message-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [error-handling-testing, error-messages, validation-testing, negative-testing, istqb-ta]
level: practitioner
status: docs-checked
description: "Test error handling: provoke each validation and system error, check message wording, field association, recovery, no data loss and no stack-trace leakage."
sources:
  - https://www.nngroup.com/articles/error-message-guidelines/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error handling and validation message testing

**Goal:** every error the user can trigger is caught, explained in plain language next to the cause, recoverable, and leaks nothing.

## Build the error inventory
List each validation rule (required, format, range, cross-field, uniqueness) and each system failure (timeout, dependency down, 500, offline, session expired). Each is a test.

## Checks per error
- **Detected at the right layer:** client validation is convenience; send the same bad value straight to the API (curl or browser devtools) and confirm the server rejects it with a client-error response.
- **Message quality** (NN/g guidelines): says what went wrong and how to fix it, in user language, no bare codes, no blame. "Enter a date after 01/01/2020" beats "Invalid input".
- **Placement:** next to the field, summary at top for long forms, focus moves to the first error, programmatically associated with the field for screen readers.
- **State preserved:** other fields keep their values after a failed submit; long text survives a session timeout.
- **Recovery:** fixing the field clears the error; retry after a transient failure works without duplicates.
- **No leakage:** no stack traces, SQL, internal hostnames, and identical responses for "user not found" and "wrong password" (account enumeration).
- **Multiple errors at once** are all reported, not one per submit.

## System failures
Stub the dependency to return 500, delay 30 s, or drop the connection (your stub's fault injection, browser offline mode). Expect a friendly message, a logged correlation ID, and no half-saved record.

## Verify
The error inventory has a result per row, and a log search for the test window shows each server-side error logged once with a correlation ID matching the one shown to the user.

## Checked

2026-10-28. Confirmed: NN/g error-message guidelines: highly visible, human-readable language, concise and precise, constructive advice, positive tone without blame. Removed: Specific HTTP codes, aria-describedby and WireMock (not in sources).

Method: documentation only; no commands were run.
