---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-appsec-deploy-custom-rule
name: crowdsec-appsec-deploy-custom-rule
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [appsec-config, appsec-rules-deploy, acquis-appsec, default-remediation, hubtest, rule-deployment]
level: practitioner
status: docs-checked
description: "Deploy a custom AppSec rule end to end: rule file, appsec-config, acquisition entry, reload and curl test."
sources: ["https://docs.crowdsec.net/docs/appsec/rules_deploy", "https://docs.crowdsec.net/docs/appsec/configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Steps for a rule that blocks GET requests whose `user_id` is non-numeric:

1. **Stage the rule** in `/etc/crowdsec/appsec-rules/` (a `custom/` subfolder keeps it tidy). The rule uses `and` of `METHOD equals GET` and `ARGS` with `variables: [user_id]` and `regex "[^0-9]"`. In a container, copy into the volume mounted at that path.
2. **Create an AppSec configuration** in `/etc/crowdsec/appsec-configs/`:

```yaml
name: custom/block-nonnumeric-user-id
default_remediation: ban
inband_rules:
  - custom/block-nonnumeric-user-id
```

`inband_rules` and `outofband_rules` accept globs such as `custom/block-*`.

3. **Reference it** in `/etc/crowdsec/acquis.d/appsec.yaml`:

```yaml
appsec_configs:
  - crowdsecurity/appsec-default
  - custom/block-nonnumeric-user-id
labels:
  type: appsec
listen_addr: 127.0.0.1:7422
source: appsec
```

Order matters: later entries override defaults such as `default_remediation`.

4. **Reload**: `sudo systemctl reload crowdsec` (restart if reload is unsupported). A syntax error fails the reload. Confirm with `cscli appsec-rules list` and `cscli appsec-configs list`.
5. **Test**: `curl -i 'http://127.0.0.1/profile?user_id=abc123'` should return 403, and `cscli alerts list -s custom/block-nonnumeric-user-id` shows the alert.

## Config keys

An appsec-config has `name`, `inband_rules`, `outofband_rules`, `default_remediation` (`allow` disables blocking; with multiple configs the last wins), `default_pass_action`, `blocked_http_code`, `passed_http_code`, `log_level`, hooks (`inband`, `outofband`, `on_load`) and options. Add regression tests with `cscli hubtest`.

## Checked

2026-11-03. Confirmed against the AppSec rules deployment and configuration pages: rule and config paths, example rule, glob rules, acquisition file and ordering, reload, cscli appsec-rules/appsec-configs list, curl test returning 403, config keys and last-wins behaviour. Removed: nothing.

Method: documentation only; no commands were run.
