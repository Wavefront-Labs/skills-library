---
id: computing-software.devops-ci-cd.flagger.flagger-alert-providers
name: flagger-alert-providers
category: computing-software
field: devops-ci-cd
product: flagger
tags: [alerting, alertprovider, slack, msteams]
level: practitioner
status: docs-checked
description: "Send Flagger canary notifications globally through Helm values or per canary with AlertProvider resources and severity levels."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/alerting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Global config at install time. Slack needs a legacy-style incoming webhook (not the new Slack app system):

```bash
helm upgrade -i flagger flagger/flagger \
  --set slack.url=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK \
  --set slack.channel=general --set slack.user=flagger \
  --set clusterName=my-cluster
```

Teams: `--set msteams.url=...`. Flagger posts when a canary is initialised, a new revision is detected, and when analysis succeeds or fails. A canary rolls back when the progress deadline passes or failed checks hit the maximum. For a Slack bot token, put `token` in a Secret and use `secretRef`.

Per canary: create an `AlertProvider` (`type`: `slack`, `msteams`, `rocket` or `discord`; `channel` defaults to `general`, `username` to `flagger`; `secretRef` with an `address` field overrides `address`). Discord uses Slack formatting with `/slack` appended to the address. Then list alerts in `analysis.alerts` with `name`, `severity` (`info` default, `warn`, `error`) and `providerRef` (namespace defaults to the canary's).

`warn` alerts on waiting-for-confirmation and failed analysis; `error` only on failed analysis. Set `-cluster-name` (Helm `clusterName`) to tell clusters apart. Alertmanager can also alert on `flagger_canary_status > 1`.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/alerting.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
