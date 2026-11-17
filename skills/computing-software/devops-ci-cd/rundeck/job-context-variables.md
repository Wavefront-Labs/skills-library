---
id: computing-software.devops-ci-cd.rundeck.job-context-variables
name: job-context-variables
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, context-variables, rd-environment-variables, inline-script-expansion, job-variables]
level: practitioner
status: docs-checked
description: "Use Rundeck job, node and option context variables in commands, inline scripts and environment variables, with the three syntaxes and their scope limits."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/jobs/job-variables.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three syntaxes for the same variables:
- Command steps, script arguments, job reference arguments, config fields: `${job.name}`
- Inline script content: `@job.id@`. Not available in Script File steps, because those files are not rewritten. Expansion can be disabled in `framework.properties`.
- Environment: uppercase, punctuation to underscore, prefix `RD_`, so `${option.myoption}` becomes `$RD_OPTION_MYOPTION`.

Job context (global scope): `job.name`, `job.group`, `job.id`, `job.execid`, `job.url`, `job.project`, `job.loglevel`, `job.user.name`, `job.user.email`, `job.executionType` (`user`, `scheduled`, `user-scheduled`), `job.retryAttempt`, `job.wasRetry`, `job.threadcount`, `job.filter`, `job.outputfilepath`.

Node context (per node): `node.name`, `node.hostname`, `node.username`, `node.description`, `node.tags` (comma separated), `node.os-name`, `node.os-version`, `node.os-arch`, `node.os-family`, plus any custom attribute as `node.<attr>`.

Options: `option.NAME` from the GUI, API or webhook.

Gotcha: the conditional logic page shows `${node.osFamily}` while this reference lists `node.os-family`. Use the hyphenated name from this reference and confirm in a debug run.

Verify:

```bash
echo "Job $RD_JOB_NAME exec $RD_JOB_EXECID on ${node.name}"
```

Run it and check the execution log shows resolved values, not literal `${...}`.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Job Variables Reference: the three syntaxes, the Script File exception and framework.properties switch, RD_ environment transformation, job.* and node.* variable lists (including node.os-family), executionType values, and option.NAME. The osFamily vs os-family gotcha compares this page with the Conditional Logic page, both read in this batch. Nothing removed.

Method: documentation only; no commands were run.
