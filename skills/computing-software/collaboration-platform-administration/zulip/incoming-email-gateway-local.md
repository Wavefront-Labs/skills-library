---
id: computing-software.collaboration-platform-administration.zulip.incoming-email-gateway-local
name: incoming-email-gateway-local
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [email-gateway, local-mailserver, mx-record, email-gateway-pattern]
level: advanced
status: docs-checked
description: "Enable Zulip's incoming email gateway with local delivery: MX record, port 25, zulip::local_mailserver Puppet class, EMAIL_GATEWAY_PATTERN and rate limits."
sources: ["https://zulip.readthedocs.io/en/latest/production/email-gateway.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Incoming email gateway: local delivery

The gateway lets users reply to notification emails and lets third-party services mail messages into channels. Each channel then shows its own email address in its settings. Local delivery is recommended: a mail server on the Zulip host hands mail straight to Zulip, with nicer addresses and no cron delay. Incoming mail is rate-limited to 50 per minute, 120 per 5 minutes and 600 per hour.

Choose a mail domain, ideally `EXTERNAL_HOST`.

1. Create a DNS MX record for that domain pointing at the Zulip hostname. Check it with `dig +short emaildomain.example.com -t MX`.
2. Allow inbound port 25 from the Internet through any firewall.
3. On the server, append `, zulip::local_mailserver` to `puppet_classes` in `/etc/zulip/zulip.conf`, for example `zulip::profile::standalone, zulip::local_mailserver`.
4. Run `~zulip/deployments/current/scripts/zulip-puppet-apply` and answer `y`.
5. Set `EMAIL_GATEWAY_PATTERN = "%s@emaildomain.example.com"` in `/etc/zulip/settings.py`.
6. Restart with `~zulip/deployments/current/scripts/restart-server`.

By default the mail server listens on port 25 on all IPv4 and IPv6 addresses; change that with `email_gateway.listen` in `zulip.conf`.

Docker deployments differ: port 25 is already exposed and settings come from `SETTING_`-prefixed variables such as `SETTING_EMAIL_GATEWAY_PATTERN`, so follow the Docker incoming-email guide instead of the steps above.

## Checked

Method: docs-checked 2026-11-09 against the Zulip production Incoming email integration page (read in full).
