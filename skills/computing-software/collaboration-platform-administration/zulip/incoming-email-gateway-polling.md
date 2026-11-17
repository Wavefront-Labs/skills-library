---
id: computing-software.collaboration-platform-administration.zulip.incoming-email-gateway-polling
name: incoming-email-gateway-polling
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [imap-polling, email-mirror, email-gateway-login]
level: advanced
status: docs-checked
description: "Set up the Zulip email gateway by polling an IMAP inbox: plus-addressing pattern, EMAIL_GATEWAY_LOGIN, email_gateway_password, email_mirror test and cron job."
sources: ["https://zulip.readthedocs.io/en/latest/production/email-gateway.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Incoming email gateway: IMAP polling

Polling suits testing or development because it needs no public IP, MX records or firewall changes. A cron job checks an IMAP inbox every minute. Production should prefer local delivery.

1. Create a dedicated mailbox, say `username@example.com`. The provider must deliver `username+stuff@example.com` to that inbox (plus-addressing).
2. In `/etc/zulip/settings.py` set `EMAIL_GATEWAY_PATTERN = "username+%s@example.com"`.
3. Enable IMAP on the account and collect its connection details.
4. Configure Zulip: login and server details go in the email gateway section of `/etc/zulip/settings.py` (`EMAIL_GATEWAY_LOGIN` and the neighbouring settings), and the password goes in `/etc/zulip/zulip-secrets.conf` as `email_gateway_password`.
5. Send a test message to the mailbox, then poll it manually:

```
su zulip -c '~zulip/deployments/current/manage.py email_mirror'
```

6. When that works, install the cron job:

```
cd ~zulip/deployments/current/
sudo cp puppet/zulip/files/cron.d/email-mirror /etc/cron.d/
```

Because delivery depends on the cron schedule, expect up to a minute of delay. The same rate limits apply as for local delivery: 50 emails per minute, 120 per 5 minutes and 600 per hour.

## Checked

Method: docs-checked 2026-11-09 against the Zulip production Incoming email integration page (read in full).
