---
id: computing-software.devops-ci-cd.rundeck.mask-passwords-log-filter
name: mask-passwords-log-filter
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, mask-passwords, log-filter, secure-option, replacement-text]
level: intro
status: docs-checked
description: "Hide secure option values in Rundeck job logs by attaching the Mask Passwords log filter to the steps that might print them."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/log-filters/mask-passwords.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Mask Passwords log filter hides the value of any job option whose Input Type is Secure or Secure Remote Authentication wherever it appears in step output.

Settings:
- Replacement: text shown in place of the value. Default `[SECURE]`.
- Color: an ANSI colour for the replacement.

Usage: define the job option with Input Type Secure (or Secure Remote Authentication), then always apply this filter to the job steps that may output the values of those options.

Verify by running the job and checking the log shows the replacement text instead of the secret.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Mask Passwords: masks Secure and Secure Remote Authentication option values, Replacement default [SECURE], Color ANSI pulldown, and the recommendation to apply it to steps that may output those values. Removed the step-by-step UI editing instructions and the per-step gotcha, which the page does not state.

Method: documentation only; no commands were run.
