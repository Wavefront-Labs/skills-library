---
id: computing-software.rpa-and-low-code.uipath.uipath-reframework-state-machine
name: uipath-reframework-state-machine
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-reframework, uipath-reframework-state-machine]
level: advanced
status: draft
description: "Use the Init, Get Transaction Data, Process and End states."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Understand the REFramework states
**Goal:** Use the Init, Get Transaction Data, Process and End states.

- REFramework is a transactional state machine template: Init, Get Transaction Data, Process Transaction, End Process.
- Retry logic is driven by MaxRetryNumber and queue retries.
- Put business logic in Process.xaml, not in the framework files.

## Gotchas
- Editing framework internals makes upgrades hard.

## Self-check
Template runs a sample queue to completion.
