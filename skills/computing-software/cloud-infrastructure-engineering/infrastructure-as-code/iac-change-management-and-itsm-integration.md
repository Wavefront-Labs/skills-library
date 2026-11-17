---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.iac-change-management-and-itsm-integration
name: iac-change-management-and-itsm-integration
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac-fundamentals, itsm-integration, change-ticket, servicenow]
level: practitioner
status: draft
description: "Integrate IaC pipelines with change management: standard vs normal changes, automatic ticket creation and closure from CI or AAP, change windows and audit evidence."
sources: ["ITIL 4 change enablement practice (https://www.axelos.com/certifications/itil-service-management)", "servicenow.itsm collection - change_request module (https://docs.ansible.com/ansible/latest/collections/servicenow/itsm/change_request_module.html)", "AWS Well-Architected - change management (https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/change-management.html)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Change management and ITSM integration

IaC makes changes reviewable and repeatable, which lets most infrastructure changes become **standard changes** (pre-approved) instead of CAB items.

## Classify
| Change type | IaC example | Approval |
|---|---|---|
| Standard (pre-approved) | merge of a reviewed PR to a module-backed stack, patch playbook run | PR review + pipeline gates |
| Normal | new network segment, DB engine upgrade | CAB/approver in the ticket, plan attached |
| Emergency | hotfix during incident | post-implementation review |

## Automate the ticket
```yaml
- name: Open change request
  servicenow.itsm.change_request:
    instance: "{{ snow_instance }}"
    type: standard
    state: new
    template: "Infrastructure - IaC standard change"
    short_description: "Deploy {{ release }} to {{ env }}"
    description: "{{ lookup('file', 'plan.txt') | truncate(3000) }}"
  register: chg
  delegate_to: localhost

- name: ... run the change ...

- name: Close change
  servicenow.itsm.change_request:
    instance: "{{ snow_instance }}"
    number: "{{ chg.record.number }}"
    state: closed
    close_code: successful
    close_notes: "Pipeline {{ lookup('env','CI_PIPELINE_URL') }}"
  delegate_to: localhost
```
Same idea in GitHub/GitLab: a pipeline job creates the change, waits for approval state (`state: scheduled`/`implement`), runs, closes with outcome.

## Gates
- Block apply outside change windows: check the ticket's planned start/end in a preflight task.
- Link evidence: PR URL, plan/check output, pipeline run, job ID in AAP.
- Failed runs close the change as unsuccessful and trigger a problem record automatically.

## Gotchas
- Do not paste secrets or full diffs with credentials into tickets.
- Manual "rubber-stamp" CAB on every IaC PR adds latency without safety; invest in automated gates and use CAB for genuinely risky changes.

## Verify
- [ ] Every production apply has a linked change record with plan, approver and outcome.
