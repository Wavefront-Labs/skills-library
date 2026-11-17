---
id: computing-software.devops-ci-cd.rundeck.job-resume-plugin
name: job-resume-plugin
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, job-resume, resumable-plugin, workflow-state, resume-on-retry]
level: advanced
status: docs-checked
description: "Resume a failed Rundeck execution from the failed step with the Resumable execution plugin (Enterprise): requirements, secure option caveats and limits."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/jobs/job-resume.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Resumable plugin (Enterprise) records workflow state as the execution runs. After a failure you can resume, starting a new execution at the failed step(s) with the same inputs.

Enable: edit the job, Execution Plugins tab, tick "Resumable". After a failure, "Run Again..." gains a resume item and a confirmation page.

Requirements and caveats:
- Not supported with the Node First strategy. Works with Sequential; Parallel and Ruleset are beta.
- Do not reorder, add, remove or replace steps before resuming; the plugin compares a snapshot and fails to start if the sequence changed. Editing existing steps should be fine.
- Secure and Secure Remote Authentication option values are not persisted. They are available on resume only if the option has a Storage Path (loaded from Key Storage) or on automatic retry with Resume On Retry checked. Manually entered secure values are not available on a manual resume.

Resume on retry, in job XML:

```xml
<plugins>
  <ExecutionLifecycle type='resume'>
    <configuration data='true'><map><string key='onRetry'>true</string></map></configuration>
  </ExecutionLifecycle>
</plugins>
```

Limits: only top-level steps are tracked (referenced jobs do not resume mid-job); a crash before state is stored prevents resume; manually killed executions cannot be resumed. In clusters the state is a `.resume.json` file in log storage.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Job Resume Plugin (Commercial): purpose, Execution Plugins tab Resumable checkbox, Run Again menu and confirmation page, Node First unsupported, Parallel and Ruleset beta, snapshot comparison rule, secure option caveats and Resume On Retry, the onRetry XML, .resume.json cluster storage, and the three limitations. Nothing removed.

Method: documentation only; no commands were run.
