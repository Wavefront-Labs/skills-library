---
id: computing-software.systems-network-administration.duplicati.duplicati-email-and-custom-message-reports
name: duplicati-email-and-custom-message-reports
category: computing-software
field: systems-network-administration
product: duplicati
tags: [email-reports, smtp-notifications, report-templates, custom-message-content, parsedresult, send-mail-options]
level: practitioner
status: draft
description: "Send Duplicati backup results by email through an SMTP server and customise the subject and body with percent-delimited template variables."
sources: ["https://docs.duplicati.com/detailed-descriptions/monitoring-and-notifications/sending-reports-via-email", "https://docs.duplicati.com/detailed-descriptions/monitoring-and-notifications/sending-reports-via-email/sending-reports-with-email", "https://docs.duplicati.com/detailed-descriptions/monitoring-and-notifications/sending-reports-via-email/custom-message-content"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Email reports and custom message content in Duplicati

A backup that is set up and forgotten can silently stop working: revoked credentials, full storage or missing provider updates are common causes. The TrayIcon shows errors and warnings as desktop notifications, but automated monitoring is strongly recommended. Report options are the Duplicati Console, email, Jabber/XMPP, HTTP, Telegram and live status reports.

Email needs an SMTP server that accepts the mail: a URL, username and password from the provider, plus the recipient address (servers may restrict recipients; your own account is generally allowed). Basic settings can go in the general settings so they apply to every backup, or be overridden per backup in its advanced options (toggle between the editor and text views). Optional settings: sender address, subject line, body, and conditions on when to send. The community tool dupReport can summarise email logs into overviews.

Templates: Duplicati expands Windows-style `%EXAMPLE%` placeholders in the subject and body. The value may also be a path to a file containing the template. Any setting name can be used as a placeholder, plus:
- `%PARSEDRESULT%`: Success, Warning or Error
- `%RESULT%`: the log of the operation in a body; the same as PARSEDRESULT in a subject
- `%OPERATIONNAME%`: usually backup, but also restore and so on
- `%REMOTEURL%` and `%LOCALPATH%`: destination URL and source folders
- `%machine-id%`, `%backup-id%`, `%backup-name%`, `%machine-name%`: overridable with `--machine-id`, `--backup-id`, `--backup-name`, `--machine-name`.

Example: `Duplicati %OPERATIONNAME% for %backup-name% on %machine-name%`. JSON output uses the template only as a key lookup, so it is handled differently from text.
