---
id: computing-software.messaging-and-integration.ntfy.cli-client-config
name: cli-client-config
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, cli, client-yml, from-config, defaults]
level: practitioner
status: docs-checked
description: "Configure many ntfy subscriptions in client.yml and run them with ntfy subscribe --from-config, including default credentials rules."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/subscribe/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# client.yml and --from-config

Config locations: Linux non-root `~/.config/ntfy/client.yml`, macOS non-root `~/Library/Application Support/ntfy/client.yml`, root `/etc/ntfy/client.yml`.

```yaml
default-host: https://ntfy.sh
default-user: phill
default-password: mypass

subscribe:
- topic: echo-this
  command: 'echo "Message received: $message"'
- topic: alerts
  command: notify-send -i /usr/share/ntfy/logo.png "Important" "$m"
  if:
    priority: high,urgent
- topic: secret
  command: 'notify-send "$m"'
  user: phill
  password: mypass
```

Run with `ntfy subscribe --from-config`.

## Rules

- Top-level keys: `default-host`, `default-user`, `default-password`, `default-token`, `default-command`.
- Use `default-user` plus `default-password`, or `default-token`, not both.
- `default-command` runs when a subscription has no `command`.
- Subscription-level settings override defaults.

## Gotchas

- Defaults are sent to every topic lacking its own credentials, even public ones; use HTTPS.
- The page's per-platform examples use `osascript` and `open -a` on macOS, and `%message%` / `%NTFY_MESSAGE%` variables on Windows.

## Checked

2026-11-04. Confirmed against the ntfy subscribe CLI page: config paths, example config, `--from-config`, default keys and credential rules, `if: priority`, HTTPS warning. Removed: the Verify step.
Method: documentation only; no commands were run.
