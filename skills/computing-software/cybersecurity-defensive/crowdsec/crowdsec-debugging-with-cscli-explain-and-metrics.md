---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-debugging-with-cscli-explain-and-metrics
name: crowdsec-debugging-with-cscli-explain-and-metrics
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [cscli-explain, cscli-metrics, debugging, lines-unparsed, acquisition-metrics, hubtest]
level: practitioner
status: docs-checked
description: "Debug why CrowdSec does not detect something using cscli explain and cscli metrics acquisition, parser and scenario tables."
sources: ["https://docs.crowdsec.net/docs/cscli/cscli_explain", "https://docs.crowdsec.net/docs/observability/cscli", "https://docs.crowdsec.net/docs/log_processor/data_sources/troubleshoot"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## cscli explain

Runs lines through the pipeline and shows which parsers and scenarios handled them:

```console
cscli explain --file ./myfile.log --type nginx
cscli explain --log "Sep 19 18:33:22 host sshd[24347]: pam_unix(sshd:auth): authentication failure; ... rhost=1.2.3.4" --type syslog
cscli explain --dsn "file://myfile.log" --type nginx
tail -n 5 myfile.log | cscli explain --type nginx -f -
```

`--failures` shows only failed lines. With explain, postoverflows run inline.

## cscli metrics

`cscli metrics list` shows the sections: acquisition, alerts, appsec-challenge, appsec-challenge-infra, appsec-engine, appsec-rule, bouncers, decisions, lapi, lapi-bouncer, lapi-decisions, lapi-machine, parsers, scenarios, stash and whitelists. `cscli metrics show engine` groups acquisition, parsers, scenarios, whitelists and stash; `show lapi`, `show appsec` and `show bot-detection` are other aliases (the list also has `appsec-challenge-infra`).

## Reading acquisition metrics

Columns per source: lines read, parsed, unparsed, poured to bucket. Interpretation:

- Zero lines read: the datasource is misconfigured or inactive.
- Zero lines parsed: the parser(s) failed.
- Non-zero unparsed lines are fine, as crowdsec selects relevant lines.
- Poured can exceed read because one line can feed several scenarios.

The docs recommend `cscli hubtest` for regression-testing parsers and scenarios you author.

## Checked

2026-11-03. Confirmed against the cscli explain reference, cscli metrics and datasource monitoring pages: explain flags and examples, metrics sections and aliases, acquisition column meanings and interpretation. Removed: the 'wrong type label' guess and the kern.log/syslog remark.

Method: documentation only; no commands were run.
