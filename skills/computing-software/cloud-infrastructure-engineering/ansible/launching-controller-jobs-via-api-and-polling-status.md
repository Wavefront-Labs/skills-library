---
id: computing-software.cloud-infrastructure-engineering.ansible.launching-controller-jobs-via-api-and-polling-status
name: launching-controller-jobs-via-api-and-polling-status
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, automation-controller, awx, controller-api, api-launch, job-polling, rest-api, oauth-token, ci-integration, job-status]
level: practitioner
status: docs-checked
description: "Launch controller job and workflow templates from scripts or CI over the REST API, pass extra vars and limits, poll status with backoff, and fail the pipeline correctly."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/automation_execution_api_overview/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/using_automation_execution/", "https://docs.ansible.com/projects/awx/en/latest/rest_api/filtering.html", "https://github.com/redhat-cop/infra.aap_configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Launching controller jobs via API and polling status

Goal: a CI pipeline or external tool triggers a controller job, waits for it, and passes or fails
with the job's result — without the `awx` CLI installed.

## 1. Token
Create a token for a service user with Execute on the template (UI: User → Tokens, scope Write,
or AAP 2.5 gateway tokens). Store as a CI secret.

## 2. Check what the template accepts
```bash
curl -s -H "Authorization: Bearer $TOKEN" https://controller.example.com/api/v2/job_templates/42/launch/ | jq '{ask_variables_on_launch, ask_limit_on_launch, survey_enabled}'
```
Fields you send at launch are not applied unless the matching prompt-on-launch option is enabled
(documented for extra_vars: only survey variables or `ask_variables_on_launch` are honoured).
On AAP 2.5 the controller API base is `/api/controller/v2/`.

## 3. Launch and poll (bash)
```bash
set -euo pipefail
API=https://controller.example.com/api/v2
resp=$(curl -sf -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "$API/job_templates/42/launch/" \
  -d '{"extra_vars": {"release_tag": "v1.2.3"}, "limit": "web"}')
job=$(echo "$resp" | jq -r .job)
echo "job $job: https://controller.example.com/#/jobs/playbook/$job/output"
delay=5
while :; do
  status=$(curl -sf -H "Authorization: Bearer $TOKEN" "$API/jobs/$job/" | jq -r .status)
  case $status in
    successful) break ;;
    failed|error|canceled) curl -s -H "Authorization: Bearer $TOKEN" "$API/jobs/$job/stdout/?format=txt" | tail -50; exit 1 ;;
  esac
  sleep $delay; [ $delay -lt 30 ] && delay=$((delay*2))
done
```
Statuses: `new`, `pending`, `waiting`, `running`, then `successful`/`failed`/`error`/`canceled`.
Workflows: launch `/workflow_job_templates/<id>/launch/`, response key `workflow_job`, poll
`/workflow_jobs/<id>/`.

## 4. From Ansible instead of curl
The certified `ansible.controller` (or upstream `awx.awx`) collections provide job launch and wait
modules — see their docs on console.redhat.com / Galaxy. `infra.aap_configuration` wraps them in
the `controller_job_launch` role.

## Gotchas
- Launch returns 201 as soon as the job is created; success of the HTTP call says nothing about the job.
- Templates with a password survey question or credentials that prompt on launch need those
  answers in the launch payload.
- Do not poll every second across many pipelines; controller API load grows fast. Backoff to 30 s, or use a webhook/notification to call back.
- Use the template ID or a name lookup (`/job_templates/?name=...`) — names can be duplicated
  across orgs (the API supports field filters).

## Verify
- [ ] Pipeline fails when the job fails (force a failure with a bad limit) and passes on success.
- [ ] Job details show the passed `release_tag` and limit.

## Checked

- 2026-10-31: the `/api/v2/job_templates/<id>/launch/` endpoint (curl examples), job status values
(new, pending, waiting, running, successful, failed, error, canceled), `launch_type` choices,
extra_vars honouring rules (survey variables or ask_variables_on_launch), workflow job templates,
job status/limit fields and field-filter queries confirmed in AAP 2.5 Using automation execution
and the Automation execution API overview. `controller_job_launch` role confirmed in the redhat-cop
roles listing.
- Removed: the `variables_needed_to_start`/`ignored_fields` response keys, the `credential_passwords`
payload key and the `ansible.controller.job_launch`/`job_wait` module example (module docs on
console.redhat.com are not fetchable; replaced with a pointer and the confirmed role name).
Method: documentation only; no commands were run.
