---
id: computing-software.devops-ci-cd.concourse-ci.secret-redaction
name: secret-redaction
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [redaction, secrets, build-logs, credentials, load-var, leaks, set-x]
level: practitioner
status: docs-checked
description: "Understand how Concourse redacts credential values from build logs, line by line, which values it tracks, what changed in v8, and why set -x still leaks."
sources:
  - https://concourse-ci.org/docs/operation/creds/redacting/
  - https://concourse-ci.org/docs/vars/
  - https://concourse-ci.org/docs/steps/load-var/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Concourse tracks the credential values used in a build, whether pipeline secrets or values from a `load_var` step, and when writing logs to the database replaces each occurrence with `((redacted))`.

Prior to v8, redaction was off by default; on older versions set `CONCOURSE_ENABLE_REDACT_SECRETS=true` on the web node.

The documented example task runs `echo $SECRET > some-file` and `sha1sum some-file`, with `SECRET: ((some-var))` as a task param and `set -x`. With `some-var` as `hello` the log shows `+ echo ((redacted))`. The page notes that `set -x` is the root cause of many accidental credential leaks, since it echoes expanded commands.

If the secret is multi-line, such as `hello\ngoodbye`, and the variable is unquoted in `echo`, the shell squashes lines into arguments and the log shows `+ echo ((redacted)) ((redacted))`. This could have confused redaction, but Concourse redacts line by line, so it remains safe. That also helps with JSON-marshalled credentials, which contain `\n` in a string literal.

Redaction is a safety net: the page says to think of it as an airbag, not a seatbelt. The right fix is not printing secrets in the first place. A `dummy` var source can be used to get redaction for sensitive values when you have no credential manager. Setting `reveal: true` on `load_var` allows a value to show in logs.

## Checked

2026-11-04. Behaviour, version note and examples confirmed on the Redacting credentials page; dummy source on the Vars page; reveal on the Load Var page.

Method: documentation only; no commands were run.
