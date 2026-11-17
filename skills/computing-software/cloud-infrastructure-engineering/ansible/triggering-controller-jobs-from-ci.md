---
id: computing-software.cloud-infrastructure-engineering.ansible.triggering-controller-jobs-from-ci
name: triggering-controller-jobs-from-ci
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ci-pipelines, ci-controller-launch, controller-api, awxkit]
level: practitioner
status: docs-checked
description: "Launch automation controller job templates from CI pipelines with awx CLI, ansible.controller modules or the REST API, wait for completion and surface job output."
sources: ["https://legacy-controller-docs.ansible.com/automation-controller/latest/html/controllercli/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/automation_execution_api_overview/", "https://github.com/redhat-cop/infra.aap_configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Triggering controller jobs from CI

Keep credentials and execution in the controller; CI only asks it to run.

## awx CLI
```bash
pip install awxkit
export CONTROLLER_HOST=https://aap.corp.example.com CONTROLLER_OAUTH_TOKEN=$AAP_TOKEN
awx job_templates launch "Deploy app" \
  --extra_vars '{"release": "'"$CI_COMMIT_TAG"'"}' \
  --limit web_canary --monitor -f human
```
`--monitor` streams output and exits non-zero if the job fails; `--wait` waits silently. For
workflows: `awx workflow_job_templates launch "Release" --monitor`. On AAP 2.5+ the CLI needs
`AWXKIT_API_BASE_PATH=/api/controller/` (the `awx` package installs from `awxkit` on PyPI).

## From Ansible
The certified `ansible.controller` (or upstream `awx.awx`) collections provide job launch and wait
modules — see their docs on console.redhat.com / Galaxy. `infra.aap_configuration` wraps them in the
`controller_job_launch` and `controller_workflow_launch` roles.

## Raw API
```bash
JOB=$(curl -s -H "Authorization: Bearer $AAP_TOKEN" -H 'Content-Type: application/json' \
  -d '{"extra_vars": {"release": "v1.4.2"}}' \
  https://aap.corp.example.com/api/controller/v2/job_templates/42/launch/ | jq .id)
until [[ $(curl -s -H "Authorization: Bearer $AAP_TOKEN" .../api/controller/v2/jobs/$JOB/ | jq -r .status) =~ successful|failed|error|canceled ]]; do sleep 10; done
```
(AAP 2.5 serves the controller API under `/api/controller/v2/`; AWX and AAP 2.4 under `/api/v2/`.)

## Requirements on the template
- Extra vars from CI must be allowed: "Prompt on launch" for variables, or a survey with those variables.
- The token's user needs Execute on the template only.

## Gotchas
- Use an application token scoped to `write` for the CI user; rotate it.
- Fail the pipeline on non-successful status, and link the job URL in CI output.

## Verify
- [ ] Pipeline fails when the controller job fails and prints the job URL.

## Checked

- 2026-10-31: `pip install awxkit`, CONTROLLER_HOST/CONTROLLER_OAUTH_TOKEN and `--conf.host`/
`--conf.token`, `awx job_templates launch --monitor`, `awx workflow_job_templates launch`,
`--wait` and the AWXKIT_API_BASE_PATH=/api/controller/ requirement for AAP 2.5+ confirmed in the
AWX CLI reference (usage/examples). The `/api/controller/v2/` base path and `/api/v2/job_templates/<id>/launch/`
endpoint confirmed in the AAP 2.5 Automation execution API overview and collection docs.
`controller_job_launch`/`controller_workflow_launch` role names confirmed in the redhat-cop roles listing.
- Removed: the `ansible.controller.job_launch`/`job_wait` module example (console.redhat.com module
docs are not fetchable; replaced with a pointer and the confirmed role names).
Method: documentation only; no commands were run.
