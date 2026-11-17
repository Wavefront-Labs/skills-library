---
id: computing-software.devops-ci-cd.concourse-ci.task-step-config-file-vars-params
name: task-step-config-file-vars-params
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [task-step, config, file, image, vars, params, external-task]
level: practitioner
status: docs-checked
description: "Use the task step: inline config versus file from an artifact, the image override, vars (templating) versus params (environment variables)."
sources:
  - https://concourse-ci.org/docs/steps/task/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `task` step runs a task. Its name is only a label shown in the web UI. Outputs listed in the task config are registered as artifacts for later steps.

- `config`: an inline task config (`platform`, `image_resource`, `run` and so on).
- `file`: a path to a task config `.yml`, whose first path segment must be an artifact from earlier in the plan, so the config can live in a repo you `get`. The file may contain `((vars))`, filled from the step `vars` or a credential manager.
- `image`: names an artifact (for example from a `get` of a `registry-image` resource) to use as the container image. It overrides `image_resource` in the config, which lets you build an image once and use it throughout the pipeline with a consistent set of dependencies.
- `vars`: template variables for an external task file. Not environment variables. They can also re-map credential-manager names, e.g. `my-var: ((var-from-vault))`.
- `params`: environment variables, overriding those declared in the task config or file. The task file can declare defaults, for example `ECHO_ME: "default text"`, and params may themselves be `((vars))`.

```yaml
- task: constrained-task
  file: ci/tasks/print-param.yml
  params:
    ECHO_ME: "Eat your fruits"
```

The difference: `vars` interpolates any template placeholder in the external file, while `params` overwrites declared task parameters specifically.

## Checked

Checked 2026-11-09 against the raw docs source of the Task Step page (read in full): config, file, image, vars and params semantics and examples all match.

Method: docs-checked 2026-11-09 against concourse docs task step page (github.com/concourse/docs source); documentation only, no commands were run.
