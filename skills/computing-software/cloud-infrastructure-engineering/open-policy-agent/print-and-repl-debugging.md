---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.print-and-repl-debugging
name: print-and-repl-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [debugging, repl, print-builtin, playground, debug-adapter]
level: practitioner
status: docs-checked
description: "Debug Rego with the print built-in, the opa run REPL loaded with policy and data, the Rego Playground, and the line-by-line debug adapter."
sources:
  - https://www.openpolicyagent.org/docs/debugging
  - https://www.openpolicyagent.org/docs/cheatsheet
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: shorten the feedback loop while writing a policy.

REPL, loaded with the files you are working on:

```
opa run [policy-files] [data-files]
```

Query rules directly at the prompt.

`print` writes values to stdout during evaluation. It also shows how many times a line executes:

```rego
allow if {
    some user in allowed_users
    print(user)
    input.user == user
}
```



Rego Playground (play.openpolicyagent.org) is a web environment for testing policy with different inputs and data. The docs say it can be used to share a policy and data with others when asking for help in the OPA Slack.

Live debugging: the Debug Adapter, built on OPA's Debug API, lets supported editors step through Rego line by line with breakpoints, variable inspection and print output. Supported editors are listed on the Regal editor support page.

For runtime errors rather than wrong results, use rego-error-tracebacks. For slowness, use profiling from the Policy Performance page.

Check: add `print` to a rule, run `opa eval -d policy.rego 'data.example.allow'` and confirm printed values appear on stdout for each iteration.

## Checked

2026-11-04. Confirmed against the OPA docs Debugging page: live debugging with the Debug Adapter built on OPA's Debug API (breakpoints, variable inspection, print statements, editors listed on the Regal Editor Support page), the opa run REPL loaded with policy and data files, the Rego Playground, the print built-in (stdout, execution counts), and the pointer to Policy Performance for profiling. Removed the unsupported claim about re-loading after edits and softened the Slack share-link claim to what the page says. The page's traceback section covers runtime errors (see rego-error-tracebacks). The Check line is a suggested exercise, not a documented example.

Method: documentation only; no commands were run.
