---
id: computing-software.systems-network-administration.zabbix.email-and-webhook-media-types
name: email-and-webhook-media-types
category: computing-software
field: systems-network-administration
product: zabbix
tags: [media-types, email, webhook, smtp, alert-sendto, media]
level: practitioner
status: docs-checked
description: "Set up email and webhook media types and assign addresses to users so actions can deliver messages."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/notifications/media/email
  - https://www.zabbix.com/documentation/current/en/manual/config/notifications/media/webhook
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Media types live in Alerts > Media types. After configuring one, go to Users > Users and edit a user to assign media (an email address, or for webhooks a dedicated user that represents the webhook); actions then send to those users.

Email: choose an Email provider (Generic SMTP, Gmail, Gmail relay, Office365, Office365 relay). Gmail and Office365 options need only the sender email and password; server, port, helo and connection security are filled in automatically. For Generic SMTP set the SMTP server and port. The Email field is the From address; a display name needs the address in angle brackets, for example Zabbix_info <monitor@example.com>, and UTF-8 display names are allowed (a display name without angle brackets is invalid). Authentication can be None, Username and password, or OAuth (not supported for Office365 relay). Message format is HTML or Plain text. SMTP authentication needs the server compiled with --with-libcurl. Multiple notifications for one event are grouped in the same email thread. The Test link in the media types list sends a test message.

The password is exported as is when you export the media type, so use a user macro such as {$EMAIL_SMTP_PASSWORD} instead of a literal password to keep it out of exported files.

Webhook: HTTP calls driven by custom JavaScript, for helpdesk systems, chats and messengers. Zabbix provides many integrations (for example Slack, Telegram, Jira, PagerDuty, ServiceNow, Opsgenie, MS Teams Workflows). To use one, take its .yaml file from the templates/media directory of your Zabbix version or the Zabbix git repository, import it, then follow its Readme.md.

Custom webhook parameters are name and value pairs. New webhooks include URL, HTTPProxy, To:{ALERT.SENDTO}, Subject:{ALERT.SUBJECT} and Message:{ALERT.MESSAGE} by default; you may keep or remove them. Parameters support user macros, macros supported in problem notifications, and {ALERT.SENDTO}, {ALERT.SUBJECT}, {ALERT.MESSAGE}. The script must contain a return operator; use local variables rather than globals so simultaneous calls do not collide.

For Spiceworks, no webhook is needed: create an email media type and enter the helpdesk email address in the profile of a designated user.

## Checked

2026-11-09. Confirmed against the Email and Webhook media type pages: providers, auto-filled fields, From display name rules, authentication options, libcurl requirement, threading, password export advice, Test, integrations list, import steps, default parameters, macro support, return requirement, Spiceworks. Removed: the claim that webhook scripts use the same JavaScript engine as preprocessing and the Media tab wording. Pages read to the end of their configuration sections; OAuth token retrieval details not summarised.
Method: documentation only; no commands were run.
