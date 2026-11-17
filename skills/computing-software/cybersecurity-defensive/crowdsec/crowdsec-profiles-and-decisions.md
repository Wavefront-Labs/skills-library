---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-profiles-and-decisions
name: crowdsec-profiles-and-decisions
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [profiles, profiles-yaml, decisions, ban, captcha, duration-expr, on-success]
level: practitioner
status: docs-checked
description: "Turn alerts into decisions with profiles.yaml: filters, decision type and duration, duration_expr, notifications and on_success."
sources: ["https://docs.crowdsec.net/docs/local_api/profiles/format", "https://docs.crowdsec.net/docs/local_api/profiles/intro"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Profiles in `/etc/crowdsec/profiles.yaml` tell the Local API what to do with each alert: create decisions and/or notify. Profiles are evaluated in order.

```yaml
name: default_ip_remediation
filters:
 - Alert.Remediation == true && Alert.GetScope() == "Ip"
decisions:
 - type: ban
   duration: 4h
notifications:
  - slack_default
on_success: break
```

## Directives

- `name`: label used in logs. `debug: true` adds contextual debug.
- `filters`: a list of expr expressions; the profile applies if any returns true. Helpers are available, and you can match on scenario, for example `Alert.GetScenario() in ["crowdsecurity/ssh-bf", "crowdsecurity/ssh-user-enum"]` to give those an 8h ban.
- `decisions`: list with optional `type` (`ban`, `captcha`), `duration` (Go duration format), `scope` and a hardcoded `value`.
- `duration_expr`: overrides duration, for example `Sprintf('%dh', (GetDecisionsCount(Alert.GetValue()) + 1) * 4)` to lengthen bans for returning attackers.
- `notifications`: names of notification plugin configs.
- `on_success: break` stops evaluating further profiles after this one applies.

## Special cases

- Notification-only profile: filter on `Alert.GetScope() == "Country"` with only `notifications`.

The docs say profiles can also be written in `profiles.yaml.local`, which is read before `profiles.yaml`. The files are not merged but read as one multi-document configuration, so you may want `on_success: break`. Defaults when unset: a 4h duration, `ban` type and `ip` scope.

## Checked
2026-11-08. Confirmed against the Profiles format and introduction pages: example profile, `name`, `debug`, `filters`, `decisions` fields, `duration_expr`, `on_success`, `notifications`, the scenario-specific 8h ban example, the notification-only example and the `.local` file behaviour. Removed: the captcha-support bullet, the PID-scope and Auditd/Laurel bullet, and the wrong claim that the local file is appended.
Method: documentation only; no commands were run.
