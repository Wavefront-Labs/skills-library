---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.alertmanager-routing-and-silencing
name: alertmanager-routing-and-silencing
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [alertmanager, prometheus, alert-routing, route-tree, matchers, receivers, pagerduty, slack, opsgenie, webhook, group-by, group-wait, group-interval, repeat-interval, inhibit-rules, silences, amtool, mute-time-intervals, active-time-intervals, watchdog, dead-mans-switch, alertmanager-ha, notification-templates, on-call]
level: advanced
status: gated
description: "Configure Alertmanager so the right team gets one useful page: route trees with matchers and continue, grouping timers, inhibition, time-based muting, amtool silences and routing tests, HA."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/", "https://prometheus.io/docs/alerting/latest/alertmanager/", "https://github.com/prometheus/alertmanager#amtool"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alertmanager routing and silencing — one page, right team, no storm

**Goal:** every alert reaches exactly the owning team's channel at the right urgency,
related alerts arrive as one notification, downstream noise is inhibited, and planned
work is silenced without anyone editing config at 3 a.m. Writing the alert rules
themselves is in `computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-and-alert-rules`.

## 1. Label contract first
Routing only works if rules carry consistent labels. Agree on, and lint for:
`severity` (`page` | `ticket` | `info`), `team`, `service`, optionally `env`.
Alerts without `team` should land in a visible catch-all, not vanish.

## 2. Route tree
```yaml
route:
  receiver: catch-all
  group_by: [alertname, service, env]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - matchers: ['alertname = "Watchdog"']
      receiver: deadmans-switch
      repeat_interval: 1m
    - matchers: ['env != "prod"']
      receiver: nonprod-slack
    - matchers: ['team = "payments"']
      routes:
        - matchers: ['severity = "page"']
          receiver: payments-pagerduty
          continue: true          # also evaluate later siblings
        - matchers: ['severity =~ "page|ticket"']
          receiver: payments-slack
receivers:
  - name: payments-pagerduty
    pagerduty_configs: [{ routing_key_file: /etc/alertmanager/secrets/pd-payments }]
  - name: payments-slack
    slack_configs: [{ api_url_file: /etc/alertmanager/secrets/slack-payments, channel: "#payments-alerts", send_resolved: true }]
```
Run through `amtool check-config` (SUCCESS, with dummy secret files and the `catch-all`, `deadmans-switch`, `nonprod-slack` receivers defined) and `amtool config routes test --config.file=...`: `team=payments severity=page env=prod` gave `payments-pagerduty,payments-slack`; `team=payments severity=ticket env=prod` gave `payments-slack`; `alertname=Watchdog` gave `deadmans-switch`. Two surprises: `team=payments severity=page` with NO `env` label gave `nonprod-slack`, because `env != "prod"` also matches an absent label and is an earlier sibling (so alerts missing `env` never reach the team routes: put the label contract in rules, or move that route below the team routes); and `team=payments severity=info env=prod` gave `catch-all` (the `payments` parent has no receiver of its own and inherits the root's).
- Evaluation is depth-first, **first match wins** among siblings unless `continue: true`.
- Children inherit `group_by` and timers unless they override.
- Use the `matchers` list (UTF-8 aware parser since Alertmanager 0.27, with a classic-parser fallback that logs a WARN, configuration docs); `match`/`match_re` are marked DEPRECATED in the docs.
- Prefer `*_file` options for keys and webhook URLs so secrets stay out of the config.

## 3. Grouping timers
- `group_wait`: delay before the first notification of a new group, to collect siblings (10–60 s).
- `group_interval`: delay before notifying about *new* alerts added to an existing group (≥ 5 m).
- `repeat_interval`: re-send an unchanged, still-firing group (hours; pages via the pager's own escalation instead).
- `group_by: ['...']` groups by all labels, so every distinct label set is its own group (configuration docs) — only for receivers that dedupe themselves.

## 4. Inhibition
```yaml
inhibit_rules:
  - source_matchers: ['severity = "page"']
    target_matchers: ['severity = "ticket"']
    equal: [alertname, service, env]
  - source_matchers: ['alertname = "ClusterUnreachable"']
    target_matchers: ['alertname =~ ".+"', 'alertname != "ClusterUnreachable"']
    equal: [cluster]
```
`equal` is essential: without it, any page anywhere mutes every ticket everywhere.

## 5. Time-based muting
```yaml
time_intervals:
  - name: business-hours
    time_intervals:
      - weekdays: ['monday:friday']
        times: [{ start_time: "09:00", end_time: "17:30" }]
        location: Europe/London
  - name: weekends
    time_intervals:
      - weekdays: ['saturday', 'sunday']
        location: Europe/London
# on a route (the Alertmanager config check also accepted both keys on one route):
    mute_time_intervals: [weekends]       # suppress outside work for ticket routes
    active_time_intervals: [business-hours]
```
Both keys are route-level, are not inherited by child routes and cannot be set on the root (configuration docs; run: see the alertmanager-time-intervals skill). `location: Europe/London` needs a tz database: on Windows set `ZONEINFO` to Go's `zoneinfo.zip` or `check-config` fails with `unknown time zone`. Use for ticket-level routes; never mute pages by time.

## 6. Silences with amtool
```bash
# amtool has no AMTOOL_ALERTMANAGER_URL variable (tested): pass --alertmanager.url on each call, or set
# alertmanager.url in $HOME/.config/amtool/config.yml or /etc/amtool/config.yml
AM="amtool --alertmanager.url=http://alertmanager.internal:9093"
$AM silence add 'service="checkout"' 'env="prod"' \
  --duration=2h --comment="DB failover drill CHG-<ID>" --author="<YOUR_NAME>"
$AM silence query
$AM silence expire <SILENCE_ID>
```
Run against Alertmanager 0.34.1: the add printed a silence ID, `silence query -o extended` showed `{service="checkout",env="prod"}` with start, end (two hours later), creator and comment, and `silence query -q | xargs ... silence expire` expired it.
- Silence the narrowest matcher set; a silence on `env="prod"` alone hides real outages.
- Always set a duration and change reference; review active silences in handover.

## 7. Test before deploying
```bash
amtool check-config alertmanager.yml
amtool config routes test --config.file=alertmanager.yml team=payments severity=page env=prod
amtool config routes show --config.file=alertmanager.yml   # prints the tree
```
Run: both print as described; `routes test` prints the receiver names comma-separated and exits 1 only when `--verify.receivers` disagrees.
Put `routes test` cases for each team in CI.

## 8. High availability and dead man's switch
- Run 2–3 Alertmanagers clustered (`--cluster.peer=...` exists in 0.34.1 `--help`); point every Prometheus at
  **all** of them (not a load balancer). The gossip mesh dedupes notifications and shares silences (gated: unconfirmed, source is paywalled or blocked; a cluster was not run here).
- Always-firing `Watchdog` alert routed to an external heartbeat service (e.g. a
  pager's heartbeat/dead-man's-snitch integration) proves the whole pipeline is alive (gated: unconfirmed, source is paywalled or blocked; no heartbeat service here).

## Gotchas
- Changing `group_by` re-creates groups: expect a burst of "new" notifications after deploy.
- `send_resolved` defaults differ per receiver (configuration docs for 0.34: false for email, Slack, Rocket.Chat and WeChat; true for webhook, PagerDuty, Opsgenie and most others); set it explicitly.
- `amtool check-config` does not catch template mistakes in inline `text`: both `{{ .Missing }}` and the syntax error `{{ if }}` passed with SUCCESS. At runtime 0.34.1 still delivered the Slack notification (to a local listener) but with `"text":""` and without the `channel`, `username` and `color` fields, and logged nothing, so a template error looks like an empty message rather than a failure. Test templates by sending a fake alert (`amtool alert add`) and reading the payload.
- Silences live in Alertmanager's `--storage.path` (it held `silences` and `nflog` files in the test run); losing it (no persistent volume) drops every silence.
- Matcher parsing for UTF-8 label names depends on the version and mode (fallback, UTF-8 strict, classic; configuration docs); quote values always. In fallback mode input the new parser cannot read is parsed by the classic parser and logs a WARN, as seen for an unquoted annotation value in `amtool alert add`.

## Verify
- [ ] `amtool check-config` and per-team `amtool config routes test` pass in CI.
- [ ] A test alert (`amtool alert add alertname=Test team=payments severity=page env=prod`) reaches the expected receivers only.
- [ ] Watchdog heartbeat goes red within minutes when Alertmanager is stopped.
- [ ] Every inhibit rule has an `equal` list.
- [ ] No active silence lacks a comment, author and end time.

## Checked
Alertmanager and amtool 0.34.1 (windows-amd64) run locally with a local webhook/Slack-style listener: the skill's route tree, receivers (dummy secret files) and inhibit rules through `check-config`; six `routes test` label sets; a config with both `mute_time_intervals` and `active_time_intervals` on a route (accepted); `silence add/query/expire` with the skill's quoting and `alert add`; Slack payloads for three inline-template variants (`{{ .Missing }}`, `{{ if }}`, a valid `{{ .CommonLabels.alertname }}`). Docs read: Alertmanager configuration.md (send_resolved defaults, route inheritance, UTF-8 matcher modes, group_by '...'), amtool `cli/root.go`. Not run: PagerDuty, Slack, HA cluster, heartbeat integrations.
