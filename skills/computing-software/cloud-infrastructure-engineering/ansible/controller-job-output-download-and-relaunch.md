---
id: computing-software.cloud-infrastructure-engineering.ansible.controller-job-output-download-and-relaunch
name: controller-job-output-download-and-relaunch
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, automation-controller, awx, job-output, job-stdout, job-output-download, relaunch, relaunch-failed-hosts, job-events, host-summaries]
level: practitioner
status: docs-checked
description: "Read, search, download and relaunch controller jobs: stdout formats via API, job events and host summaries for failures, relaunch on failed hosts, and output retention."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/using_automation_execution/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/configuring_automation_execution/", "https://legacy-controller-docs.ansible.com/automation-controller/latest/html/controllercli/", "https://docs.ansible.com/projects/awx/en/latest/rest_api/filtering.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller job output, download and relaunch

Goal: find why a job failed quickly, hand the output to someone else, and rerun only what failed.

## In the UI
- Output tab: filter by **host**, task, or event type (failed, changed, skipped). Click an event to see the module result JSON.
- Details: launched by, extra vars, scm_revision, EE, instance group, execution node — the facts you need for a postmortem.
- Download icon: full plain-text stdout.

## Via API / CLI
```bash
# plain text, ANSI stripped
curl -s -H "Authorization: Bearer $TOKEN" "https://controller.example.com/api/v2/jobs/1234/stdout/?format=txt" -o job-1234.log
awx jobs stdout 1234 > job-1234.log
# only failed events, with host and task
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://controller.example.com/api/v2/jobs/1234/job_events/?failed=true&page_size=200" \
  | jq -r '.results[] | [.host_name, .task, .event_data.res.msg] | @tsv'
# per-host recap
curl -s -H "Authorization: Bearer $TOKEN" "https://controller.example.com/api/v2/jobs/1234/job_host_summaries/" \
  | jq -r '.results[] | [.host_name, .ok, .changed, .failures, .dark] | @tsv'
```
`dark` = unreachable. Very large outputs are truncated for display (the "Standard Output Maximum
Display Size" and job-event display settings); download the output or use the events endpoint.

## Relaunch
- **Relaunch** (UI): re-runs the most recent job on all hosts or just the failed hosts in the
  inventory; prompts again for anything that was prompted. `launch_type` is recorded as `relaunch`
  (only playbook runs can be relaunched — not project/inventory updates or system jobs).
- Use relaunch-on-failed-hosts after fixing the cause; hosts that succeeded are not touched.
- The relaunched job records `launch_type: relaunch` and links to the original.

## Retention
Job output and events are pruned by the **Cleanup Job Details** system job (default keeps 120
days). Export what audit requires (stdout download or forward job events to a log aggregator
via the logging integration) before it ages out.

## Gotchas
- Relaunch uses the template's *current* project revision, not necessarily the commit the original ran, unless the project is pinned.
- `no_log` tasks show "the output has been hidden" in events too — expected.
- Relaunch requires Execute on the template; users who could only view the job cannot relaunch.

## Verify
- [ ] The jq one-liner lists the same failed hosts as the UI recap.
- [ ] "Relaunch on failed hosts" job's limit contains only those hosts.

## Checked

- 2026-10-31: job status values (new, pending, waiting, running, successful, failed, error,
canceled), `launch_type` choices incl. relaunch, relaunch of playbook runs on all or failed-only
hosts, `awx jobs stdout`/`awx jobs list`, the standard-output display size settings, filtering
(`?field__lookup=`, `not__`, `or__`, `chain__`, related-field filters) and `page_size` max 200
confirmed in AAP 2.5 Using automation execution / Configuring automation execution, the AWX CLI
reference and the AWX REST API filtering page.
- Removed: the `txt_download`/`ansi_download` format enumeration (kept `format=txt` and the download
  behaviour), the `POST /api/v2/jobs/<id>/relaunch/` and `{"hosts": "failed"}` request forms
  (documented UI behaviour is kept), the `STDOUT_MAX_BYTES_DISPLAY` name (replaced with the
documented setting labels) and the `res.msg`/host-summary field specifics.
Method: documentation only; no commands were run.
