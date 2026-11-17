---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-notification-plugins
name: crowdsec-notification-plugins
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [notifications, notification-plugins, http-plugin, slack, email, cscli-notifications-test, group-wait]
level: practitioner
status: docs-checked
description: "Configure CrowdSec notification plugins (HTTP, Slack, email and more), register them in profiles, protect secrets and test them."
sources: ["https://docs.crowdsec.net/docs/local_api/notification_plugins/intro", "https://docs.crowdsec.net/docs/local_api/notification_plugins/http"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Plugins push alerts to third-party services. They are defined and used **on the LAPI**, so in a multi-server setup configure them on the server receiving alerts. Plugin binaries ship with the package (Debian and Ubuntu `/usr/lib/crowdsec/plugins/`, RPM `/usr/lib64/crowdsec/plugins/`, Docker or source `/usr/local/lib/crowdsec/plugins/`) and each reads its own file in `/etc/crowdsec/notifications/`.

CrowdSec rejects plugin binaries that are not owned by root:root or are world-writable.

## Enabling

Name the plugin in a profile:

```yaml
name: default_ip_remediation
filters:
 - Alert.Remediation == true && Alert.GetScope() == "Ip"
decisions:
 - type: ban
   duration: 4h
notifications:
 - slackreport
on_success: break
```

The profile entry is matched to the plugin config whose `name` equals it.

## Common keys

`type`, `name`, `format` (a Go template given the list of alerts), `group_wait`, `group_threshold`, `max_retry`, `timeout`, `log_level`.

HTTP plugin example: `type: http`, `name: http_default`, `format` as a `|` block containing `{{.|toJson}}`, `url`, `method`, and optional `headers`, `unix_socket`, `skip_tls_verification`. Its file is `/etc/crowdsec/notifications/http.yaml` on Linux.

## Secrets and testing

Except in `format`, keys can use `${ENV_VAR}`; in `format` use sprig's `{{env "ENV_VAR"}}`. `cscli notifications inspect` shows raw values without interpolation. Test before enabling:

```console
SMTP_PASSWORD=secret cscli notifications test email_default
```

Provide the variables in the shell for the test; beware shell history storing secrets.

## Checked
2026-11-08. Confirmed against the Notification plugins introduction and the HTTP plugin page: LAPI-level configuration, plugin and notification directories, root:root and world-writable rejection, profile registration, common keys, environment-variable syntax, `inspect` versus `test`, the HTTP keys. Fixed: `format` shown as a `|` block (an unquoted `{{...}}` scalar is not valid YAML).
Method: documentation only; no commands were run.
