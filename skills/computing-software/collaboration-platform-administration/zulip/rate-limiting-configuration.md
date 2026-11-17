---
id: computing-software.collaboration-platform-administration.zulip.rate-limiting-configuration
name: rate-limiting-configuration
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [rate-limiting, rate-limiting-rules, reset-authentication-attempt-count]
level: practitioner
status: docs-checked
description: "Inspect and tune Zulip rate limiting: get-django-setting RATE_LIMITING_RULES, RATE_LIMITING, RATE_LIMIT_TOR_TOGETHER and clearing login lockouts."
sources: ["https://zulip.readthedocs.io/en/latest/production/securing-your-zulip-server.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zulip rate limiting

Zulip rate-limits login attempts, all API access and certain abuse-prone actions. The email confirmation flow must allow mail to addresses with no account, so limits there protect your server's spam reputation from confirmation emails sent to random addresses.

Defaults change as the product improves. See current rules with:

```
~zulip/deployments/current/scripts/get-django-setting RATE_LIMITING_RULES
```

For commented defaults read `DEFAULT_RATE_LIMITING_RULES` in `zproject/default_settings.py`.

Tweaks in `/etc/zulip/settings.py`:

- `RATE_LIMITING = False` disables all rate limiting.
- `RATE_LIMITING_RULES` overrides specific rules; follow the comment in the settings file. After editing, run `get-django-setting RATE_LIMITING_RULES` to verify the merged result, then restart with `scripts/restart-server`.
- `RATE_LIMIT_TOR_TOGETHER = True` groups all known Tor exit nodes for IP-based limits. Without it, traffic spread across exit nodes sidesteps IP limits. The exit list is refetched hourly.

If a user hits the login attempt limit, an administrator clears it with the `reset_authentication_attempt_count` management command, run through `manage.py`.

The API documentation has a separate page describing rate limiting from the client side.

## Checked

Confirmed against section 6 of the Securing your Zulip server page: the rate-limited actions, get-django-setting RATE_LIMITING_RULES, DEFAULT_RATE_LIMITING_RULES, RATE_LIMITING, RATE_LIMIT_TOR_TOGETHER with the hourly refetch, and reset_authentication_attempt_count. Removed the reverse-proxy X-Forwarded-For remark (not on the page).

Method: docs-checked 2026-11-09 against docs/production/securing-your-zulip-server.md in the zulip/zulip repository (main), the source of the cited page.
