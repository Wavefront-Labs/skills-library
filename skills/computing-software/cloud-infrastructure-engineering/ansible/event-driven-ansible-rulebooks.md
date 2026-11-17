---
id: computing-software.cloud-infrastructure-engineering.ansible.event-driven-ansible-rulebooks
name: event-driven-ansible-rulebooks
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, event-driven-ansible, eda, rulebooks, ansible-rulebook, ansible-eda, event-sources, webhook-source, kafka-source, alertmanager-source, prometheus-alerts, conditions, actions, run-job-template, run-playbook, set-fact-eda, eda-controller, decision-environments, rulebook-activation, auto-remediation, servicenow-events, drools]
level: advanced
status: docs-checked
description: "Automate reactions with Event-Driven Ansible: rulebooks (sources, conditions, actions), ansible-rulebook locally, the Alertmanager source, run_job_template and design rules."
sources: ["https://github.com/ansible/ansible-rulebook/blob/main/docs/rulebooks.rst", "https://github.com/ansible/ansible-rulebook/blob/main/docs/conditions.rst", "https://github.com/ansible/ansible-rulebook/blob/main/docs/actions.rst", "https://github.com/ansible/ansible-rulebook/blob/main/docs/installation.rst", "https://github.com/ansible/ansible-rulebook/blob/main/docs/usage.rst", "https://github.com/ansible/event-driven-ansible/blob/main/extensions/eda/plugins/event_source/alertmanager.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event-Driven Ansible rulebooks

**Goal:** an alert, a webhook or a queue message triggers the right playbook or
job template automatically, with conditions precise enough that nobody gets paged
for the remediation itself.

## 1. A rulebook
```yaml
# rulebooks/disk-remediation.yml
- name: Remediate disk alerts
  hosts: all                              # inventory passed on the CLI / activation
  sources:
    - ansible.eda.alertmanager:           # Prometheus Alertmanager webhook receiver
        host: 0.0.0.0
        port: 5000
        data_alerts_path: alerts
        data_host_path: labels.instance
        data_path_separator: "."
        skip_original_data: true
  rules:
    - name: Clean journal when disk alert fires
      condition: >
        event.alert.labels.alertname == "DiskSpaceLow" and
        event.alert.status == "firing" and
        event.alert.labels.severity in ["warning", "critical"]
      throttle: {once_within: 15 minutes, group_by_attributes: [event.meta.hosts]}
      action:
        run_job_template:
          name: "cleanup disk"
          organization: platform
          job_args:
            limit: "{{ event.meta.hosts | join(',') }}"
            extra_vars: {mount: "{{ event.alert.labels.mountpoint }}"}
    - name: Debug everything else
      condition: event.alert is defined
      action: {debug: {msg: "ignored {{ event.alert.labels.alertname }}"}}
```
- Alertmanager source options: `host` (default `localhost`), `port` (default 5000), `data_alerts_path` (default `alerts`; `""` treats the whole payload as one alert), `data_host_path` (default `labels.instance`), `data_path_separator` (default `.`), `skip_original_data` (default false: the raw body is queued as an event too, under `payload`, besides one `alert` event per alert). Each alert event carries `meta.hosts` (a list; any `:port` suffix is stripped from the host).
- A ruleset has `name`, `hosts`, `sources`, `rules`, plus optional `gather_facts`, `default_events_ttl` (default 2 hours), `execution_strategy` (`sequential` default, or `parallel`) and `match_multiple_rules` (caches events for `default_events_ttl`, memory cost).
- Rule fields: `name` (unique in the rulebook), `condition`, `action` or `actions` (run in order, each waits for the previous), `enabled` (default true), `throttle`.
- Actions in the docs: `run_playbook`, `run_module`, `run_job_template`, `run_workflow_template`, `post_event`, `set_fact`, `retract_fact`, `print_event`, `shutdown`, `debug`, `none`.
- Throttle (`once_within`, `once_after`, `accumulate_within` with `threshold`) requires `group_by_attributes` and works with a single condition; see the rulebook-event-filters-throttling skill.
- Condition language: `event.*`, `events.m_*` (multi-event), `fact.*`, `vars.*`; operators `==`, `!=`, `<`, `>`, `+`, `-`, `*`, `and`, `or`, `not`, `in`, `not in`, `contains`, `not contains`, `is defined`, `is not defined` (read the caveats), `is match(...)`, `is search(...)`, `is regex(...)`, `is select(op, value)`, `is selectattr(key, op, value)`, and `<<` to bind matching events. Jinja filters are not available in conditions; Jinja substitution is for action arguments.

## 2. Run it locally
Requirements per the install page: Python 3.10 or newer, pip, and a Java development kit 17 or newer (`JAVA_HOME` set when several JDKs are installed); `pip install ansible-rulebook ansible ansible-runner`, then `ansible-galaxy collection install ansible.eda`.```bash
ansible-rulebook --rulebook rulebooks/disk-remediation.yml -i inventory.yml \
  --controller-url https://ctl.example.com --controller-token "$TOKEN" -vv
curl -X POST localhost:5000/alerts -H 'Content-Type: application/json' -d @tests/alert.json
ansible-rulebook --rulebook r.yml -i inv.yml --print-events
```
- `--rulebook` requires `--inventory`. `-e/--vars FILE` loads variables, `-E/--env-vars` reads variables from the environment, `-S/--source-dir` and `-F/--filter-dir` point at local source and filter plugins, `-v` up to `-vv` for debug.
- `--websocket-*` options are for the worker/controller streaming mode.
- Unit-test rules with the `generic` source feeding canned `payload:` events (`eda.builtin.generic` in current releases) and read the `debug`/`print_event` output.

## 3. EDA controller (Automation Platform)
Rulebooks are placed under `extensions/eda/rulebooks` in a project for the controller (the rulebooks doc names that folder). For projects, decision environments, activations, event streams and rule audit, follow the Red Hat documentation for your AAP version; those pages could not be read as text in this review, so no controller-specific figures or image names are kept here.

## 4. Design rules
- **Idempotent remediation**: the job template must be safe to run repeatedly; `throttle` prevents storms but not correctness problems.
- **Fail closed**: match on `status == "firing"` and specific labels; `event.alert is defined` alone would remediate on `resolved` too.
- **Human in the loop for destructive actions**: `run_workflow_template` with an approval node.
- **Map identity**: the host in the event must map to inventory names. The Alertmanager source strips the port from `labels.instance`; the rest of the name must still match the controller inventory.
- **Observability**: a `print_event` or `debug` rule at the bottom while developing.

## Gotchas
- `event.payload` vs `event.alert`: shapes differ per source (webhook puts the body under `payload`; the Alertmanager source emits one `alert` event per alert). Run with `--print-events` first.
- `run_job_template` needs `--controller-url` plus `--controller-token` (or username and password). For `job_args.limit` and for event data in the `ansible_eda` namespace, enable "Prompt on launch" for Limit and Variables on the job template. `EDA_CONTROLLER_CONNECTION_LIMIT` caps concurrent controller connections (default 30). `retries`, `delay`, `set_facts`, `post_events` and `lock` are optional action options.
- `match_multiple_rules` and long `default_events_ttl` hold events in memory.

## Verify
- [ ] `ansible-rulebook ... --print-events` shows the event, and a crafted test event makes exactly one rule fire.
- [ ] A burst of identical alerts within the throttle window launches one job, and a `resolved` alert triggers nothing.

## Checked
2026-10-28. Confirmed in the ansible-rulebook docs (rulebooks, conditions, actions, installation, usage) and the ansible.eda alertmanager plugin source: ruleset and rule fields and defaults, action list, condition operators, install requirements (Python 3.10+, JDK 17+), CLI flags, `run_job_template` prerequisites and options, Alertmanager source options, `meta.hosts` and port stripping. Removed because not confirmed: the Kafka/SQS/CloudTrail/Service Bus/GCP Pub/Sub/journald source list, vendor-collection claims, the `registry.redhat.io` decision-environment image and `ansible-builder` steps, the EDA controller object model (event stream auth types, restart policies, rule audit, credentials), Java heap and restart-replay claims, division operator and the `ask_*_on_launch` wording. The EDA controller pages on docs.redhat.com returned no readable text.
Method: documentation only; no commands were run.
