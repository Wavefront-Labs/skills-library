---
id: computing-software.cloud-infrastructure-engineering.ansible.controller-schedules-and-notifications
name: controller-schedules-and-notifications
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, awx, automation-controller, schedules, rrule, notifications, notification-templates, slack-notification, email-notification, webhook-notification, pagerduty, mattermost, teams-webhook, grafana, irc, twilio, custom-messages, approval-notifications, management-jobs, cleanup-jobs, drift-schedule, compliance-schedule]
level: practitioner
status: docs-checked
description: "Schedule AWX/controller jobs with RRULE (timezones, exceptions), run management cleanup jobs, and wire Slack/email/webhook/PagerDuty notification templates with custom messages."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/using_automation_execution/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/configuring_automation_execution/", "https://legacy-controller-docs.ansible.com/automation-controller/latest/html/controllercli/", "https://github.com/redhat-cop/infra.aap_configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller schedules and notifications

**Goal:** drift checks, patching and reports run themselves on a calendar that
respects timezones and freeze windows, and the right people hear about failures
and pending approvals — from the controller, not from someone watching a screen.

## 1. Schedules
A schedule belongs to a job template, workflow, project (sync) or inventory source (sync).
Fields: name, start date/time, **local time zone**, repeat frequency (none, minute, hour, day,
week, month, year) with interval, days/weekdays, end (never, after N, on date), and prompted
values (extra vars, limit, inventory, credentials, job type) if the template allows prompting.
Underneath it is an iCalendar **RRULE** (the `awx.awx.schedule_rrule` lookup can generate them;
the awx.awx collection needs PyPy/pytz support in the EE). The schedule Details tab lists the
next occurrences in the selected local time zone.
```
DTSTART;TZID=Europe/London:20260105T020000 RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR;INTERVAL=1
DTSTART;TZID=UTC:20260101T000000 RRULE:FREQ=MONTHLY;BYMONTHDAY=1;COUNT=12
```
Complex rules (exceptions for freeze dates) are API-only; `awx schedules create` accepts a rule.
Toggle **Enabled** to pause without deleting.

Useful recurring jobs: nightly `--check` drift run (job type Check, notify on changed hosts
via a custom message or a `set_stats` + follow-up), weekly patching workflow with approval,
hourly inventory syncs (or `update on launch` instead), daily compliance report.

## 2. Management jobs
Built-in templates under Administration → Management Jobs: *Cleanup Job Details* (job events/stdout
older than N days — default 120 days, weekly — the big one for DB size), *Cleanup Activity Stream*,
*Cleanup Expired Sessions*. Schedule them on day one (each takes "days of data to keep").
Without them the job event data grows unbounded and the UI slows.

## 3. Notification templates
Create once per channel in an org, attach to objects for the events you want:
| Type | Needs |
|---|---|
| Slack | bot token, channels (`#deploys`), optional per-event colour |
| Email | SMTP host/port/TLS, sender, recipients |
| Webhook | URL, headers (auth), HTTP method POST/PUT; the body is the job JSON or a custom message |
| PagerDuty | integration key, client name, subdomain |
| Grafana / IRC / Mattermost / Rocket.Chat / Twilio | see the notification template docs for each type's fields |
Attach points: job template / workflow template (start, success, failure and **approval** for
workflow nodes), project, or entire organizations. Approval notifications go out when an approval
node is reached, approved, denied or times out.

Custom messages (Jinja over the job context) per event:
```
{{ job.name }} #{{ job.id }} {{ job.status }} on {{ job.summary_fields.inventory.name }} — {{ url }}
hosts failed: {{ job.summary_fields.hosts | selectattr('failed') | map(attribute='hostname') | join(', ') }}
```
Custom messages can reference the job context (name, status, timestamps, inventory and host
summaries). Message bodies for webhooks must be valid JSON if the receiver expects it — build it
in the custom message body.

Test with the bell icon on the notification template (sends a test event). Notification
history: `awx notifications list`.

## 4. Automate
```yaml
- infra.aap_configuration.controller_notification_templates:
    name: slack-deploys
    organization: platform
    notification_type: slack
    notification_configuration: {token: "{{ vault_slack_token }}", channels: ["#deploys"]}
    messages:
      success: {message: "{{ '{{' }} job.name {{ '}}' }} succeeded — {{ '{{' }} url {{ '}}' }}"}
- infra.aap_configuration.controller_schedules:
    name: nightly-drift
    unified_job_template: "site (check)"
    rrule: "DTSTART;TZID=Europe/London:20260105T020000 RRULE:FREQ=DAILY"
    job_type: check
    enabled: true
- infra.aap_configuration.controller_job_templates:
    name: app-a deploy (prod)
    notification_templates_started: [slack-deploys]
    notification_templates_success: [slack-deploys]
    notification_templates_error: [slack-deploys, pagerduty-platform]
```
(Escape Jinja in custom messages when the config itself is an Ansible playbook.)

## 5. Operate
- Freeze windows: disable the schedule (automate it with a tiny job that flips `enabled`), or add `EXDATE`s.
- Missed runs while the controller was down are not replayed; the next occurrence runs.
- Schedules on a template with `concurrent jobs` off queue behind long-running instances; a daily check that takes 26 hours silently stacks.
- Notifications go out from the controller's task pods; outbound proxy/firewall must allow Slack/SMTP.

## Gotchas
- A schedule created in the UI stores the browser's timezone unless you set it; daylight-saving shifts are handled by `TZID`, not by UTC offsets — never use `DTSTART` in UTC for "2 am local" jobs.
- `COUNT` and `UNTIL` are mutually exclusive in RRULE; the API rejects both.
- Notification failure (bad token) does not fail the job; check notification history with
  `awx notifications list`.
- Email notification templates with many recipients are rate-limited by your SMTP relay; use a list address.
- Custom message templates run with sandboxed Jinja: no filters beyond the basics, no lookups.
- Org-level notifications fire for **every** job, including inventory syncs — noisy; prefer template-level.

## Verify
- [ ] `POST /api/v2/schedules/preview/` with your RRULE lists the intended next five runs in the right local times across a DST change.
- [ ] The test button on each notification template delivers; a deliberately failed job pages/posts with the custom message rendered.
- [ ] Management job schedules exist and `Cleanup Job Details` has run (job events older than the retention are gone).

## Checked

- 2026-10-31: schedule fields (start date/time, time zone, repeat frequency, prompted values),
  UTC scheduling with local-time-zone display and DST drift, management jobs (Cleanup Job Details
default 120 days weekly, Cleanup Activity Stream, Cleanup Expired Sessions with days-of-data
schedules), notification types (Email, Grafana, IRC, Mattermost, PagerDuty, Rocket.Chat, Slack,
Twilio, Webhook), notification events (job start, success, failure, approval) at template/project/organization
level, customizable messages, `awx schedules create` and `awx notifications list` confirmed in
AAP 2.5 Using automation execution / Configuring automation execution and the AWX CLI reference.
  `controller_notification_templates`/`controller_schedules`/`controller_job_templates` role names
  confirmed in the redhat-cop roles listing.
- Removed: the `POST /api/v2/schedules/preview/` endpoint, the EXRULE/EXDATE example, the schedule
  creator/RBAC claim and the custom-message variable list (`job_friendly_name` etc.); the Microsoft
  Teams/Matrix row was folded into the documented type list.
Method: documentation only; no commands were run.
