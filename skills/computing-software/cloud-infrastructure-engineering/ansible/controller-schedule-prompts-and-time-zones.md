---
id: computing-software.cloud-infrastructure-engineering.ansible.controller-schedule-prompts-and-time-zones
name: controller-schedule-prompts-and-time-zones
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, schedules-notifications, schedule-extra-vars, schedule-prompt, schedule-timezone, dst, rrule]
level: practitioner
status: docs-checked
description: "Create controller schedules that pass extra vars and prompted values (limit, tags, inventory), and write RRULEs with explicit time zones, UTC UNTIL and DST care."
sources: ["https://raw.githubusercontent.com/ansible/awx/devel/docs/schedules.md", "https://raw.githubusercontent.com/ansible/awx/devel/awx_collection/plugins/modules/schedule.py", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/proc-controller-adding-new-schedule.adoc", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/proc-controller-define-schedule-exceptions.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller schedules: prompts and time zones

## Prompted values on a schedule
A schedule can be created for a job template, workflow job template, inventory source, project sync
or management job template. The `awx.awx.schedule` / `ansible.controller.schedule` module accepts
`extra_data`, `limit`, `job_tags`, `inventory` and `enabled` alongside `unified_job_template` and `rrule`.
Values the template does not accept as prompt-on-launch should not be relied on; enable
**Prompt on launch** for each field the schedule sets.

```yaml
- name: Nightly patching of the web tier
  awx.awx.schedule:
    name: patch-web-nightly
    unified_job_template: patch-linux          # job template name
    rrule: "DTSTART;TZID=Europe/London:20261101T020000 RRULE:FREQ=WEEKLY;INTERVAL=1;BYDAY=TU,TH"
    extra_data:
      reboot_allowed: true
      patch_severity: [critical, important]
    limit: web
    job_tags: patch
    inventory: prod
    enabled: true
```
The module documents `extra_data` as a dict; its docs also show building the rrule with the
`awx.awx.schedule_rrule` query plugin (`start_date=`) instead of writing it by hand.

## RRULE rules enforced by AWX
- `DTSTART` is required, must come first, and must carry time zone information (no naive dates).
- UTC: `DTSTART:20300115T120000Z`. Local zone: `DTSTART;TZID=America/New_York:20300115T120000`. Valid zone names are listed by `GET /api/v2/schedules/zoneinfo/`.
- `UNTIL` must always be in UTC (with the `Z` suffix), including when `DTSTART` uses `TZID`.
- Each rule needs `INTERVAL`; `FREQ=SECONDLY`, `BYDAY` with a numeric prefix, `COUNT` together with `UNTIL`, and `COUNT` over 999 are prohibited.
- `RDATE` and `EXDATE` are prohibited. Exclusions use `EXRULE`; in the UI, schedule exceptions use the same format as rules.
- Preview occurrences (next ten, in local and UTC time) with `POST /api/v2/schedules/preview/` and body `{"rrule": "..."}`.

## Time zones and DST
The product documentation states that jobs are scheduled in UTC, that repeating jobs run at a
specific time of day can move relative to a local time zone when Daylight Saving Time shifts, and
that the system resolves the local time to UTC when the schedule is saved. To make sure schedules
are created correctly, the documentation advises setting them in UTC. Preview the rrule and check
the occurrences either side of each DST change.

## Verify
- [ ] The preview endpoint lists the expected local and UTC times.
- [ ] The first run's job shows the extra vars, limit and tags from the schedule.

## Checked

- Date: 2026-11-09. Sources: ansible/awx devel docs/schedules.md and awx_collection schedule.py; ansible/aap-docs main (adding a schedule, schedule exceptions).
- Confirmed: supported resource types; module parameters; DTSTART/TZID rules and zoneinfo endpoint; UTC-only UNTIL; the RRULE limitations list including INTERVAL and EXDATE/RDATE bans; preview endpoint behaviour; UTC scheduling and DST statement and the advice to use UTC.
- Corrected: the example rrule gained the required `INTERVAL`; "EXRULE/EXDATE support varies by version" replaced by the documented EXDATE ban.
- Removed unconfirmed claims: exact behaviour of nonexistent and repeated local times at DST changes, 03:30 maintenance advice, `next_run` field remarks, schedules silently dropping extra_data in some versions, schedules deleted when a template is replaced by config-as-code, the lookup call with `on_days`/`timezone` arguments, workflow approval pairing for change windows, survey-answer requirements, staggering advice.

Method: documentation and module source read from cloned repositories; no commands were run against a controller.
