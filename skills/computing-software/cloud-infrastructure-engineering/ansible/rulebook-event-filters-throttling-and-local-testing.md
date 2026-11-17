---
id: computing-software.cloud-infrastructure-engineering.ansible.rulebook-event-filters-throttling-and-local-testing
name: rulebook-event-filters-throttling-and-local-testing
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, event-driven-ansible, event-filters, dashes-to-underscores, eda-throttle, time-window, rulebook-test, print-events, ansible-rulebook]
level: advanced
status: docs-checked
description: "Shape events with ansible-rulebook event filters, stop alert storms with throttle once_within/once_after, and test rulebooks locally with the generic source and print_event."
sources: ["https://docs.ansible.com/projects/rulebook/en/latest/filters.html", "https://docs.ansible.com/projects/rulebook/en/latest/sources.html", "https://github.com/ansible/ansible-rulebook/blob/main/docs/conditions.rst", "https://github.com/ansible/ansible-rulebook/blob/main/docs/usage.rst", "https://github.com/ansible/ansible-rulebook/blob/main/docs/actions.rst", "https://github.com/ansible/event-driven-ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rulebook event filters, throttling and local testing

## Event filters
Filters preprocess event data **before** the rule engine evaluates it. They chain: each filter's output feeds the next. Define them under the source:
```yaml
sources: []
  - name: alerts
    eda.builtin.webhook:
      host: 0.0.0.0
      port: 5000
      token: "{{ webhook_token }}"
    filters:
      - eda.builtin.json_filter:
          exclude_keys: ["payload.raw_body"]
      - eda.builtin.dashes_to_underscores:
      - eda.builtin.insert_hosts_to_meta:
          host_path: payload.labels.instance   # sets meta.hosts; actions then run only on those hosts
```
- The `webhook`, `generic`, `range` and `pg_listener` sources and the `insert_hosts_to_meta`, `json_filter`, `normalize_keys`, `dashes_to_underscores` filters now ship inside ansible-rulebook as `eda.builtin.*`. The old `ansible.eda.*` names still map to them for compatibility but are no longer maintained; use `eda.builtin`. Other built-ins: `insert_meta_info` (added automatically: source name and type, `received_at`, `uuid`) and `event_splitter` (splits an array of events, with `splitter_key` required).
- Event keys can only contain letters, numbers and underscores, and `.` reaches nested keys. `dashes_to_underscores` rewrites dashed keys recursively (`overwrite` default true); `normalize_keys` replaces any non-alphanumeric run with one underscore.
- `json_filter`: `exclude_keys` removes key patterns (wildcards `*` and `?`); `include_keys` is NOT a whitelist, it only protects keys that would otherwise be excluded, and include wins over exclude.
- `insert_hosts_to_meta`: `host_path` required (dot notation by default, `path_separator` changes it), `host_separator` splits a multi-host string, `raise_error` (default false, recommended while developing).
- Custom filters are Python distributed in a collection. During development `-F DIR` (`--filter-dir`) points at a local filter directory; that does not work inside a decision environment.

## Throttling
```yaml
rules:
  - name: Restart app on repeated 5xx alert
    condition: event.payload.alertname == "App5xx" and event.payload.status == "firing"
    throttle:
      once_within: 10 minutes
      group_by_attributes:
        - event.payload.labels.instance
    action:
      run_job_template:
        name: restart-app
        organization: Platform
        job_args:
          limit: "{{ event.payload.labels.instance }}"
```
- `once_within`: the first matching event fires, further ones are suppressed until the window expires; `group_by_attributes` is mandatory. Event-level granularity.
- `once_after`: waits for the window, then fires once for all unique events collected; `group_by_attributes` is mandatory.
- `accumulate_within` with `threshold`: fires when the threshold count arrives inside the window, otherwise the events are discarded.
- All three work only with a single condition. Time units: milliseconds, seconds, minutes, hours, days.
- To require several events within a window use `all:` (or `not_all:`) plus `timeout: 10 seconds`; the timer starts when the first condition matches and overrides the ruleset's `default_events_ttl` (default 2 hours).
- `run_job_template` needs `--controller-url` and a token (or username and password) on the command line. For `job_args.limit` or `ansible_eda` event data to take effect, enable "Prompt on launch" for Limit and Variables on the job template.

## Testing locally
```yaml
# test-rulebook.yml
- name: test
  hosts: all
  sources:
    - eda.builtin.generic:
        payload:
          - {alertname: App5xx, status: firing, labels: {instance: web1}}
          - {alertname: App5xx, status: firing, labels: {instance: web1}}
          - {alertname: App5xx, status: firing, labels: {instance: web2}}
  rules:
    - name: print
      condition: event.alertname == "App5xx"
      throttle: {once_within: 1 minute, group_by_attributes: [event.labels.instance]}
      action:
        print_event:
          pretty: true
```
```bash
ansible-rulebook -r test-rulebook.yml -i inventory.yml --print-events -v
```
- `--print-events` prints events to stdout (it is redundant and disabled at `-vv`); `-v` adds debug messages, maximum `-vv`.
- `eda.builtin.range` (`limit` exclusive, optional `delay`) emits `{"i": n}` events; `eda.builtin.generic` takes `payload` or `payload_file`, plus `loop_count`, `event_delay`.
- `print_event` (optional `pretty`) and `debug` actions show what a rule matched.

## Gotchas
- `execution_strategy` on the ruleset is `sequential` (default, waits for each action) or `parallel`; the action `lock` option serialises parallel actions.
- Webhook sources without `token`, HMAC (`hmac_secret`) or TLS (`certfile`, `keyfile`, optional `cafile` for mTLS) accept events from anyone who can reach the port.

## Verify
- [ ] The local test prints filtered keys as expected and throttling suppresses duplicates per instance.

## Checked
2026-10-28. Confirmed in the ansible-rulebook docs (filters, sources, conditions, usage, actions, rulebooks pages) and the ansible.eda README: `eda.builtin` migration, filter parameters and semantics, throttle forms and the group_by_attributes requirement, timeout units, controller flags and prompt-on-launch notes, `-F`, `--print-events`, `-v` levels, generic and range source parameters, `print_event`, `execution_strategy`, webhook auth options. Removed because not confirmed: the `extensions/eda/plugins/event_filter/` path, the claim that throttle state resets on activation restart, and a rule ordering claim. Fixed: `json_filter` `include_keys` was presented as a whitelist.
Method: documentation only; no commands were run.
