---
id: computing-software.cybersecurity-defensive.network-defence.suricata-update-ruleset-management
name: suricata-update-ruleset-management
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [ids, suricata-update, et-open, et-pro, disable-conf, modify-conf, ruleset-management, rule-reload]
level: practitioner
status: docs-checked
description: "Manage Suricata rulesets with suricata-update: enabling ET Open/Pro and other sources, disable/enable/modify/drop conf files, local rules, testing, and live reload."
sources: ["https://docs.suricata.io/en/latest/rule-management/suricata-update.html", "https://docs.suricata.io/en/latest/rule-management/rule-reload.html", "https://docs.suricata.io/en/latest/unix-socket.html", "https://suricata-update.readthedocs.io/en/latest/", "https://rules.emergingthreats.net/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ruleset management with suricata-update

## Basics
```
suricata-update update-sources
suricata-update list-sources
suricata-update enable-source et/pro secret-code=<oinkcode>      # or keep et/open default
suricata-update enable-source oisf/trafficid
suricata-update                                                   # fetch, merge, write /var/lib/suricata/rules/suricata.rules
suricatasc -c reload-rules                                        # live reload (or kill -USR2)
```
`suricata.yaml` should point `default-rule-path: /var/lib/suricata/rules` and `rule-files: [suricata.rules]`.

## Control files (in /etc/suricata/)
- `disable.conf`: one matcher per line: a SID (`2019401` or `1:2019401`), `group:emerging-icmp.rules`,
  `re:heartbleed` (regex over the whole rule, case-insensitive), `filename:*/emerging-dos.rules`, or a
  `metadata: deployment perimeter` match.
- `enable.conf`: the same matchers, to enable rules that are disabled by default in the source.
- `drop.conf`: the same matchers; matching rules become drop rules for IPS mode (start narrow, e.g. specific high-confidence SIDs).
- `modify.conf`: `<match> "<from>" "<to>"` search and replace, e.g. `2019401 "seconds \d+" "seconds 3600"` or
  `re:. ^alert drop`; metadata matching is not available for modification.
- `threshold.config` is read by Suricata itself (suricata-update can template it via `--threshold-in` / `--threshold-out`).
Run `suricata-update` after any change; the files are applied in the order disable, enable, drop, modify.

## Local rules
Keep your own rules in `/etc/suricata/rules/local.rules` and add it via `--local /etc/suricata/rules/local.rules`
(or in the `local:` list of `/etc/suricata/update.yaml`) so they merge into the same output. Use SIDs that cannot
clash with published ranges (see sidallocation.org).

## Test before reload
```
suricata -T -c /etc/suricata/suricata.yaml -v     # validate config and rules
suricata -r sample.pcap -c /etc/suricata/suricata.yaml -l /tmp/out   # replay pcaps, check eve.json alerts
```
suricata-update runs a test by default (`--no-test` skips it; do not skip in automation).

## Automation
Run `suricata-update` on a schedule with `--reload-command='sudo suricatasc -c reload-rules'` (it runs only when the
output changed); `suricatasc -c ruleset-reload-nonblocking` reloads without waiting. Version the `/etc/suricata/*.conf`
files in Git and deploy with config management.

## Gotchas
- Enabling every category = performance problems and noise. Start with ET Open/Pro defaults, disable
  policy-only categories (games, chat) unless needed.
- `HOME_NET`/`EXTERNAL_NET` wrong makes directional rules useless.
- Air-gapped sensors cannot download: point `--url` at a local mirror, or run `suricata-update --offline` to reuse the cached rules.

## Verify
`suricatasc -c ruleset-stats` shows the number of rules loaded and failed (`ruleset-failed-rules` lists the failures);
replay a pcap that should trigger a known rule and confirm the alert in `eve.json`.

## Checked

Checked 2026-10-25 against Suricata user guide source (OISF/suricata doc/userguide, main branch, last pushed 2026-10-23, 8.x documentation) and the suricata-update documentation source (OISF/suricata-update `doc/`, last pushed 2026-07-07). Confirmed: `update-sources`, `list-sources`, `enable-source <name> [param=val]` (including `et/pro secret-code=`), `list-enabled-sources`, default output `/var/lib/suricata/rules/suricata.rules`, `--local`, `--url`, `--no-test`, `--offline`, `--reload-command`, matcher types (SID, `gid:sid`, `re:`, `group:`, `filename:`, `metadata:`), the `<match> "<from>" "<to>"` modify format, the apply order disable, enable, drop, modify, `local:` in update.yaml, and the `reload-rules`, `ruleset-reload-nonblocking`, `ruleset-stats`, `ruleset-failed-rules` socket commands plus `kill -USR2`. Removed the undocumented `classification:` matcher, the testmynids SID, the fleet-tool names and the silent-failure claim.

Method: documentation only; no commands were run.
