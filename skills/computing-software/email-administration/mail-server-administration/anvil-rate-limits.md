---
id: computing-software.email-administration.mail-server-administration.anvil-rate-limits
name: anvil-rate-limits
category: computing-software
field: email-administration
product: mail-server-administration
tags: [anvil-rate-limits, postfix-rate-limits, anvil, smtpd-client-connection-rate-limit, smtpd-client-message-rate-limit]
level: advanced
status: docs-checked
description: "Limit abusive connections with Postfix anvil settings: smtpd_client_connection_rate_limit and message rate limits."
sources:
  - https://www.postfix.org/anvil.8.html
  - https://www.postfix.org/postconf.5.html
  - https://www.postfix.org/TUNING_README.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Anvil rate limits

**Goal:** cap per-client damage without blocking legitimate bursts.
## Steps
1. `smtpd_client_connection_count_limit = 20` (default 50; 0 disables).
2. `smtpd_client_connection_rate_limit = 30` per `anvil_rate_time_unit` (default 60s; the rate limit default is 0 = off).
3. `smtpd_client_message_rate_limit` and `smtpd_client_recipient_rate_limit` for outbound abusers on submission.
4. Clients in `$mynetworks` are exempt by default (`smtpd_client_event_limit_exceptions`, default `$mynetworks`); list other trusted relays there.
## Failure modes
- Limits keyed on a NAT address block entire offices.
- Anvil counts per (service, client) combination, so submission and port 25 are counted separately.
- The limits are meant to stop abuse, not to regulate legitimate mail traffic (postconf(5) warning).
## Verify
- Check the mail log for the rejects/deferrals the limits cause; the exact message text is not given in the pages read.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): anvil(8), postconf(5), TUNING_README.
Confirmed: `smtpd_client_connection_count_limit`, `smtpd_client_connection_rate_limit`, `smtpd_client_message_rate_limit`, `smtpd_client_recipient_rate_limit`, `anvil_rate_time_unit`, `smtpd_client_event_limit_exceptions`, (service, client) counting.
Corrected or removed: the unconfirmed log message strings; the exception expression (default is `$mynetworks`).
Method: documentation only; no commands were run.
