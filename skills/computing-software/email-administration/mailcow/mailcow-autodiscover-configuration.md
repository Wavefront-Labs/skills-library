---
id: computing-software.email-administration.mailcow.mailcow-autodiscover-configuration
name: mailcow-autodiscover-configuration
category: computing-software
field: email-administration
product: mailcow
tags: [autodiscover-config, autoconfig, activesync, vars-local-inc-php, outlook-clients]
level: advanced
status: docs-checked
description: "Override mailcow autodiscover and autoconfig behaviour with vars.local.inc.php, including ActiveSync versus IMAP and which ports are announced."
sources: ["https://docs.mailcow.email/manual-guides/u_e-autodiscover_config/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Customising autodiscover and autoconfig

Autodiscover works out of the box; only change it for customisation. Newer Outlook clients, especially those delivered with Microsoft 365, will not autodiscover mail profiles. ActiveSync should not be used with a desktop client.

Create `data/web/inc/vars.local.inc.php` and define `$autodiscover_config`; it is merged with the defaults in `data/web/inc/vars.inc.php`. Key settings:
- `autodiscoverType`: `activesync` or `imap`. eM Client uses autodiscover but does not support ActiveSync, so mailcow excludes it from ActiveSync.
- `useEASforOutlook`: `yes` also uses ActiveSync for Outlook desktop on Windows (2013 or later); Outlook for Mac does not support ActiveSync.
- `imap`, `pop3`, `smtp` arrays with `server`, `port` and `tlsport`. Autodiscover always announces the TLS-wrapped services (SMTPS and IMAPS); autoconfig additionally announces the STARTTLS ports from `tlsport`. Do not put STARTTLS ports in `port`.

The defaults use the mailcow hostname and the IMAP, POP3 and SMTP port variables from the environment. The `activesync` URL is `https://` plus the hostname and `/Microsoft-Server-ActiveSync`, and `caldav` and `carddav` use the hostname and HTTPS port. To always use IMAP and SMTP instead of EAS, set `autodiscoverType` to `imap`; to disable ActiveSync for Outlook desktop clients, set `useEASforOutlook` to `no`.

## Checked

2026-11-09. Confirmed on the autodiscover config page: vars.local.inc.php merge into autodiscover_config, autodiscoverType, useEASforOutlook, tlsport and port rules, eM Client and Outlook notes. Replaced an unconfirmed DNS-record sentence with the page's defaults and the imap and no-EAS switches.

Method: docs-checked 2026-11-09 against the full autodiscover config page (u_e-autodiscover_config.en.md in mailcow-dockerized-docs).
