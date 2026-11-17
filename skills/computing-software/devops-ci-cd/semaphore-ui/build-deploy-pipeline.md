---
id: computing-software.devops-ci-cd.semaphore-ui.build-deploy-pipeline
name: build-deploy-pipeline
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [build, deploy, artifact-version, semaphore-vars, pipeline, semaphore-ui]
level: practitioner
status: docs-checked
description: "Create a Build template that versions an artifact and a Deploy template that ships a chosen version."
sources:
  - https://semaphoreui.com/docs/user-guide/task-templates/build-deploy
  - https://semaphoreui.com/docs/user-guide/task-templates/build-deploy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Build and deploy templates

Goal: a simple versioned pipeline inside Semaphore.

Build templates produce an artifact (tarball, image, package). Each build task gets an auto-incremented version starting at the template's Start Version. Use `semaphore_vars.task_details.target_version` in the playbook to name the artifact.

Deploy templates link to a build template through Build Template. The New Task dialog asks for the Build Version (the latest successful build is preselected). Enable Autorun to start a deploy automatically after every successful build; the version to deploy is in `semaphore_vars.task_details.incoming_version`.

Every Ansible run gets the `semaphore_vars` variable. Example for a build:

```yaml
semaphore_vars:
  task_details:
    type: build
    username: user123
    message: New version of some feature
    target_version: 1.5.33
```

Use it to learn the task type, version, who started it and the message.

Steps:
1. Create the Build template and set Start Version (for example 1.0.0).
2. Create the Deploy template and choose the build template.
3. Run Build, then Deploy and pick the version.

Gotchas:
- For Bash, PowerShell and Python templates the same values arrive as environment variables such as `SEMAPHORE_TASK_DETAILS_TYPE`, `SEMAPHORE_TASK_DETAILS_TARGET_VERSION` and `SEMAPHORE_TASK_DETAILS_INCOMING_VERSION`.
- Multi-step pipelines with approvals use Workflows instead.

Verify: the template list shows the latest build version.

## Checked

2026-11-04: checked against the build and deploy templates page. Added the documented incoming_version variable and the SEMAPHORE_TASK_DETAILS_* environment variables; removed unconfirmed gotchas about version formats and script apps.

Method: documentation only; no commands were run.
