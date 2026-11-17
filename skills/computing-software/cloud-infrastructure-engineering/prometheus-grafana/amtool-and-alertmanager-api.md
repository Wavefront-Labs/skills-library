---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.amtool-and-alertmanager-api
name: amtool-and-alertmanager-api
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [alertmanager, amtool-usage, amtool-config-routes-test, alertmanager-api, alerts-api-v2, silences, automation]
level: practitioner
status: verified
description: "Operate Alertmanager from the CLI and API: amtool config check and route testing, querying alerts, creating/expiring silences, and the v2 HTTP API for automation."
sources: ["https://github.com/prometheus/alertmanager#amtool", "https://github.com/prometheus/alertmanager/blob/main/api/v2/openapi.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# amtool and the Alertmanager API

## Config
```bash
amtool check-config alertmanager.yml
amtool config routes show --config.file=alertmanager.yml                 # tree view
amtool config routes test --config.file=alertmanager.yml --verify.receivers=team-db-pager \
  severity=page team=db alertname=PostgresDown                           # exit 1 if receiver differs
```
Run on amtool 0.34.1: `check-config` prints `SUCCESS` and counts of routes, receivers and inhibit rules; `routes show` prints the tree; `routes test` prints the matching receiver(s), comma-separated when `continue: true` matches several; with a wrong `--verify.receivers` it prints `WARNING: Expected receivers did not match resolved receivers.` and exits 1; `--tree` prints the matching routes. Put `routes test` cases in CI so a routing change can't silently reroute pages.

## Alerts and silences
```bash
# amtool needs --alertmanager.url on every call, or alertmanager.url in $HOME/.config/amtool/config.yml
# or /etc/amtool/config.yml (amtool source and --help). There is NO AMTOOL_ALERTMANAGER_URL environment
# variable: with it exported, amtool 0.34.1 still failed with "required flag --alertmanager.url not provided".
AM="amtool --alertmanager.url=http://alertmanager:9093"
$AM alert query                             # active alerts (the default view)
$AM alert query -s -i                       # -s silenced, -i inhibited, -u unprocessed; -a means ACTIVE, not "all"
$AM silence add alertname=DiskFull 'instance=~db-0[12].*' -d 2h -c "disk migration CHG-1234" -a "alice"   # -a is --author here
$AM silence query                           # active silences with IDs
$AM silence expire <id>
$AM silence query -q | xargs $AM silence expire     # expire all (careful)
$AM alert add test_alert severity=info --annotation=summary="routing test"   # synthetic alert
```
Run against a local Alertmanager 0.34.1: `alert add` created three alerts; `alert query severity=page -a` listed the active `severity=page` alerts (`-a` is the active filter); after `silence add` the matching alert showed `suppressed` under `-s`; `-o extended` prints labels, annotations, start/end and state; the regex matcher is anchored (`instance=~db-0[12]` silenced `db-02` but not `db-01x`); `silence query -q | xargs ... silence expire` expired the silence (exit 0) and `silence query --expired` then listed it. `--annotation=summary="routing test"` (the shell removes the quotes) worked but logged a WARN that the input was parsed with the classic matchers parser, suggesting `summary="routing test"` with the quotes kept.

## API v2
```bash
AM=http://alertmanager:9093/api/v2
curl -s "$AM/alerts?active=true&silenced=false&filter=severity%3D%22page%22"   # JSON array; each item has .labels.alertname and .status.state
curl -s "$AM/status"       # .cluster.status and .versionInfo.version (run: "disabled" and "0.34.1" on a single node started with an empty --cluster.listen-address)
curl -s -XPOST "$AM/silences" -H 'Content-Type: application/json' -d '{
  "matchers":[{"name":"service","value":"checkout","isRegex":false,"isEqual":true}],
  "startsAt":"2026-10-16T22:00:00Z","endsAt":"2026-10-16T23:00:00Z",
  "createdBy":"deploy-bot","comment":"deploy 4812"}'        # returns {"silenceID": "..."}
curl -s -XDELETE "$AM/silence/<id>"       # run: HTTP 200, the silence then reads back with state "expired"
```
Deploy pipelines: create a scoped silence for the deploy window, expire it when done.

## Gotchas
- Alertmanager has no relabeling of its own; Prometheus applies `alert_relabel_configs` before sending (Prometheus configuration docs), so silences match the labels that arrive. Check the exact labels with `amtool alert query -o extended`.
- Regex matchers are anchored like PromQL (run: `instance=~db-0[12]` did not match `db-01x`).

## Verify
- [ ] Routes test cases pass in CI.
- [ ] A silence created via API shows in `amtool silence query` and moves to `--expired` at `endsAt` (run: a one-minute silence was in the expired list 80 s later).

## Checked
Alertmanager and amtool 0.34.1 (windows-amd64) run locally against a single Alertmanager: `check-config`, `config routes show/test` (including `--verify.receivers` match and mismatch exit codes, `--tree`), `alert add/query` with `-a`, `-s`, `-i`, `-o extended`, `silence add/query/expire`, `silence query -q | xargs`, `silence query --expired`, the exported-variable attempt, and the API v2 calls (`alerts` filter, `status`, POST and DELETE on silences). Sources: amtool `cli/root.go` at v0.34.1 (config file locations, no environment variable), Alertmanager configuration docs, Prometheus configuration docs (alert relabeling). `jq` was replaced by plain output. A one-minute silence was seen moving to the expired list.
